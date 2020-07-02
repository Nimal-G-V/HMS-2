from modules import app, api
from modules.forms import PatientRegistration, UpdatePatient, Search, LoginForm, DeleteForm, Pharmacy, Diagnosis, Billing
from modules.models import Users, PatientDetails, PharmacyDetails, Diagnostics, Discharge
from flask import Flask, render_template, redirect, request, session, flash, url_for, jsonify, session
from modules.pipeline import pharmacy_pipe, diagnosis_pipe
from flask_restful import Resource
from datetime import date, datetime




def getID():
    id=0
    for user in PatientDetails.objects:
        id=user.patient_id
    return (id)+1


def get_medicine_total(patient_id):
    total=0
    medicine_data = list(PatientDetails.objects.aggregate(*pharmacy_pipe(patient_id=patient_id)))
    # print(medicine_data)
    for data in medicine_data:
        total += data["medicine"]["medicine_total_amount"]
    return total


def get_diagnosis_total(patient_id):
    total=0
    diagnosis_data = list(PatientDetails.objects.aggregate(*diagnosis_pipe(patient_id=patient_id)))
    # print(diagnosis_data)
    for data in diagnosis_data:
        total += data["diagnosis"]["test_amount"]
    return total


def get_no_of_days(admission_date):
    date_format = "%Y-%m-%d"
    a = datetime.strptime(str(admission_date), date_format)
    b = datetime.strptime(str(date.today()), date_format)
    # print(b-a)
    return b-a


def get_room_rent(room_type, no_of_days):
    if room_type =="Single":
        return no_of_days*8000
    if room_type =="General":
        return no_of_days*2000
    else:
        return no_of_days*4000


@app.route("/login", methods=["POST", "GET"])
def login():
    if session.get("uid"):
        return redirect("home")
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Users.objects(email=email).first()
        if password == user.password:
            session["uid"]=user.user_id
            session["first_name"]=user.first_name
            session["category"]=user.category
            flash(f"Hello! {user.first_name}, Your login is successfull.", category="success")
            return redirect("home")
        flash(f"E-mail or Password dosen't match.", category="danger")    
    return render_template("login.html", form=form, title="Login", set_login_active=True)


@app.route("/")
@app.route("/home")
def home():
    return render_template("base.html", title="Home")


@app.route("/patients")
def patients():
    if not session.get("uid"):
        return redirect("login")
    if not session.get("category") == "Desk":
        return redirect("home")
    patients_data = PatientDetails.objects.order_by("patient_id")
    return render_template("patients.html", patients=patients_data, title="List of Patients", set_patients_active=True)


@app.route("/register", methods=["POST", "GET"])
def register():
    if not session.get("uid"):
        return redirect("login")
    if not session.get("category") == "Desk":
        return redirect("home")
    form = PatientRegistration()
    if form.validate_on_submit():
        patient_id     = getID()
        ssn_id         = form.ssn_id.data
        patient_name   = form.patient_name.data
        patient_age    = form.patient_age.data
        admission_date = form.admission_date.data
        bed_type       = form.bed_type.data
        address        = form.address.data
        state          = form.state.data
        city           = form.city.data
        print(form.bed_type.data)
        print(patient_id)
        PatientDetails(
            patient_ssn_id=ssn_id, patient_id=patient_id, patient_name=patient_name, 
            patient_age=patient_age, patient_DOA=admission_date, patient_type_of_bed=bed_type,
            patient_address=address, patient_state=state, patient_city=city
        ).save()
        flash(f"{patient_name}'s, Details are successfully added.", category="success")
        return redirect(url_for("home"))
    if request.method=="POST":
        flash("Something went wrong. Please try again.", category="danger")
    return render_template("register.html", form=form, title="Register Patient", set_register_active=True)


@app.route("/update", methods=["POST", "GET"])
def update():
    if not session.get("uid"):
        return redirect("login")
    if not session.get("category") == "Desk":
        return redirect("home")
    forms=UpdatePatient()
    pid = request.form.get("pid")
    if request.method == "GET":
        return redirect(url_for("search"))
    if pid:
        return render_template("update.html", form=forms, pid=pid, title="Update Patient")
    if forms.validate_on_submit():
        PatientDetails.objects(patient_id=forms.patient_id.data).update(
                    set__patient_ssn_id      = forms.ssn_id.data,
                    set__patient_name        = forms.patient_name.data,
                    set__patient_age         = forms.patient_age.data,
                    set__patient_DOA         = forms.admission_date.data,
                    set__patient_type_of_bed = forms.bed_type.data,
                    set__patient_address     = forms.address.data,
                    set__patient_state       = forms.state.data,
                    set__patient_city        = forms.city.data
        )
        flash(f"{forms.patient_name.data}'s Details are successfully updated.", category="success")
        return redirect(url_for("patients"))
    if request.method=="POST":
        flash("Something went wrong. Please try again.", category="danger")
    return render_template("update.html", form=forms, pid=pid, title="Update Patient")


@app.route("/search", methods=["POST", "GET"])
def search():
    if not session.get("uid"):
        return redirect("login")
    if not session.get("category") == "Desk":
        return redirect("home")
    form = Search()
    id = form.patient_id.data
    if form.validate_on_submit():
        data = PatientDetails.objects(patient_id=id).first()
        flash(f"Patient with ID: {id}, Found !.", category="success")
        return render_template("search.html", display=True, patient=data, form=form, title="Search Patient", set_search_active=True)
    if request.method=="POST":
        flash(f"Patient with ID: {id}, Not Found !.", category="danger")
    return render_template("search.html", display=False, form=form, title="Search Patient", set_search_active=True)


@app.route("/delete", methods=["POST", "GET"])
def delete():
    if request.method == "POST":
        forms = DeleteForm()
        pid = request.form.get("pid")
        user = PatientDetails.objects(patient_id=pid).first()
        if forms.yes.data:
            user.delete()
            flash(f"{user.patient_name}'s details' is successfully deleted.", category="success")
            return redirect(url_for("patients"))
        if forms.no.data:
            return redirect(url_for("patients"))
        return render_template("delete.html", patient=user, form=forms)
    return redirect(url_for("home"))


@app.route("/pharmacy", methods=["POST", "GET"])
def pharmacy():
    if not session.get("uid"):
        return redirect("login")
    if not session.get("category") == "Pharma":
        return redirect("home")
    form=Pharmacy()
    if form.get.data:
        patient_data = PatientDetails.objects(patient_id=form.get_id.data).first()
        if patient_data:
            medicine_data = list(PatientDetails.objects.aggregate(*pharmacy_pipe(patient_id=form.get_id.data)))
            return render_template("pharmacy.html", form=form, got_details=True, got_to_add=False,
                                    patient_data=patient_data, medicine_data=medicine_data, 
                                    set_pharmacy_active=True, title="Pharmacy")
        else:
            flash(f"Patient with ID: {form.get_id.data}, Not Found !.", category="danger")
    
    return render_template("pharmacy.html", form=form, got_details=False, 
                            set_pharmacy_active=True, title="Pharmacy")


@app.route("/diagnostics", methods=["POST", "GET"])
def diagnostics():
    if not session.get("uid"):
        return redirect("login")
    if not session.get("category") == "Diagno":
        return redirect("home")
    form=Diagnosis()
    if form.get.data:
        patient_data = PatientDetails.objects(patient_id=form.get_id.data).first()
        if patient_data:
            diagnosis_data = list(PatientDetails.objects.aggregate(*diagnosis_pipe(patient_id=form.get_id.data)))
            return render_template("diagnosis.html", form=form, got_details=True, 
                                    got_to_add=False, patient_data=patient_data, 
                                    diagnosis_data=diagnosis_data, title="Diagnostics")
        else:
            flash(f"Patient with ID: {form.get_id.data}, Not Found !.", category="danger")
    
    return render_template("diagnosis.html", form=form, got_details=False, 
                            title="Diagnostics")


@app.route("/billing", methods=["POST", "GET"])
def billing():
    if not session.get("uid"):
        return redirect("login")
    if not session.get("category") == "Desk":
        return redirect("home")
    form=Billing()
    if form.get.data:
        patient_data = PatientDetails.objects(patient_id=form.get_id.data).first()
        if patient_data:
            medicine_total=0
            diagnosis_total = 0
            no_of_days = get_no_of_days(patient_data["patient_DOA"])
            day_of_discharge = date.today()
            room_rent = get_room_rent(patient_data["patient_type_of_bed"], no_of_days.days)
            medicine_data = list(PatientDetails.objects.aggregate(*pharmacy_pipe(patient_id=form.get_id.data)))
            diagnosis_data = list(PatientDetails.objects.aggregate(*diagnosis_pipe(patient_id=form.get_id.data)))
            if medicine_data:
                medicine_total = get_medicine_total(form.get_id.data)
            if diagnosis_data:
                diagnosis_total = get_diagnosis_total(form.get_id.data)
            grand_total = (medicine_total+diagnosis_total+room_rent)
            return render_template("billing.html", form=form, patient_data=patient_data, got_details=True,
                                    medicine_data=medicine_data, diagnosis_data=diagnosis_data,
                                    no_of_days=no_of_days.days, day_of_discharge=day_of_discharge,
                                    medicine_total=medicine_total, diagnosis_total=diagnosis_total,
                                    room_rent=room_rent, grand_total=grand_total, title="Billing")
        else:
            flash(f"Patient with ID: {form.get_id.data}, Not Found !.", category="danger")
    
    return render_template("billing.html", form=form, got_details=False, title="Billing")


@app.route("/logout")
def logout():
    if session.get("uid"):
        session["uid"]=False
        session["first_name"]=False
        session["category"]=False
        flash(f"Logged out Successfully!.", category="success")
    return redirect("login")


@app.route("/update/<id>")
def getdata(id):
    data = PatientDetails.objects(patient_id=id).first()
    return jsonify(data)


class Add_Medicine(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        if data:
            if len(data['name']) == len(data['quantity']) and len(data['quantity']) == len(data['rate']) and len(data['rate']) == len(data['total']):
                for i in range(len(data['name'])):
                    print()
                    PharmacyDetails(patient_id=data['pid'], 
                                    medicine_name=data['name'][i], 
                                    medicine_quantity=int(data['quantity'][i]), 
                                    medicine_rate=int(data['rate'][i]),
                                    medicine_total_amount=int(data['total'][i])).save()
                flash("The medicines are added to the patient.", category="success")
                return "Saved Successfully"
        flash("Something went wrong. Please try again.", category="danger")
        return "Something went wrong"
    
    def get(self):
        return "Pharmacy Details"


class Add_Diagnostics(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        if data:
            if len(data['name']) == len(data['amount']):
                for i in range(len(data['name'])):
                    Diagnostics(patient_id=data['pid'], 
                                test_name=data['name'][i], 
                                test_amount=int(data['amount'][i])).save()
                flash("The diagnostics details are added to the patient.", category="success")
                return "Saved Successfully"
        flash("Something went wrong. Please try again.", category="danger")
        return "Something went wrong"
    
    def get(self):
        return "Diagnostics Details"


class Add_Discharge(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        if data:
            Discharge(patient_id=data["pid"], patient_discharge_date=data["discharge"], grand_total=data["grand_total"]).save()
            user = PatientDetails.objects(patient_id=data["pid"]).first()
            user.delete()
            flash("The discharge details is added.", category="success")
            return "Saved Successfully"
        flash("Something went wrong. Please try again.", category="danger")
        return "Something went wrong"

api.add_resource(Add_Medicine, "/update-medicines-for-patient")
api.add_resource(Add_Diagnostics, "/update-diagnosis-for-patient")
api.add_resource(Add_Discharge, "/update-discharge-details")

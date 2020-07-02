from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField,  SelectField, TextAreaField, SubmitField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, Email
from modules.models import PatientDetails, Users
from modules.selectfeilddata import state, city

# Patient Registration form!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class PatientRegistration(FlaskForm):
    ssn_id = IntegerField("SSN ID", validators=[
        (InputRequired(message="This filed must not empty!")), 
        # Length(max=6, message="Maximum length of ssn_id is 6 digits")
        ])
    
    patient_name = StringField("Patient Name", validators=[
        (InputRequired(message="This filed must not empty!")),
        Length(min=3, max=20, message="maximum characters 20")
        ])
    
    patient_age = IntegerField("Patient Age", validators=[
        (InputRequired(message="This filed must not empty!")),
        # Length(max=2, message="Please enter valid age!")
        ])

    admission_date = DateField("Admission Date", format="%Y-%m-%d", validators=[
        (InputRequired(message="This filed must not empty!"))
        ])

    bed_type = SelectField("Type of Bed", choices=[('General','General Ward'),('Semi','Semi Sharing'), ('Single','Single Room')], validators=[
        (InputRequired(message="This filed must not empty!"))
        ])

    address = TextAreaField("Address", validators=[
        (InputRequired(message="This filed must not empty!"))
        ])

    state = SelectField("State", choices=state, validators=[
        (InputRequired(message="This filed must not empty!"))
        ])

    city = SelectField("City", choices=city, validators=[
        (InputRequired(message="This filed must not empty!"))
        ])

    submit = SubmitField("Submit")


    def validate_ssn_id(self, ssn_id):
        user = PatientDetails.objects(patient_ssn_id=ssn_id.data).first()
        if user:
            raise ValidationError("The SSN ID Already exists, Try Again!")




# Patient Updation form!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class UpdatePatient(FlaskForm):
    patient_id = IntegerField("Patient ID", validators=[
        (InputRequired(message="This filed must not empty!")), 
        # Length(max=6, message="Maximum length of ssn_id is 6 digits")
        ])

    get_details = SubmitField("Get this patient details")

    ssn_id = IntegerField("SSN ID", validators=[
        (InputRequired(message="This filed must not empty!")), 
        # Length(max=6, message="Maximum length of ssn_id is 6 digits")
        ])
    
    patient_name = StringField("Patient Name", validators=[
        InputRequired(message="This filed must not empty!"),
        Length(min=3, max=20, message="maximum characters 20")
        ])
    
    patient_age = IntegerField("Patient Age", validators=[
        (InputRequired(message="This filed must not empty!")),
        # Length(max=2, message="Please enter valid age!")
        ])

    admission_date = DateField("Admission Date", format='%Y-%m-%d', validators=[
        (InputRequired(message="This filed must not empty!"))
        ])

    bed_type = SelectField("Type of Bed", choices=[('General','General Ward'),('Semi','Semi Sharing'), ('Single','Single Room')], validators=[
        (InputRequired(message="This filed must not empty!"))
        ])

    address = TextAreaField("Address", validators=[
        (InputRequired(message="This filed must not empty!"))
        ])

    state = SelectField("State", choices=state, validators=[
        (InputRequired(message="This filed must not empty!"))
        ])

    city = SelectField("City", choices=city, validators=[
        (InputRequired(message="This filed must not empty!"))
        ])

    update = SubmitField("Update")

    def validate_patient_id(self, patient_id):
        user = PatientDetails.objects(patient_id=patient_id.data).first()
        if not user:
            raise ValidationError(f"There is no user with patient ID : {patient_id.data}")


class Search(FlaskForm):
    patient_id = IntegerField("Patient ID", validators=[
        (InputRequired(message="This filed must not empty!")), 
        # Length(max=6, message="Maximum length of ssn_id is 6 digits")
        ])
    
    search = SubmitField("Search")

    def validate_patient_id(self, patient_id):
        user = PatientDetails.objects(patient_id=patient_id.data).first()
        if not user:
            raise ValidationError(f"There is no user with patient ID : {patient_id.data}")


class LoginForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("Login")

class DeleteForm(FlaskForm):
    yes = SubmitField("YES")
    no = SubmitField("NO")

class Pharmacy(FlaskForm):
    get_id = IntegerField("Patient ID", validators=[DataRequired()])
    get = SubmitField("Get Details")
    add_medicines = SubmitField("Add Medicines")

class Diagnosis(FlaskForm):
    get_id = IntegerField("Patient ID", validators=[DataRequired()])
    get = SubmitField("Get Details")
    add_diagnosis = SubmitField("Add Diagnosis")

class Billing(FlaskForm):
    get_id = IntegerField("Patient ID", validators=[DataRequired()])
    get = SubmitField("Get Details")
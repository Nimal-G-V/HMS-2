from modules import db

class Users(db.Document):
    user_id = db.IntField( unique=True)
    first_name = db.StringField( max_length = 50)
    email =   db.StringField( max_length=50, unique=True )
    password = db.StringField( max_length = 50 )
    category = db.StringField( max_length = 50 )

class Patient(db.Document):
    hospital_id = db.IntField( unique=True )
    patient_id = db.IntField( unique=True)

class PatientDetails(db.Document):
    patient_ssn_id = db.IntField( unique=True)
    patient_id = db.IntField( unique=True)
    patient_name = db.StringField( max_length = 50)
    patient_age = db.IntField()
    patient_DOA = db.DateField(max_length=50)
    patient_type_of_bed = db.StringField(max_length=50)
    patient_address = db.StringField(max_length=100)
    patient_state = db.StringField(max_length=100)
    patient_city = db.StringField(max_length=100)

class PharmacyDetails(db.Document):
    patient_id = db.IntField()
    medicine_name = db.StringField(max_length = 50)
    medicine_quantity = db.IntField()
    medicine_rate = db.IntField()
    medicine_total_amount = db.IntField()

class Diagnostics(db.Document):
    patient_id = db.IntField()
    test_name = db.StringField(max_length = 50)
    test_amount = db.IntField()

class Discharge(db.Document):
    patient_id = db.IntField()
    patient_discharge_date = db.DateField(max_length=50)
    grand_total = db.IntField()

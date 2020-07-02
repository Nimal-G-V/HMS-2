def pharmacy_pipe(patient_id):
    pipeline = [
    {
        '$lookup': {
            'from': 'pharmacy_details', 
            'localField': 'patient_id', 
            'foreignField': 'patient_id', 
            'as': 'medicine'
        }
    }, {
        '$unwind': {
            'path': '$medicine', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$match': {
            'patient_id': patient_id
        }
    }
    ]
    return pipeline


def diagnosis_pipe(patient_id):
    pipeline=[
    {
        '$lookup': {
            'from': 'diagnostics', 
            'localField': 'patient_id', 
            'foreignField': 'patient_id', 
            'as': 'diagnosis'
        }
    }, {
        '$unwind': {
            'path': '$diagnosis', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$match': {
            'patient_id': patient_id
        }
    }
    ]
    return pipeline
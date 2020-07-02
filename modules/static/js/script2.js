    var pid = document.getElementById("pid").value;
    console.log(pid);
    fetch("/update/"+pid).then(function(response){
        response.json().then(function(data){
            document.getElementById("patient_id").focus();
            document.getElementById("patient_id").defaultValue=data.patient_id;
            document.getElementById("patient_name").focus();
            document.getElementById("patient_name").defaultValue=data.patient_name;
            document.getElementById("patient_age").focus();
            document.getElementById("patient_age").defaultValue=data.patient_age;
            document.getElementById("ssn_id").focus();
            document.getElementById("ssn_id").defaultValue=data.patient_ssn_id;
            document.getElementById("address").focus();
            document.getElementById("address").defaultValue=data.patient_address;
            var BedSelect = document.getElementById('bed_type');
            for(var i, j = 0; i = BedSelect.options[j]; j++) {
                if(i.value == data.patient_type_of_bed) {
                    BedSelect.selectedIndex = j;
                    break;
                }
            }
            var element = document.getElementById('state');
            var event = new Event('change');
            var StateSelect = document.getElementById('state');
            for(var i, j = 0; i = StateSelect.options[j]; j++) {
                if(i.value == data.patient_state) {
                    StateSelect.selectedIndex = j;
                    element.dispatchEvent(event);
                    break;
                }
            }
            var CitySelect = document.getElementById('city');
            for(var i, j = 0; i = CitySelect.options[j]; j++) {
                if(i.value == data.patient_city) {
                    CitySelect.selectedIndex = j;
                    break;
                }
            }
            const formatDate = (d) => {
                let month = '' + (d.getMonth() + 1),
                    day = '' + d.getDate(),
                    year = d.getFullYear();
                if (month.length < 2)
                    month = '0' + month;
                if (day.length < 2)
                    day = '0' + day;
                return [year, month, day].join('-');
            }
            let da = new Date(data.patient_DOA.$date)
            var value = formatDate(da)
            document.getElementById("admission_date").focus();
            document.getElementById("admission_date").defaultValue=value;
            // console.log(value);
        })
    })

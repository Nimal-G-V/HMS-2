$(document).ready(() => {

    let pid
    if (document.getElementById("get_id")) {
        pid = document.getElementById("get_id").value
    }

    let trow = []


    let id = 0

    if (document.getElementById("addDiagnosis")) {
        document.getElementById("addDiagnosis").addEventListener('click', () => {

           let dname = document.getElementById("Diagnosisname").value
            let damou = document.getElementById("DiagnosisAmo").value
            

            if (dname.length == 0 && damou == 0) {
                return
            }
        
            let tobj = { id: id, name: dname, amount:damou }
            trow.push(tobj)
            var tableRef = document.getElementById('myTable').getElementsByTagName('tbody')[0];
            var newRow = tableRef.insertRow();
            newRow.id = id
            Object.keys(tobj).forEach((key, index) => {
                if (index !== 0) {
                    var newCell = newRow.insertCell(index - 1);
                    var newText = document.createTextNode(tobj[key]);
                    newCell.appendChild(newText);
                }
            })
            let newCell = newRow.insertCell(2)
            var button = document.createElement('button');
            button.id = id
            id++
            button.innerHTML = 'Delete';
            button.addEventListener('click', deleteRow);
            newCell.appendChild(button)
        })
    }
    const deleteRow = (event) => {
        let row_index = parseInt(event.target.id)
        document.getElementById(event.target.id).remove()
       
        trow = trow.filter(tcol => { tcol.id !== row_index })
    
    }

    if (document.getElementById('update')) {
        document.getElementById('update').addEventListener('click', () => {
            let diagnosis_name_list = []
            let diagnosis_amount_list = []
            trow.forEach(tcol => {
                diagnosis_name_list.push(tcol.name);
                diagnosis_amount_list.push(tcol.amount);
            })
            let data = {
                pid: pid,
                name: diagnosis_name_list,
                amount: diagnosis_amount_list
            }
            console.log(data)
            fetch("http://127.0.0.1:5000/update-diagnosis-for-patient", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                body: JSON.stringify(data),
            }).then(response => {
                // location.replace("http://127.0.0.1:5000/diagnostics")
                location.reload()
            })


        })

    }

})
let first=true;
let count=1;

function addOneMoreFeild(){
    var table = document.getElementById("insert-inside");

    var tr = document.createElement("tr");

    var td1 = document.createElement("td");
    var td2 = document.createElement("td");

    var label1 = document.createElement("label");
    label1.setAttribute("for", "diagnosis_name");
    label1.appendChild(document.createTextNode("Diagnosis Name"));
    var label2 = document.createElement("label");
    label2.setAttribute("for", "diagnosis_amount");
    label2.appendChild(document.createTextNode("Amount (Rs.)"));

    var input1 = document.createElement("input");
    input1.setAttribute("type", "text");
    input1.setAttribute("name", "diagnosis_name");
    input1.setAttribute("class", "form-control form-control-sm");
    var input2 = document.createElement("input");
    input2.setAttribute("type", "text");
    input2.setAttribute("name", "diagnosis_amount");
    input2.setAttribute("class", "form-control form-control-sm");

    td1.appendChild(label1);
    td1.appendChild(input1);
    td2.appendChild(label2);
    td2.appendChild(input2);

    tr.appendChild(td1);
    tr.appendChild(td2);

    if(first){
        var div = document.getElementById("add-update");
        var td3 = document.createElement("td");

        var add_button = document.createElement("button");
        add_button.type="button";
        add_button.id="add-input-feild";
        add_button.innerText="ADD";
        add_button.setAttribute("onclick", "addOneMoreFeild()");
        var update_button = document.createElement("button");
        update_button.type="button";
        update_button.id="update";
        update_button.innerText="UPDATE";
        update_button.setAttribute("onclick", "updateDetails()");

        td3.id="fix";
        td3.rowSpan=count++;
        td3.appendChild(add_button); 

        tr.appendChild(td3); 

        div.appendChild(update_button);

        var add_diagnosis = document.getElementById("add-daignosis");
        add_diagnosis.remove();

        first=false;
    }else{
        var td = document.getElementById("fix");
        td.rowSpan=count++;
    }
    table.appendChild(tr);
}

function updateDetails(){

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var diagnosis_name = document.getElementsByName("diagnosis_name");
    var diagnosis_amount = document.getElementsByName("diagnosis_amount");
    var diagnosis_name_list=[];
    var diagnosis_amount_list=[];

    for(let i=0; i<diagnosis_name.length; i++){
        diagnosis_name_list.push(diagnosis_name[i].value);
        diagnosis_amount_list.push(diagnosis_amount[i].value);
    }
    var data ={
        "pid": document.getElementById("get_id").value,
        "name": diagnosis_name_list,
        "amount": diagnosis_amount_list
    }

    // alert(medicine_name_list);


    var raw = JSON.stringify(data);

    var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
    };

    fetch("http://127.0.0.1:5000/update-diagnosis-for-patient", requestOptions)
            .then(response => response.text())
            .then(function(data){
                // location.replace("http://127.0.0.1:5000/diagnostics");
                location.reload();
            })
            .catch(function(error){
                console.log('error', error);
            });
}
let first=true;
let count=1;

function addOneMoreFeild(){
    var table = document.getElementById("insert-inside");

    var tr = document.createElement("tr");

    var td1 = document.createElement("td");
    var td2 = document.createElement("td");
    var td3 = document.createElement("td"); 
    var td4 = document.createElement("td");

    var label1 = document.createElement("label");
    label1.setAttribute("for", "medicine_name");
    label1.appendChild(document.createTextNode("Medicine Name"));
    var label2 = document.createElement("label");
    label2.setAttribute("for", "medicine_quantity");
    label2.appendChild(document.createTextNode("Quantity"));
    var label3 = document.createElement("label");
    label3.setAttribute("for", "medicine_rate");
    label3.appendChild(document.createTextNode("Rate (Rs.)"));
    var label4 = document.createElement("label");
    label4.setAttribute("for", "medicine_total_amount");
    label4.appendChild(document.createTextNode("Total Amount"));

    var input1 = document.createElement("input");
    input1.setAttribute("type", "text");
    input1.setAttribute("name", "medicine_name");
    input1.setAttribute("class", "form-control form-control-sm");
    var input2 = document.createElement("input");
    input2.setAttribute("type", "text");
    input2.setAttribute("name", "medicine_quantity");
    input2.setAttribute("class", "form-control form-control-sm");
    var input3 = document.createElement("input");
    input3.setAttribute("type", "text");
    input3.setAttribute("name", "medicine_rate");
    input3.setAttribute("class", "form-control form-control-sm");
    var input4 = document.createElement("input");
    input4.setAttribute("type", "text");
    input4.setAttribute("name", "medicine_total_amount");
    input4.setAttribute("class", "form-control form-control-sm");

    td1.appendChild(label1);
    td1.appendChild(input1);
    td2.appendChild(label2);
    td2.appendChild(input2);
    td3.appendChild(label3);
    td3.appendChild(input3);
    td4.appendChild(label4);
    td4.appendChild(input4);

    tr.appendChild(td1);
    tr.appendChild(td2);
    tr.appendChild(td3);
    tr.appendChild(td4);

    if(first){
        var div = document.getElementById("add-update");
        var td5 = document.createElement("td");

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

        td5.id="fix";
        td5.rowSpan=count++;
        td5.appendChild(add_button); 

        tr.appendChild(td5); 

        div.appendChild(update_button);

        var add_medicine = document.getElementById("add-medicine");
        add_medicine.remove();

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

    var medicine_name = document.getElementsByName("medicine_name");
    var medicine_quantity = document.getElementsByName("medicine_quantity");
    var medicine_rate = document.getElementsByName("medicine_rate");
    var medicine_total_amount = document.getElementsByName("medicine_total_amount");
    var medicine_name_list=[];
    var medicine_quantity_list=[];
    var medicine_rate_list=[];
    var medicine_total_amount_list=[];

    for(let i=0; i<medicine_name.length; i++){
        medicine_name_list.push(medicine_name[i].value);
        medicine_quantity_list.push(medicine_quantity[i].value);
        medicine_rate_list.push(medicine_rate[i].value);
        medicine_total_amount_list.push(medicine_total_amount[i].value);
    }
    var data ={
        "pid": document.getElementById("get_id").value,
        "name": medicine_name_list,
        "quantity": medicine_quantity_list,
        "rate": medicine_rate_list,
        "total": medicine_total_amount_list
    }

    // alert(medicine_name_list);


    var raw = JSON.stringify(data);

    var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
    };

    fetch("http://127.0.0.1:5000/update-medicines-for-patient", requestOptions)
            .then(response => response.text())
            .then(function(data){
                // location.replace("http://127.0.0.1:5000/pharmacy");
                location.reload();
            })
            .catch(function(error){
                console.log('error', error);
            });
}
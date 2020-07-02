$(document).ready(() => {

    let pid
    if (document.getElementById("get_id")) {
        pid = document.getElementById("get_id").value
        console.log(pid)
    }

    let trow = []


    let id = 0

    if (document.getElementById("addRow")) {
        document.getElementById("addRow").addEventListener('click', () => {

            mname = document.getElementById("mname").value
            let mrate = document.getElementById("rate").value
            let mqty = document.getElementById("qty").value

            if (mname.length == 0 && mrate == 0 && mqty == 0) {
                return
            }
            let mamount = mrate * mqty
            let tobj = { id: id, name: mname, qty: mqty, rate: mrate, amount: mamount }
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
            let newCell = newRow.insertCell(4)
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
        console.log(row_index)
        trow = trow.filter(tcol => { tcol.id !== row_index })
        console.log(trow)
    }

    if (document.getElementById('update')) {
        document.getElementById('update').addEventListener('click', () => {
            let name_list = []
            let qty_list = []
            let rate_list = []
            let amount_list = []
            trow.forEach(tcol => {
                name_list.push(tcol.name)
                qty_list.push(tcol.qty)
                rate_list.push(tcol.rate)
                amount_list.push(tcol.amount)
            })
            let data = {
                pid: pid,
                name: name_list,
                quantity: qty_list,
                rate: rate_list,
                total: amount_list
            }

            fetch("http://127.0.0.1:5000/update-medicines-for-patient", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                body: JSON.stringify(data),
            }).then(response => {
                // location.replace("http://127.0.0.1:5000/pharmacy")
                location.reload();
            })


        })

    }

})
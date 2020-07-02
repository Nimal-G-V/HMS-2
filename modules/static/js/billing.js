document.querySelector("#discharge").addEventListener("click", discharge);
function discharge(){
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    var data={
        "pid": document.getElementById("patient-id").value,
        "discharge": document.getElementById("patient-discharge").value,
        "grand_total": document.getElementById("grand-total").value
    }
    var raw = JSON.stringify(data);

    var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
    };

    fetch("http://127.0.0.1:5000//update-discharge-details", requestOptions)
            .then(response => response.text())
            .then(function (){
                location.replace("http://127.0.0.1:5000//");
            })
            .catch(error => console.log('error', error));
}
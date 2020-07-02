var dropdown = document.getElementsByClassName("dropdown-btn");
let flag = 0;
let desca = document.getElementById("desca")
for (let i = 0; i < dropdown.length; i++) {
    dropdown[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var dropdownContent = this.nextElementSibling;
        if (dropdownContent.style.display === "block") {
            dropdownContent.style.display = "none";
            desca.className = "fa fa-sort-desc"
        } else {
            dropdownContent.style.display = "block";
            desca.className = "fa fa-sort-asc asce"
        }
    });
}


const togglenav = () => {
    if (flag == 0) {
        flag = 1
        document.getElementById("mySidenav").style.width = "250px";
        document.getElementById("main").style.marginLeft = "250px";
    } else {
        flag = 0
        document.getElementById("mySidenav").style.width = "0";
        document.getElementById("main").style.marginLeft = "0";
    }
}
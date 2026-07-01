// ================================
// SMART LIBRARY DASHBOARD
// ================================

document.addEventListener("DOMContentLoaded", function () {

    loadDateTime();
    updateGreeting();
    animateCards();
    initializeCounters();

});

// ================================
// LIVE DATE & TIME
// ================================

function loadDateTime() {

    const dateElement =
    document.getElementById("currentDateTime");

    if (!dateElement) return;

    setInterval(() => {

        let now = new Date();

        dateElement.innerHTML =
        now.toLocaleString();

    }, 1000);

}

// ================================
// GREETING
// ================================

function updateGreeting() {

    const greeting =
    document.getElementById("greeting");

    if (!greeting) return;

    let hour =
    new Date().getHours();

    let text = "";

    if(hour < 12){
        text = "Good Morning";
    }
    else if(hour < 17){
        text = "Good Afternoon";
    }
    else{
        text = "Good Evening";
    }

    greeting.innerHTML = text;

}

// ================================
// CARD ANIMATION
// ================================

function animateCards(){

    let cards =
    document.querySelectorAll(".dashboard-card");

    cards.forEach((card,index)=>{

        card.style.opacity = "0";
        card.style.transform = "translateY(30px)";

        setTimeout(()=>{

            card.style.transition = "0.6s";

            card.style.opacity = "1";
            card.style.transform = "translateY(0px)";

        },index * 150);

    });

}

// ================================
// COUNTER ANIMATION
// ================================

function initializeCounters(){

    const counters =
    document.querySelectorAll(".counter");

    counters.forEach(counter => {

        let target =
        parseInt(counter.innerText);

        let count = 0;

        let increment =
        Math.ceil(target / 50);

        let updateCounter = () => {

            count += increment;

            if(count > target){

                count = target;

            }

            counter.innerText = count;

            if(count < target){

                setTimeout(updateCounter,20);

            }

        };

        updateCounter();

    });

}

// ================================
// SEARCH MEMBER
// ================================

function searchMember(){

    let input =
    document.getElementById("searchMember");

    if(!input) return;

    let filter =
    input.value.toUpperCase();

    let table =
    document.getElementById("memberTable");

    let tr =
    table.getElementsByTagName("tr");

    for(let i=1;i<tr.length;i++){

        let td =
        tr[i].getElementsByTagName("td")[1];

        if(td){

            let txtValue =
            td.textContent ||
            td.innerText;

            if(txtValue.toUpperCase()
               .indexOf(filter) > -1){

                tr[i].style.display = "";

            }
            else{

                tr[i].style.display = "none";

            }

        }

    }

}

// ================================
// SEARCH BOOK
// ================================

function searchBook(){

    let input =
    document.getElementById("searchBook");

    if(!input) return;

    let filter =
    input.value.toUpperCase();

    let table =
    document.getElementById("bookTable");

    let tr =
    table.getElementsByTagName("tr");

    for(let i=1;i<tr.length;i++){

        let td =
        tr[i].getElementsByTagName("td")[2];

        if(td){

            let txt =
            td.textContent ||
            td.innerText;

            if(txt.toUpperCase()
                .indexOf(filter) > -1){

                tr[i].style.display = "";

            }
            else{

                tr[i].style.display = "none";

            }

        }

    }

}

// ================================
// NOTIFICATION
// ================================

function showNotification(message){

    alert(message);

}

// ================================
// LOGOUT CONFIRM
// ================================

function confirmLogout(){

    return confirm(
        "Are you sure you want to logout?"
    );

}
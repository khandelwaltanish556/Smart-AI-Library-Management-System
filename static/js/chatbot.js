// ======================================
// SMART LIBRARY CHATBOT
// ======================================

document.addEventListener("DOMContentLoaded", () => {

    const sendBtn =
    document.getElementById("sendBtn");

    const messageInput =
    document.getElementById("message");

    if(sendBtn){

        sendBtn.addEventListener(
            "click",
            sendMessage
        );

    }

    if(messageInput){

        messageInput.addEventListener(
            "keypress",
            function(e){

                if(e.key === "Enter"){

                    e.preventDefault();

                    sendMessage();

                }

            }
        );

    }

});

// ======================================
// SEND MESSAGE
// ======================================

async function sendMessage(){

    const input =
    document.getElementById("message");

    const chatBox =
    document.getElementById("chatBox");

    const message =
    input.value.trim();

    if(message === ""){

        return;

    }

    // USER MESSAGE

    appendUserMessage(message);

    input.value = "";

    // TYPING EFFECT

    const typingDiv =
    showTyping();

    try{

        const response =
        await fetch("/chatbot",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                message:message
            })

        });

        const data =
        await response.json();

        typingDiv.remove();

        appendBotMessage(
            data.response
        );

    }

    catch(error){

        typingDiv.remove();

        appendBotMessage(
            "Server connection failed."
        );

        console.error(error);

    }

}

// ======================================
// USER MESSAGE
// ======================================

function appendUserMessage(message){

    const chatBox =
    document.getElementById("chatBox");

    const div =
    document.createElement("div");

    div.className =
    "user-message";

    div.innerHTML = `
        <strong>You:</strong><br>
        ${message}
    `;

    chatBox.appendChild(div);

    scrollBottom();

}

// ======================================
// BOT MESSAGE
// ======================================

function appendBotMessage(message){

    const chatBox =
    document.getElementById("chatBox");

    const div =
    document.createElement("div");

    div.className =
    "bot-message";

    div.innerHTML = `
        <strong>Library AI:</strong><br>
        ${message}
    `;

    chatBox.appendChild(div);

    scrollBottom();

}

// ======================================
// TYPING ANIMATION
// ======================================

function showTyping(){

    const chatBox =
    document.getElementById("chatBox");

    const typing =
    document.createElement("div");

    typing.className =
    "bot-message";

    typing.id =
    "typing";

    typing.innerHTML =
    "<strong>Library AI:</strong><br>Typing...";

    chatBox.appendChild(
        typing
    );

    scrollBottom();

    return typing;

}

// ======================================
// AUTO SCROLL
// ======================================

function scrollBottom(){

    const chatBox =
    document.getElementById("chatBox");

    chatBox.scrollTop =
    chatBox.scrollHeight;

}

// ======================================
// QUICK QUESTIONS
// ======================================

function askQuestion(question){

    document.getElementById(
        "message"
    ).value = question;

    sendMessage();

}

// ======================================
// CLEAR CHAT
// ======================================

function clearChat(){

    const chatBox =
    document.getElementById("chatBox");

    chatBox.innerHTML = "";

}

// ======================================
// SAVE CHAT
// ======================================

function saveChat(){

    const chatBox =
    document.getElementById("chatBox");

    const content =
    chatBox.innerText;

    const blob =
    new Blob(
        [content],
        {type:"text/plain"}
    );

    const link =
    document.createElement("a");

    link.href =
    URL.createObjectURL(blob);

    link.download =
    "library_chat.txt";

    link.click();

}

// ======================================
// SAMPLE QUESTIONS
// ======================================

function loadSampleQuestions(){

    const questions = [

        "How many books are available?",

        "Show overdue books",

        "Most issued book",

        "Library timing",

        "Latest notices",

        "Student attendance report",

        "Fine calculation"

    ];

    console.log(
        "Sample Questions:",
        questions
    );

}
async function askAI() {

let question = document.getElementById("question").value;

document.getElementById("answer").innerText = "Thinking...";

let response = await fetch("/ask", {

method: "POST",

headers: {
"Content-Type": "application/json"
},

body: JSON.stringify({question: question})

});

let data = await response.json();

document.getElementById("answer").innerText = data.answer;

}

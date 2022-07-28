const email_input = document.getElementById("email_input")
const alertDiv = document.getElementById("alertDiv")
const alert_p = document.getElementById("alert")
const messagesDiv = document.getElementById("messagesDiv")
const message = document.getElementById("message")
const email_input_div = document.getElementById("email_input_div")
const email_sent_message = document.getElementById("email_sent_message")
const forename_input = document.getElementById("forename_input")
const surname_input = document.getElementById("surname_input")
const initial_message_div = document.getElementById("initial_message_div")

function validate_email (emailAdress)
{
  let regexEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  if (emailAdress.match(regexEmail)) {
    return true;
  } else {
    return false;
  }
}

function submit_pressed(){
  email = email_input.value
  forename = forename_input.value
  surname = surname_input.value
  full_name = forename + " " + surname
  if (validate_email(email)){
    send_email(email,full_name)
  }else{
    alertDiv.style.display = "block";
    alert_p.innerHTML = "The email is not in a valid format. Please try again";
  }
}

const send_email = async (email,full_name) => {
   const url = '/book_a_session_login_email'; // the URL to send the HTTP request to
   var content = {
     "email":email,
     "full_name":full_name
   }
   const body = JSON.stringify(content); // whatever you want to send in the body of the HTTP request
   const headers = {'Content-Type': 'application/json'}; // if you're sending JSON to the server
   const method = 'POST';
   const response = await fetch(url, { method, body, headers });
   const data = await response.text(); // or response.json() if your server returns JSON
   if (data == "Email Sent"){
     alertDiv.style.display = "none";
     messagesDiv.style.display = "block";
     message.innerHTML = data;
     email_sent_message.style.display="block"
     email_input_div.style.display="none"
     initial_message_div.style.display="none"
   }else{
     messagesDiv.style.display = "none";
     alertDiv.style.display = "block";
     alert_p.innerHTML = data;
   }
   email_input.innerHTML = ""

}

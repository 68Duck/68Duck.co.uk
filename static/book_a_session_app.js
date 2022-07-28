const name_input = document.getElementById("name_input")
const date_input = document.getElementById("date_input")
const time_input = document.getElementById("time_input")
const hour_input = document.getElementById("hour_input")
const mins_input = document.getElementById("mins_input")
const alertDiv = document.getElementById("alertDiv")
const alert_p = document.getElementById("alert")
const introductory_div = document.getElementById("introductory_div")
const book_session_div = document.getElementById("book_session_div")
const view_invoice_div = document.getElementById("view_invoice_div")
const previous_sessions_div = document.getElementById("previous_sessions_div")
const confirm_booking_div = document.getElementById("confirm_booking_div")
const message_span = document.getElementById("message_span")
const messagesDiv = document.getElementById("messagesDiv")
const message = document.getElementById("message")
const booked_sessions_div = document.getElementById("booked_sessions_div")


function book_session(){
  alertDiv.style.display = "none"
  name = name_input.value
  date = date_input.value
  words_date = new Date(date)
  words_date_arr = words_date.toDateString().split(" ")
  words_date = words_date_arr[2] + " " + words_date_arr[1] + " " + words_date_arr[3]
  time = time_input.value
  hour = hour_input.value
  mins = mins_input.value
  today = new Date()
  entered_date = new Date(date)
  // console.log(name,date,time,hour,mins)

  if (name==""){
    alertDiv.style.display = "block";
    alert_p.innerHTML = "Please enter a name";
  }else if (date == ""){
    alertDiv.style.display = "block";
    alert_p.innerHTML = "Please enter a date";
  }else if (time > "20:00" || time < "08:00"){
    alertDiv.style.display = "block";
    alert_p.innerHTML = "Please enter a time between 08:00 and 20:00. If you would like to book a session outside of these times, please contact me directly on Josh@68duck.co.uk";
  }else if(entered_date<today){
    alertDiv.style.display = "block";
    alert_p.innerHTML = "Please enter a date that is after today";
  }else{
    alertDiv.style.display = "none";
    introductory_div.style.display="none"
    book_session_div.style.display="none"
    previous_sessions_div.style.display="none"
    view_invoice_div.style.display="none"
    booked_sessions_div.style.display="none"
    confirm_booking_div.style.display="block"
    message_span.innerHTML = "Are you sure you would like to request a session for " + name + " at " + time + " on " + words_date + " for " + hour + " hour(s) " + " and " + mins + " mins?"
  }
}

function yes_pressed(){
  alertDiv.style.display = "none";
  introductory_div.style.display="block"
  book_session_div.style.display="block"
  previous_sessions_div.style.display="block"
  view_invoice_div.style.display="block"
  booked_sessions_div.style.display="block"
  confirm_booking_div.style.display="none"
  messagesDiv.style.display = "block"
  message.innerHTML = "Booking requested"
  request_booking(name,date,time,hour,mins,words_date)
}


const request_booking = async (name,date,time,hour,mins,words_date) => {
   const url = '/request_booking'; // the URL to send the HTTP request to
   var content = {
     "name":name,
     "date":date,
     "time":time,
     "hour":hour,
     "mins":mins,
     "words_date":words_date,
     "email":email,  //global defined in html
     "full_name":full_name //global defined in html
   }
   const body = JSON.stringify(content); // whatever you want to send in the body of the HTTP request
   const headers = {'Content-Type': 'application/json'}; // if you're sending JSON to the server
   const method = 'POST';
   const response = await fetch(url, { method, body, headers });
   const data = await response.text(); // or response.json() if your server returns JSON
   if (data == "All OK"){

   }else{
     alert(data)
   }
}

function no_pressed(){
  alertDiv.style.display = "block";
  alert_p.innerHTML = "Booking cancled"
  introductory_div.style.display="block"
  book_session_div.style.display="block"
  previous_sessions_div.style.display="block"
  view_invoice_div.style.display="block"
  booked_sessions_div.style.display="block"
  confirm_booking_div.style.display="none"
}

function request_invoice_pressed(){
  // request_invoice()
  window.open("/view_invoice/"+full_name+"/"+email)
}

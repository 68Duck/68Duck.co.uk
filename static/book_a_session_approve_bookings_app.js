const table = document.getElementById("table")
const table2 = document.getElementById("table2")


function getTableInformation (table_name){
  var table = document.getElementById(table_name)
  var tableHTML = table.outerHTML
  var rows = new Array()
  // console.log(table)
  table.querySelectorAll("tbody").forEach(tbody =>{
    tbody.querySelectorAll("tr").forEach(tr =>{
      var row = new Array()
      tr.querySelectorAll("td").forEach(item =>{
        if (item.innerHTML.substring(0,6) == "<input") {
          if (item.innerHTML.substring(13,21)=="checkbox"){
            item.querySelectorAll("input").forEach(input =>{
              row.push(input.checked)
            })
          }else if (item.innerHTML.substring(13,19)=="number"){
            item.querySelectorAll("input").forEach(input =>{
              row.push(input.value)
            })
          }
        } else{

          row.push(item.innerHTML)
        }
        // console.log(item.innerHTML)
      })
      rows.push(row)
    })
  })
  return rows
}

function submit_pressed(){
  update_approved_bookings(getTableInformation("table"),true)
  window.location.reload()
}

function update_pressed(){
  update_approved_bookings(getTableInformation("table2"),false)
  window.location.reload()
}

function update2_pressed(){
  update_approved_bookings(getTableInformation("table3"),false)
  window.location.reload()
}

const update_approved_bookings = async (table_information,send_email) => {
   const url = '/update_approved_bookings'; // the URL to send the HTTP request to
   const content = {
     "table_information":table_information,
     "send_email":send_email
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

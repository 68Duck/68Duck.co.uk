table = document.getElementById("table")

function change_made(){
  data = []
  inputs = document.querySelectorAll(".input")
  for (var i=0;i<inputs.length;i++){
    input = inputs[i]
    data.push(input.checked)
    // console.log(input.checked)
    // if (input.value == "on"){
    //   data.push(1)
    // }else{
    //   data.push(0)
    // }
  }
  // for (var i=0,row;row=table.rows[i];i++){
  //   // for (var j=0,col;col=table.rows[j];j++){
  //     var toggle = row.querySelectorAll(".switch_table_item")
  //     if (toggle.length != 0){
  //       td = toggle[0]
  //       label = td.querySelectorAll(".switch")
  //       input = label.querySelectorAll(".input")
  //       data.push(input.value)
  //       console.log(input.checked)
  //     }else{
  //       data.push(null)
  //     }
  //
  // }
  // alert(data)

  send_data(data)
}

const send_data = async (data) => {
  const url = '/slst_changes_made'; // the URL to send the HTTP request to
  const body = JSON.stringify(data); // whatever you want to send in the body of the HTTP request
  const headers = {'Content-Type': 'application/json'}; // if you're sending JSON to the server
  const method = 'POST';
  const response = await fetch(url, { method, body, headers });
}

function exportTableToExcel(tableID, filename = '') {
    var downloadLink;
    var dataType = 'application/vnd.ms-excel';
    var tableSelect = document.getElementById(tableID);
    var tableHTML = tableSelect.outerHTML.replace(/ /g, '%20');

    // Specify file name
    filename = filename ? filename + '.xls' : 'excel_data.xls';

    // Create download link element
    downloadLink = document.createElement("a");

    document.body.appendChild(downloadLink);

    if (navigator.msSaveOrOpenBlob) {
        var blob = new Blob(['\ufeff', tableHTML], {
            type: dataType
        });
        navigator.msSaveOrOpenBlob(blob, filename);
    } else {
        // Create a link to the file
        downloadLink.href = 'data:' + dataType + ', ' + tableHTML;
        // Setting the file name
        downloadLink.download = filename;

        //triggering the function
        downloadLink.click();
    }
}


var tableToExcel = (function() {
  var uri = 'data:application/vnd.ms-excel;base64,'
    , template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--><meta http-equiv="content-type" content="text/plain; charset=UTF-8"/></head><body><table>{table}</table></body></html>'
    , base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))) }
    , format = function(s, c) { return s.replace(/{(\w+)}/g, function(m, p) { return c[p]; }) }
  return function(table, name) {
    if (!table.nodeType) table = document.getElementById(table)
    var ctx = {worksheet: name || 'Worksheet', table: table.innerHTML}
    window.location.href = uri + base64(format(template, ctx))
  }
})()

//
// function tableItemClicked() {
//
// }
// $(function(){
//   $("td").click(function(event){
//     if($(this).children("input").length > 0)
//           return false;
//
//     var tdObj = $(this);
//     var preText = tdObj.html();
//     var inputObj = $("<input type='text' />");
//     tdObj.html("");
//
//     inputObj.width(tdObj.width())
//             .height(tdObj.height())
//             .css({border:"0px",fontSize:"17px"})
//             .val(preText)
//             .appendTo(tdObj)
//             .trigger("focus")
//             .trigger("select");
//
//     inputObj.keyup(function(event){
//       if(13 == event.which) { // press ENTER-key
//         var text = $(this).val();
//         tdObj.html(text);
//       }
//       else if(27 == event.which) {  // press ESC-key
//         tdObj.html(preText);
//       }
//     });
//
//     inputObj.click(function(){
//       return false;
//     });
//   });
// });

// getTableInformation();
// fetch("/")
//   .then(function getTableInformation () {
//     var table = document.getElementById("table")
//     var tableHTML = table.outerHTML
//     var rows = new Array()
//     // console.log(table)
//     table.querySelectorAll("tbody").forEach(tbody =>{
//       tbody.querySelectorAll("tr").forEach(tr =>{
//         var row = new Array()
//         tr.querySelectorAll("td").forEach(item =>{
//           row.push(item.innerHTML)
//           // console.log(item.innerHTML)
//         })
//         rows.push(row)
//       })
//     })
//     console.log(rows)
//     return rows
//   }).then(function (text) {
//           console.log('GET response:');
//           console.log(text);
//           return text
//       });

function addTableRow(){
  var table = document.getElementById("table")
  var tbody = table.querySelector("tbody")
  var count = 0
  var rowsCount = 1   // as the id starts at one


  var tr = tbody.querySelector("tr")
  tbody.querySelectorAll("tr").forEach(tr =>{
    rowsCount++
  })
  if (tr == null) {
    var count = 1
    console.log(count)
  }else{
    tr.querySelectorAll("td").forEach(td =>{
      count++
    })
  }

  newRow = document.createElement("tr")
  for (var i=0;i<count;i++){
    newElement = document.createElement("td")
    if (i==0){
      newElement.innerHTML = rowsCount
    }
    newElement.setAttribute("contenteditable","true")
    newElement.setAttribute("name","tableItem")
    newElement.setAttribute("class",".tableItem")
    newRow.appendChild(newElement)
  }
  tbody.appendChild(newRow)
  sendPost()
  window.location.reload()
}

const sendPost = async () => {
   const url = '/tableUpdate'; // the URL to send the HTTP request to
   const body = JSON.stringify(getTableInformation()); // whatever you want to send in the body of the HTTP request
   const headers = {'Content-Type': 'application/json'}; // if you're sending JSON to the server
   const method = 'POST';
   const response = await fetch(url, { method, body, headers });
   const data = await response.text(); // or response.json() if your server returns JSON
   // console.log(data);
}

const searchTable = async () => {
   const url = '/searchTable'; // the URL to send the HTTP request to
   const body = JSON.stringify(getTableSearch()); // whatever you want to send in the body of the HTTP request
   const headers = {'Content-Type': 'application/json'}; // if you're sending JSON to the server
   const method = 'POST';
   const response = await fetch(url, { method, body, headers });
   const data = await response.text(); // or response.json() if your server returns JSON
   // console.log(data);
   window.location.reload()
}

function getTableSearch() {
  var searchColumnName = document.getElementById("searchColumnName")
  var searchInput = document.getElementById("searchInput")
  columnName = searchColumnName.value
  searchValue = searchInput.value
  var jsonObject = {"columnName":columnName,"searchValue":searchValue};
  return jsonObject
}

getTableSearch()

function getTableInformation (){
  var table = document.getElementById("table")
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
          }else if (item.innerHTML.substring(13,17)=="date") {
            item.querySelectorAll("input").forEach(input =>{
              if (input.valueAsDate == null){
                row.push(input.valueAsDate)
              }else{
                var date = input.valueAsDate
                var d = new Date(date),
                month = '' + (d.getMonth() + 1),
                day = '' + d.getDate(),
                year = d.getFullYear();

                if (month.length < 2)
                    month = '0' + month;
                if (day.length < 2)
                    day = '0' + day;
                row.push([year,month,day].join("-"))
              }
            })
          }else if (item.innerHTML.substring(13,17)=="time"){
            item.querySelectorAll("input").forEach(input =>{
              row.push(input.value)
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


$(document).on('input','#table > tbody > tr > td',function(){
  sendPost()
  clearCalcsTable()
  createCalcsTable()
})

function logTest(){
  console.log("test")
}

// var fileInput = document.getElementById("fileInput")
// fileInput.addEventListener("change",fileInputed)
const reader = new FileReader()

function fileInputed(e) {
  if (e!=false){
    fileTarget = e.target
    var fileList = fileTarget.files;
    reader.addEventListener("load",(e) => {
      console.log(e.target.result)
      var lines = e.target.result.split(newLine)
      lines.forEach((line) => {
        console.log(line)
      })
    })
  }else{
    alert("The file was not valid. Please try again")
  }
  reader.readAsText(fileList[0])
}



function Upload() {
    //Reference the FileUpload element.
    var fileUpload = document.getElementById("fileInput");

    //Validate whether File is valid Excel file.
    var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.xls|.xlsx)$/;
    if (regex.test(fileUpload.value.toLowerCase())) {
        if (typeof (FileReader) != "undefined") {
            var reader = new FileReader();

            //For Browsers other than IE.
            if (reader.readAsBinaryString) {
                reader.onload = function (e) {
                    ProcessExcel(e.target.result);
                };
                reader.readAsBinaryString(fileUpload.files[0]);
            } else {
                //For IE Browser.
                reader.onload = function (e) {
                    var data = "";
                    var bytes = new Uint8Array(e.target.result);
                    for (var i = 0; i < bytes.byteLength; i++) {
                        data += String.fromCharCode(bytes[i]);
                    }
                    ProcessExcel(data);
                };
                reader.readAsArrayBuffer(fileUpload.files[0]);
            }
        } else {
            alert("This browser does not support HTML5.");
        }
    } else {
        alert("Please upload a valid Excel file.");
    }
};
async function ProcessExcel(data) {
    //Read the Excel File data.
    var workbook = XLSX.read(data, {
        type: 'binary'
    });

    //Fetch the name of First Sheet.
    var firstSheet = workbook.SheetNames[0];

    //Read all rows from First Sheet into an JSON array.
    var excelRows = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[firstSheet]);
    openExcelFile(excelRows)
    // window.location.reload()
}

const openExcelFile = async (excelRows) => {
   const url = '/openExcelFile'; // the URL to send the HTTP request to
   const body = JSON.stringify(excelRows); // whatever you want to send in the body of the HTTP request
   const headers = {'Content-Type': 'application/json'}; // if you're sending JSON to the server
   const method = 'POST';
   const response = await fetch(url, { method, body, headers });
   const data = await response.text(); // or response.json() if your server returns JSON
   // console.log(data);
   window.location.reload()
}

const openDatabaseTable = async (tableName) => {
  const url = '/openTable'; // the URL to send the HTTP request to
  const body = JSON.stringify(tableName); // whatever you want to send in the body of the HTTP request
  const headers = {'Content-Type': 'application/json'}; // if you're sending JSON to the server
  const method = 'POST';
  const response = await fetch(url, { method, body, headers });
  const data = await response.text(); // or response.json() if your server returns JSON
  // console.log(data);
  window.location.reload()
}

function openTableFromDatabase() {
  var openTableName = document.getElementById("openTableName")
  var tableName = openTableName.value
  openDatabaseTable(tableName);
}

function test() {
  alert("test")
}

// addTableRow()

const saveTableRequest = async (tableName) => {
  const url = '/saveTable'; // the URL to send the HTTP request to
  const body = JSON.stringify(tableName); // whatever you want to send in the body of the HTTP request
  const headers = {'Content-Type': 'application/json'}; // if you're sending JSON to the server
  const method = 'POST';
  const response = await fetch(url, { method, body, headers });
  const data = await response.text(); // or response.json() if your server returns JSON
  // console.log(data);
  window.location.reload()
}

function saveTable() {
  var tableNameInput = document.getElementById("saveTableName")
  var tableName = tableNameInput.value
  saveTableRequest(tableName)
  window.onbeforeunload = function () {
        window.scrollTo(0, 0);
  }
}



const createTableRequest = async (information) => {
  const url = '/createNewTable'; // the URL to send the HTTP request to
  const body = JSON.stringify(information); // whatever you want to send in the body of the HTTP request
  const headers = {'Content-Type': 'application/json'}; // if you're sending JSON to the server
  const method = 'POST';
  const response = await fetch(url, { method, body, headers });
  const data = await response.text(); // or response.json() if your server returns JSON
  // console.log(data);
  window.location.reload()
}

function createNewTable(){
  columns = new Array()
  var tableName = document.getElementById("createTableNameInput").value
  columns.push(tableName)
  var tableColumns = document.querySelectorAll(".newColumnInput").forEach((item, i) => {
    columns.push(item.value)
  });
  createTableRequest(columns)

}

const deleteTableRequest = async (tableName) => {
  const url = '/deleteTable'; // the URL to send the HTTP request to
  const body = JSON.stringify(tableName); // whatever you want to send in the body of the HTTP request
  const headers = {'Content-Type': 'application/json'}; // if you're sending JSON to the server
  const method = 'POST';
  const response = await fetch(url, { method, body, headers });
  const data = await response.text(); // or response.json() if your server returns JSON
  // console.log(data);
  window.location.reload()
}


function deleteTableFromDatabase(){
  if (confirm("Are you sure you want to delete the table?")){
    var deleteTableName = document.getElementById("deleteTableName")
    var tableName = deleteTableName.value
    deleteTableRequest(tableName)
  }else{
    //do nothing if cancel is pressed
  }
}

function clearCalcsTable(){
  var tbody = calcs.querySelector("tbody")
  var thead = calcs.querySelector("thead")
  tbody.querySelectorAll('*').forEach(child => child.remove());
  thead.querySelectorAll('*').forEach(child => child.remove());
}

function createCalcsTable(){
  var tableInformation = getTableInformation()
  var calcs = document.getElementById("calcs")
  var tbody = calcs.querySelector("tbody")
  var thead = calcs.querySelector("thead")
  var headers = ["Total","Total paid","Amount to pay"]
  var tr = document.createElement("tr")
  for (var i=0;i<headers.length;i++){
    newElement = document.createElement("th")
    newElement.innerHTML = headers[i]
    newElement.setAttribute("contenteditable","true")
    newElement.setAttribute("name","tableItem")
    newElement.setAttribute("class",".tableItem")
    tr.appendChild(newElement)
  }
  thead.appendChild(tr)
  var total = 0
  var ptotal = 0  // paid total
  var nptotal = 0 // not paid total
  for (var i=0;i<tableInformation.length;i++){
    total = total + parseFloat(tableInformation[i][3])
    if (tableInformation[i][4] == true){
      ptotal = ptotal + parseFloat(tableInformation[i][3])
    }else{
      nptotal = nptotal + parseFloat(tableInformation[i][3])
    }
  }
  newRow = document.createElement("tr")
  totals = [total,ptotal,nptotal]  //needs to be in the same order as the headers
  for (var i=0;i<totals.length;i++){
    newElement = document.createElement("th")
    newElement.setAttribute("contenteditable","true")
    newElement.setAttribute("name","tableItem")
    newElement.setAttribute("class",".tableItem")
    newElement.innerHTML = totals[i].toFixed(2) //round to 2dp
    newRow.appendChild(newElement)
  }
  tbody.appendChild(newRow)
}

function main(){
  createCalcsTable()
}

main()

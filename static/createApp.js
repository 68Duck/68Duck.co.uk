var termsAndDeffinitionsBox = document.querySelector(".termsAndDeffinitionsBox")
var termsAndDeffinitionsInputs = document.querySelector(".termsAndDeffinitionsInputs")
var addTermBtn = document.getElementById("addTermBtn")
var copyButton = document.getElementById("copyButton")
var textToCopy = document.getElementById("textToCopy")
var newTermSplitType1 = document.getElementById("doubleSlashTermSplit")
var newTermSplitType2 = document.getElementById("commaTermSplit")
var newTermSplitType3 = document.getElementById("customTermSplit")
var newLineType1 = document.getElementById("newLine")
var newLineType2 = document.getElementById("semicolonNewLine")
var newLineType3 = document.getElementById("customNewLine")



termCount = 0
addTerm()
textToCopy.innerHTML = "Type in some terms and this will become the file."
addTermBtn.addEventListener("click",addTerm)
copyButton.addEventListener("click",copyText)
newTermSplitType1.addEventListener("change",newTermSplitInputed)
newTermSplitType2.addEventListener("change",newTermSplitInputed)
newTermSplitType3.addEventListener("change",newTermSplitInputed)
newLineType1.addEventListener("change",newLineTypeInputed)
newLineType2.addEventListener("change",newLineTypeInputed)
newLineType3.addEventListener("change",newLineTypeInputed)
// customNewLineInput.addEventListener("change",newLineTypeInputed)
newLine = "<br/>"
termSplit = "//"

function newLineTypeInputed(e){
  if (e.target.id == "newLine"){
    // console.log("newLine")
    newLine = "<br/>"

  }else if(e.target.id == "semicolonNewLine"){
    // console.log("semicolon")
    newLine = ";"

  }else{
    // console.log("custom")
    newLine = customNewLineInput.value
    // console.log(newLine)

  }
  changeTextToCopy()
}

function newTermSplitInputed(e){
  if (e.target.id == "doubleSlashTermSplit"){
    // console.log("newLine")
    termSplit = "//"
  }else if(e.target.id == "commaTermSplit"){
    // console.log("semicolon")
    termSplit = ","
  }else{
    // console.log("custom")
    termSplit = customTermSplitInput.value
    // console.log(newLine)
  }
  changeTextToCopy()
}

function changeTextToCopy(){
  // console.log("changeme")
  questionsAndAnswersDivs = termsAndDeffinitionsInputs.querySelectorAll(".termDisplay")
  questionsAndAnswers = []
  finalText = ""
  for (var i=0;i<questionsAndAnswersDivs.length;i++){
    questionsAndAnswers.push(questionsAndAnswersDivs[i].value)
    finalText = finalText + questionsAndAnswersDivs[i].value
    if (i%2==0){
      finalText = finalText + termSplit
    }else{
      finalText = finalText + newLine
    }
  }
  // console.log(questionsAndAnswers)
  // console.log(finalText)
  textToCopy.innerHTML = finalText

}

function addTerm(){
  newQuestion = document.createElement("input")
  newAnswer = document.createElement("input")
  newQuestionNumber = document.createElement("div")
  termCount++
  newQuestionNumber.innerHTML = termCount + "."
  newQuestion.setAttribute("placeholder","Enter the prompt")
  newAnswer.setAttribute("placeholder","Enter the answer")
  newQuestion.setAttribute("oninput","changeTextToCopy()")
  newAnswer.setAttribute("oninput","changeTextToCopy()")
  // newQuestion.innerHTML = "Enter the prompt"
  // newAnswer.innerHTML = "Enter the answer"
  newQuestion.style.setProperty("--height",(newQuestion.innerHTML.length)/2+20+"px")
  newAnswer.style.setProperty("--height",(newAnswer.innerHTML.length)/2+20+"px")
  newQuestion.classList.add("termDisplay")
  newAnswer.classList.add("termDisplay")
  newQuestionNumber.classList.add("questionNumberDisplay")
  termsAndDeffinitionsInputs.appendChild(newQuestionNumber)
  termsAndDeffinitionsInputs.appendChild(newQuestion)
  termsAndDeffinitionsInputs.appendChild(newAnswer)
}

function copyText(){
  // var textToCopy = document.getElementById("textToCopy")
  // copyText.setSelectionRange(0,999999)  //for mobile devices
  var range = document.createRange();   //copied from stack overflow
  range.selectNode(document.getElementById("textToCopy"));
  window.getSelection().removeAllRanges(); // clear current selection
  window.getSelection().addRange(range); // to select text
  document.execCommand("copy");
  window.getSelection().removeAllRanges();// to deselect
  alert("Text Coppied to Clipboard")
}

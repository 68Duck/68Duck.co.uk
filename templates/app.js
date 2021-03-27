var fileSelector = document.getElementById("fileInput")
var textInput = document.getElementById("textInput")
var answerInput = document.getElementById("answer")
var saveButton = document.getElementById("saveButton")
var img = document.getElementById("image")
var question = document.getElementById("question")
var submitButton = document.getElementById("submitAnswer")
var questionContainer = document.getElementById("questionContainer")
var nextButton = document.querySelector(".nextBtn")
var startButton = document.getElementById("startBtn")
var prompt = document.getElementById("prompt")
var fileQuestions = document.getElementById("fileQuestions")
var fileAnswers = document.getElementById("fileAnswers")
var fileContents = document.getElementById("fileContents")
var fileInputDiv = document.getElementById('fileInputDiv')
var answerChangeDisplay = document.getElementById("answerChangeDisplay")
var correctAnswerDisplay = document.getElementById("correctAnswerDisplay")
var gapFill = document.getElementById("gapFill")
var gapFillContainer = document.getElementById("gapFillContainer")
var promptGapFill = document.getElementById("promptGapFill")
var submitButtonGapFill = document.getElementById("submitAnswerGapFill")
var nextButtonGapFill = document.querySelector(".nextBtnGapFill")
var newLineType1 = document.getElementById("newLine")
var newLineType2 = document.getElementById("semicolonNewLine")
var newLineType3 = document.getElementById("customNewLine")
var customNewLineInput = document.getElementById("customNewLineInput")
var newTermSplitType1 = document.getElementById("doubleSlashTermSplit")
var newTermSplitType2 = document.getElementById("commaTermSplit")
var newTermSplitType3 = document.getElementById("customTermSplit")
var customTermSplitInput = document.getElementById("customTermSplitInput")
var fileInformation = document.getElementById('fileInformation')
var startSelectionScreenContainer = document.getElementById("startSelectionScreenContainer")
var questionTypeInput1 = document.getElementById("CopyType")
var questionTypeInput2 = document.getElementById("GapFill1")
var questionTypeInput3 = document.getElementById("GapFill2")
var questionTypeInput4 = document.getElementById("ShuffleQuestion")
var questionTypeInput5 = document.getElementById("MemoryQuestion")
var selectAll = document.getElementById("SelectAll")
var startButton2 = document.getElementById("startBtn2")
var individualQuestionOrder = document.getElementById("individualQuestion")
var wholeQuestionSetOrder = document.getElementById("wholeQuestionSet")
var allQuestionsRange = document.getElementById("allQuestionsRange")
var startAtQuestionRange = document.getElementById("startAtQuestionRange")
var startAtARangeInput = document.getElementById("startAtARangeInput")
var overruleButton = document.getElementById("overruleBtn")
var overruleButtonGapFill = document.getElementById("overruleBtnGapFill")
// var customRange = document.getElementById("customRange")
// var customRangeInput = document.getElementById("customRangeInput")

var gapFillInputList = new Array()
var correctAnswersGapFill = new Array()

var isCorrect = false;
var inidividualQuestionMode = true;
var currentQuestionTypeArrayPos = 0;
var selectedQuestionTypes = new Array()
var fileTarget;
var isFileInputed = false;
var newLine = "\n"
var termSplit = "//"
const reader = new FileReader();
var questionsArray = new Array();
var qArray = new Array(); //question not answer
var aArray = new Array();  //answer array
var shuffledQuestions = new Array();
var shuffledAnswers = new Array();
var questionNumber = 0;
var questionType = 0;
var type = 0;
var questionsDisplay;
var answersDisplay;
var currentQuestion;
var currentAnswer
startButton.addEventListener("click",startButtonClicked)
fileSelector.addEventListener("change",fileInputed)
newLineType1.addEventListener("change",newLineTypeInputed)
newLineType2.addEventListener("change",newLineTypeInputed)
newLineType3.addEventListener("change",newLineTypeInputed)
newTermSplitType1.addEventListener("change",newTermSplitInputed)
newTermSplitType2.addEventListener("change",newTermSplitInputed)
newTermSplitType3.addEventListener("change",newTermSplitInputed)
// start()
// startSelectionScreen()   //REMOVE ME

function returnToStart() {
  fileInputDiv.classList.remove("hide")
  fileInformation.classList.remove("hide")
  questionNumber = 0
  currentQuestionTypeArrayPos = 0
  fileInputed(false)
}


function startButtonClicked(){
  if (questionsArray[0]!=null && questionsArray[0]!=undefined){
    fileInputDiv.classList.add("hide")
    fileInformation.classList.add("hide")
    startSelectionScreen()
  }else{
    alert("Please choose a file")
  }
}
function startButton2Clicked(){
  if (questionTypeInput1.checked==true || questionTypeInput2.checked==true || questionTypeInput3.checked==true || questionTypeInput4.checked==true || questionTypeInput5.checked==true){
    if (allQuestionsRange.checked==true){}//dont do anything as default
    if (startAtQuestionRange.checked==true){
      var numberToStartAt = Number(startAtARangeInput.value)
      // console.log(numberToStartAt)
      // console.log(startAtARangeInput.value)
      // console.log(Number.isInteger(numberToStartAt))
      if (Number.isInteger(numberToStartAt)==true){
        if (numberToStartAt <= qArray.length){
          for (var i=0;i<numberToStartAt-1;i++){
            qArray.shift()
            aArray.shift()
          }
        }else{
          alert("There are not that many questions. Please try again")
          return;
        }
      }else{
        alert("The range you inputed is not an integer. Please try again")
        return;
      }
    }
    startSelectionScreenContainer.classList.add("hide")
    if (questionTypeInput1.checked==true){selectedQuestionTypes.push(0)}
    if (questionTypeInput2.checked==true){selectedQuestionTypes.push(1)}
    if (questionTypeInput3.checked==true){selectedQuestionTypes.push(2)}
    if (questionTypeInput4.checked==true){selectedQuestionTypes.push(3)}
    if (questionTypeInput5.checked==true){selectedQuestionTypes.push(4)}
    // console.log(selectedQuestionTypes)
    start()
  }else{
    alert("Please select at least one type of question")
  }

}

function startSelectionScreen(){
  fileInputDiv.classList.add("hide")
  fileInformation.classList.add("hide")
  startSelectionScreenContainer.classList.remove("hide")
  selectAll.addEventListener("change",selectAllClicked)
  questionTypeInput1.addEventListener("change",questionTypeInputClicked)
  questionTypeInput2.addEventListener("change",questionTypeInputClicked)
  questionTypeInput3.addEventListener("change",questionTypeInputClicked)
  questionTypeInput4.addEventListener("change",questionTypeInputClicked)
  questionTypeInput5.addEventListener("change",questionTypeInputClicked)
  startButton2.addEventListener("click",startButton2Clicked)
  individualQuestionOrder.addEventListener("click",orderTypeClicked)
  wholeQuestionSetOrder.addEventListener("click",orderTypeClicked)
}

function questionTypeInputClicked(e){
  if (e.target.checked==false){
    selectAll.checked = false
  }
  var allSelected = false
  if (questionTypeInput1.checked==true && questionTypeInput2.checked==true && questionTypeInput3.checked==true && questionTypeInput4.checked==true && questionTypeInput5.checked==true){
    selectAll.checked=true
  }
}

function selectAllClicked(e){
  // console.log(e.target)
  // console.log(e.target.checked)
  if (e.target.checked==true){
    questionTypeInput1.checked = true
    questionTypeInput2.checked = true
    questionTypeInput3.checked = true
    questionTypeInput4.checked = true
    questionTypeInput5.checked = true
  } else{
    questionTypeInput1.checked = false
    questionTypeInput2.checked = false
    questionTypeInput3.checked = false
    questionTypeInput4.checked = false
    questionTypeInput5.checked = false
  }
}

function orderTypeClicked(e){
  if (e.target.checked==true){
    if (e.target.id=="individualQuestion"){
      inidividualQuestionMode = true;
    }else{
      inidividualQuestionMode = false;
    }
  }
}

function overruleButtonClicked(){
  if (isCorrect == true){
    isCorrect = false
  }else{
    isCorrect = true;
  }
  questionContainer.classList.add("green-glow")
  questionContainer.classList.remove("red-glow")
  gapFillContainer.classList.add("green-glow")
  gapFillContainer.classList.remove("red-glow")
  overruleButton.classList.add("hide")
  overruleButtonGapFill.classList.add("hide")
  // nextButtonClicked()
}

function start(){
  // saveButton.addEventListener("click",saveFile)
  questionContainer.classList.remove("hide")
  document.addEventListener("keydown",logKey)
  submitButton.addEventListener("click",checkIfCorrect)
  submitButtonGapFill.addEventListener("click",checkIfCorrectGapFill)
  nextButton.addEventListener("click",nextButtonClicked)
  nextButtonGapFill.addEventListener("click",nextButtonClicked)
  overruleButton.addEventListener("click",overruleButtonClicked)
  overruleButtonGapFill.addEventListener("click",overruleButtonClicked)
  if (qArray.length == aArray.length){
    shuffledArrays = new Array()
    var tempQ = new Array()
    var tempA = new Array()
    for (var i=0;i<qArray.length;i++){
      tempQ[i] = qArray[i]
      tempA[i] = aArray[i]
    }
    shuffledArrays = shuffleBothArrays(qArray,aArray)
    qArray = tempQ
    aArray = tempA
    shuffledQuestions = shuffledArrays[0]
    shuffledAnswers = shuffledArrays[1]
  }
  nextQuestion()
}

function logKey(e){
  if (e.code == "Enter"){
    if (questionContainer.classList.contains("hide") == false){
      if (nextButton.classList.contains("hide")){
        checkIfCorrect()
      }else{
        nextButtonClicked()
      }
    }else if (gapFillContainer.classList.contains("hide") == false){
      if (nextButtonGapFill.classList.contains("hide")){
        checkIfCorrectGapFill()
      }else{
        nextButtonClicked()
      }
    }
  }
}

function nextButtonClicked(){
  answerInput.value = ""
  if (isCorrect == true){
    nextQuestion()
    isCorrect = false;
  }else{
    repeatQuestion()
  }
}

function repeatQuestion(){
  overruleButton.classList.add("hide")
  overruleButtonGapFill.classList.add("hide")
  nextButton.classList.add("hide")
  nextButtonGapFill.classList.add("hide")
  questionContainer.classList.remove("green-glow")
  questionContainer.classList.remove("red-glow")
  gapFillContainer.classList.remove("green-glow")
  gapFillContainer.classList.remove("red-glow")
  switch (questionType) {
    case 0:
      // console.log(0)
      copyQuestionType();
      break;
    case 1:
      // console.log(1)
      gapFillQuestion(0);
      type = 0;
      break;
    case 2:
      // console.log(2)
      gapFillQuestion(1);
      type = 1;
      questionType = 2;
      break;
    case 3:
      // console.log(3)
      shuffleQuestionType();
      break;
    case 4:
      // console.log(4)
      writeFromMemory();
      break;
  }
}

function nextQuestion(){
  nextButton.classList.add("hide")
  nextButtonGapFill.classList.add("hide")
  overruleButton.classList.add("hide")
  overruleButtonGapFill.classList.add("hide")
  questionContainer.classList.remove("green-glow")
  questionContainer.classList.remove("red-glow")
  gapFillContainer.classList.remove("green-glow")
  gapFillContainer.classList.remove("red-glow")
  if (inidividualQuestionMode==true){
    questionContainer.classList.add("hide")
    gapFillContainer.classList.add("hide")
    if (currentQuestionTypeArrayPos >= selectedQuestionTypes.length){
      currentQuestionTypeArrayPos = 0;
      questionNumber++;
    }
  }else{
    questionNumber++;
    if (questionNumber >= qArray.length){
      questionNumber = 0;
      currentQuestionTypeArrayPos++;
      questionContainer.classList.add("hide")
      gapFillContainer.classList.add("hide")
    }
  }
  // console.log(questionNumber)
  // console.log(selectedQuestionTypes,currentQuestionTypeArrayPos)
  if (currentQuestionTypeArrayPos<selectedQuestionTypes.length && questionNumber<qArray.length){
    if (inidividualQuestionMode==true){
      questionType = selectedQuestionTypes[currentQuestionTypeArrayPos]
      // console.log(currentQuestionTypeArrayPos)
      currentQuestionTypeArrayPos++;
    }else{
      questionType = selectedQuestionTypes[currentQuestionTypeArrayPos]
    }
    switch (questionType) {
      case 0:
        // console.log(0)
        copyQuestionType();
        break;
      case 1:
        // console.log(1)
        gapFillQuestion(0);
        type = 0;
        break;
      case 2:
        // console.log(2)
        gapFillQuestion(1);
        type = 1;
        questionType = 2;
        break;
      case 3:
        // console.log(3)
        shuffleQuestionType();
        break;
      case 4:
        // console.log(4)
        writeFromMemory();
        break;
    }
  }else{
    alert("Reached End Of Questions")
    returnToStart()
  }
}

function copyQuestionType(){
  questionType = 0
  questionContainer.classList.remove("hide")
  answerInput.removeAttribute("readonly")
  answerInput.classList.remove("hide")
  answerChangeDisplay.classList.add("hide")
  correctAnswerDisplay.classList.add("hide")
  question.innerHTML = qArray[questionNumber];
  prompt.innerHTML = aArray[questionNumber];
  currentQuestion = qArray[questionNumber]
  //   question.innerHTML = shuffledQuestions[questionNumber];
  //   prompt.innerHTML = shuffledAnswers[questionNumber];   //use these for unordered questions
}

function writeFromMemory(){
  questionContainer.classList.remove("hide")
  questionType = 4
  answerInput.removeAttribute("readonly")
  answerInput.classList.remove("hide")
  answerChangeDisplay.classList.add("hide")
  correctAnswerDisplay.classList.add("hide")
  question.innerHTML = "There is no prompt for this last one. Try to remember it on your own!"
  prompt.innerHTML = aArray[questionNumber];
  currentQuestion = qArray[questionNumber]
  //   question.innerHTML = shuffledQuestions[questionNumber];
  //   prompt.innerHTML = shuffledAnswers[questionNumber];   //use these for unordered questions
}

function shuffleQuestionType(){
  questionContainer.classList.remove("hide")
  questionType = 3
  answerInput.removeAttribute("readonly")
  answerInput.classList.remove("hide")
  answerChangeDisplay.classList.add("hide")
  correctAnswerDisplay.classList.add("hide")
  currentQuestion = qArray[questionNumber]
  currentAnswer = aArray[questionNumber]
  var currentQWords = new Array()
  currentQWords = currentQuestion.split(" ")
  currentShuffledQuestion = shuffleWords(currentQWords)
  question.innerHTML = currentShuffledQuestion;
  prompt.innerHTML = currentAnswer;

//   question.innerHTML = shuffledQuestions[questionNumber];
//   prompt.innerHTML = shuffledAnswers[questionNumber];
}

function gapFillQuestion(paramaterType){
  if (paramaterType != undefined && paramaterType != null){
    type = paramaterType
  }
  currentQuestion = qArray[questionNumber]
  // console.log(type,questionType)
  if (type == 0){
    questionType = 1
  }else if (type == 1){
    questionType = 2
  }
  // console.log(type,questionType)
  questionContainer.classList.add("hide")
  gapFillContainer.classList.remove("hide")
  // var type = 0;  //set to 1 for other type
  gapFill.querySelectorAll('*').forEach(child => child.remove());
  gapFillInputList = new Array()
  var currentQuestion = qArray[questionNumber];
  var currentAnswer = aArray[questionNumber];
  promptGapFill.innerHTML = currentAnswer;
  var currentQuestionWords = currentQuestion.split(" ")
  for (var i=0;i<currentQuestionWords.length-1;i++){
    // console.log(currentQuestionWords[i])
    // console.log(i%2==type, i)
    if (i%2==type){
      newWord = document.createElement("div");
      newWord.classList.add("gapFillWord")
      newWord.innerHTML = currentQuestionWords[i]
      gapFill.appendChild(newWord)
    }else{
      newGap = document.createElement("input")
      newGap.classList.add("gapFillInput")
      newGap.setAttribute("id","gap"+Math.floor(i/2))
      newGap.setAttribute("test",i)
      newCorrectGap = document.createElement("div")
      newCorrectGap.classList.add("correctGapDisplay")
      newCorrectGap.classList.add("hide")
      newCorrectGap.setAttribute("id","correctGap"+Math.floor(i/2))

      gapFill.appendChild(newGap)
      gapFill.appendChild(newCorrectGap)
      gapFillInputList[i] = (newGap)
      correctAnswersGapFill[i] = newCorrectGap
    }
  }
}

function checkIfCorrectGapFill(){  //CHANGE TYPE 1 TO SAME AS TYPE 0
  var correct = true;
  // var type = 0
  var currentQuestion = qArray[questionNumber];
  var currentAnswer = aArray[questionNumber];
  var currentQuestionWords = currentQuestion.split(" ")
  for (var i=0;i<currentQuestionWords.length;i++){
    if (i%2==type){
      if (type==1){

        var correctDisplay = ""
        for (var k=0;k<currentQuestionWords[i-1].length;k++){
          // console.log(i)
          // console.log(currentQuestionWords[i][k],gapFillInputList[i].value)
          if (gapFillInputList[i-1].value[k] != undefined){
            if (currentQuestionWords[i-1][k].toLowerCase() == gapFillInputList[i-1].value[k].toLowerCase()){
              correctDisplay = correctDisplay + "<span style='color: green'>"+ currentQuestionWords[i-1][k] + "</span>"
            }else{
              correctDisplay = correctDisplay + "<span style='color: red'>"+ currentQuestionWords[i-1][k] + "</span>"
              correct = false
            }

          }else{
            correctDisplay = correctDisplay + "<span style='color: red'>"+ currentQuestionWords[i-1][k] + "</span>"
            correct = false
          }
        }
        correctAnswersGapFill[i-1].innerHTML = correctDisplay
      }
    }else{
      if (type==0){
        var correctDisplay = ""
        if (currentQuestionWords[i] != undefined){
          for (var k=0;k<currentQuestionWords[i].length;k++){
            // console.log(gapFillInputList[i])
            // console.log(gapFillInputList)
            // console.log(i)
            if (gapFillInputList[i].value[k] != undefined){
              if (currentQuestionWords[i][k].toLowerCase() == gapFillInputList[i].value[k].toLowerCase()){
                correctDisplay = correctDisplay + "<span style='color: green'>"+ currentQuestionWords[i][k] + "</span>"
              }else{
                correctDisplay = correctDisplay + "<span style='color: red'>"+ currentQuestionWords[i][k] + "</span>"
                correct = false
              }

            }else{
              correctDisplay = correctDisplay + "<span style='color: red'>"+ currentQuestionWords[i][k] + "</span>"
              correct = false
            }
          }
          if (correctAnswersGapFill[i] != undefined){

            correctAnswersGapFill[i].innerHTML = correctDisplay
          }
        }
      }
    }
  }

  gapFill.querySelectorAll(".gapFillInput").forEach(gap => {
    gap.classList.add("hide")
  })
  gapFill.querySelectorAll(".correctGapDisplay").forEach(gap => gap.classList.remove("hide"))
  nextButtonGapFill.classList.remove("hide")
  overruleButtonGapFill.classList.remove("hide")
  if (correct == true){
    gapFillContainer.classList.add("green-glow")
    isCorrect = true
  }else{
    gapFillContainer.classList.add("red-glow")

  }
}


function checkIfCorrect(){
  if (questionType == 0 || questionType == 3 || questionType == 4){
    var answer = answerInput.value.toLowerCase()
    while (answer[0] == " "){
      answer = answer.slice(1)
    }
    while (answer[answer.length-1]==" "){
      answer = answer.slice(0,-1)
    }
    if (questionType == 0){
      var correctAnswer = question.innerHTML.toLowerCase()
      var correctAnswerCorrectCaps = question.innerHTML
    } else if (questionType == 3  || questionType == 4){
      var correctAnswer = currentQuestion.toLowerCase()
      var correctAnswerCorrectCaps = currentQuestion
    }
    while (correctAnswer[0] == " "){
      correctAnswer = correctAnswer.slice(1)
    }
    while (correctAnswer[correctAnswer.length-1]==" "){
      correctAnswer = correctAnswer.slice(0,-1)
    }
    if (correctAnswer == answer){
      questionContainer.classList.add("green-glow")
      isCorrect = true
      // answerElement.style.setProperty("--colour","#00ff00")
      // console.log("correct")
    } else{
      // console.log(correctAnswer)
      // console.log(answer)
      // console.log(question.innerHTML.toLowerCase())
      // console.log(answerInput.value.toLowerCase())
      questionContainer.classList.add("red-glow")
      var incorrectAnswer = answerInput.value.toLowerCase()
      // console.log(findDifferences(correctAnswer,incorrectAnswer))
      // console.log(findDifferences2(correctAnswer,incorrectAnswer))
      var differences = findDifferences(correctAnswer.toLowerCase(),answerInput.value.toLowerCase())
      var correctWords = findDifferences2(correctAnswer.toLowerCase(),incorrectAnswer.toLowerCase())
      answerInput.setAttribute("readonly","readonly")
      incorrectDisplay = new Array()
      for (var j=0;j<incorrectAnswer.length;j++){
        incorrectDisplay[j] = incorrectAnswer[j]
      }
      for (var i=0;i<differences.length;i++){
        // console.log(incorrectDisplay[differences[i]])
        if (incorrectDisplay[differences[i]] == undefined){
          incorrectDisplay[differences[i]] = " # "
        }
        incorrectDisplay[differences[i]] = "<span style='background-color: rgba(255,0,0,0.8)'>"+incorrectDisplay[differences[i]] + "</span>"
        // incorrectDisplay[differences[i]] = "A"
        // console.log(incorrectDisplay[differences[i]])
      }
      // console.log(incorrectDisplay)
      var incorrectDisplay2 = ""
      for (var k=0;k<incorrectDisplay.length;k++){
        incorrectDisplay2 = incorrectDisplay2 + incorrectDisplay[k]
      }
      var correctDisplay = ""
      for (var l=0;l<correctAnswer.length;l++){
        if (correctAnswer[l] == incorrectAnswer[l]){

          correctDisplay = correctDisplay + "<span style='color: green'>"+ correctAnswerCorrectCaps[l] + "</span>"
        }else{
          correctDisplay =  correctDisplay + "<span style='color: red'>"+ correctAnswerCorrectCaps[l] + "</span>"

        }

      }
      // console.log(incorrectDisplay2)
      // answerInput.value = incorrectDisplay2
      answerInput.classList.add("hide")
      answerChangeDisplay.classList.remove("hide")
      correctAnswerDisplay.classList.remove("hide")
      correctAnswerDisplay.innerHTML = correctDisplay
      answerChangeDisplay.innerHTML = incorrectDisplay2
      // answerElement.style.setProperty("--colour","#ff0000")
      // console.log("wrong")
    }
  }
  nextButton.classList.remove("hide")
  overruleButton.classList.remove("hide")
}


function saveFile(e) {
  var textToSave = textInput.value;
  var blob = new Blob([textToSave], {type :"text/plain;charset=utf-8" });
  saveAs(blob,"testtest.txt")
}

function findDifferences(txt1,txt2){
  if (txt1.length == txt2.length){
    if (txt1==txt2){
      return false;
    }else{
      differences = new Array();
      for (var i=0;i<txt1.length;i++){
        if (txt1[i]!=txt2[i]){
          differences.push(i);
        }
      }
      return differences;
    }
  }else{
    differences = new Array();
    for (var i=0;i<txt1.length;i++){
      if (txt1[i]!=txt2[i]){
        differences.push(i);
      }
    }
    return differences
    // return "different lengths";
  }
}

function findDifferences2(txt2,txt1){
  correct = new Array()
  var txt1Words = txt1.split(" ")
  var txt2Words = txt2.split(" ")
  // console.log(txt1Words)
  for (var j=0;j<txt1Words.length;j++){
    var word = txt1Words[j]
    // console.log(word)
    for (var i=0;i<txt2Words.length;i++){
      if (word == txt2Words[i]) {
        correct.push(word)
        break
      }
    }
  }
  return correct
}

function newLineTypeInputed(e){
  if (e.target.id == "newLine"){
    // console.log("newLine")
    newLine = "\n"
    if (isFileInputed==true){
      fileInputed(false);
    }
  }else if(e.target.id == "semicolonNewLine"){
    // console.log("semicolon")
    newLine = ";"
    if (isFileInputed==true){
      fileInputed(false);
    }
  }else{
    // console.log("custom")
    newLine = customNewLineInput.value
    // console.log(newLine)
    if (isFileInputed==true){
      fileInputed(false);
    }
  }
}

function newTermSplitInputed(e){
  if (e.target.id == "doubleSlashTermSplit"){
    // console.log("newLine")
    termSplit = "//"
    if (isFileInputed==true){
      fileInputed(false);
    }
  }else if(e.target.id == "commaTermSplit"){
    // console.log("semicolon")
    termSplit = ","
    if (isFileInputed==true){
      fileInputed(false);
    }
  }else{
    // console.log("custom")
    termSplit = customTermSplitInput.value
    // console.log(newLine)
    if (isFileInputed==true){
      fileInputed(false);
    }
  }
}

function fileInputed(e){
  if (e!=false){
    isFileInputed = true;
    fileTarget = e.target

  }else{
    fileTarget = fileTarget
  }
  for (var i=0;i<questionsArray.length;i++){
    qArray[i] = undefined
    aArray[i] = undefined
    questionsArray[i] = undefined
  }
  fileContents.querySelectorAll('*').forEach(child => child.remove());
  var fileList = fileTarget.files;
  // console.log(fileList)
  // console.log(fileList[0])

  reader.addEventListener("load",(e) => {

    // img.src = e.target.result;
    var test = e.target.result;
    var lines = test.split(newLine);
    for (var i=0;i<lines.length;i++){
      questionsArray[i] = []
      line = lines[i].split(termSplit)
      qArray[i] = line[0]
      // qArray[i] = qArray[i].slice(0,-1)  //should remove the last character // IF STOPS WORKING UNCOMMENT ME
      // console.log(qArray[i][qArray[i].length-1])
      aArray[i] = line[1]
      questionsArray[i][0] = line[0]
      questionsArray[i][1] = line[1]
    }
    // if (qArray.length == aArray.length){
    // }else{
    //   alert("Questions and answers are not the same length. Please try again")
    //   // return false;
    // }

    // console.log(lines.length)
    displayQuestionsAndAnswers(qArray,aArray);
    // fileQuestions.innerHTML = qArray;
    // fileAnswers.innerHTML = aArray;
    lines.forEach((line) => {
      // console.log(line)
    })
    // for (var i=0;i<lines.length;i++){
    //   console.log(lines[i])
    // }
    // console.log(test)
  })
  // reader.readAsDataURL(fileList[0])  //this if for images
  reader.readAsText(fileList[0])

}


function displayQuestionsAndAnswers(questions,answers){
  for (var i=0;i<questions.length;i++){  //answers and questions should always be same length
    newQuestion = document.createElement("div")
    newAnswer = document.createElement("div")
    newQuestion.innerHTML = questions[i]
    newAnswer.innerHTML = answers[i]
    newQuestion.style.setProperty("--height",(newQuestion.innerHTML.length)/2+20+"px")
    newAnswer.style.setProperty("--height",(newAnswer.innerHTML.length)/2+20+"px")
    newQuestion.classList.add("contentDisplay")
    newAnswer.classList.add("contentDisplay")
    fileContents.appendChild(newQuestion)
    fileContents.appendChild(newAnswer)
  }
}

function shuffle(array){
  var returningList = []
  while (array.length>0){
    var randNo = Math.floor(Math.random()*(array.length-1))
    returningList.push(array[randNo])
    array.splice(randNo,1)
  }
  return returningList

}

function shuffleBothArrays(array1,array2){
  var shuffled1 = new Array()
  var shuffled2 = new Array()
  while (array1.length>0){
    var randNo = Math.floor(Math.random()*(array1.length-1))
    shuffled1.push(array1[randNo])
    array1.splice(randNo,1)
    shuffled2.push(array2[randNo])
    array2.splice(randNo,1)
  }
  return [shuffled1,shuffled2]
}

function shuffleWords(array1){
  var shuffled1 = ""
  while (array1.length>0){
    var randNo = Math.floor(Math.random()*(array1.length-1))
    shuffled1 = shuffled1 + array1[randNo] + " "
    array1.splice(randNo,1)
  }
  return shuffled1
}

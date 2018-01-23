const OSC_JS = require('osc-js');
const remote = require('electron').remote;
const request = require('request');
const srv_port = 7007

const options = {
  open: { host: '192.168.1.255', port: srv_port },
  send: { host: '192.168.1.3', port: 7007 }
};
const osc = new OSC_JS({ plugin: new OSC_JS.DatagramPlugin(options) });
console.log('OSC: ', osc);

const listCount = 4; 

var current_status;
var gotQuestions; 


//HUNTER: JSON REQUEST LIST -- CHANGE THE RELATIVE PATH IF YOU NEED TO KEEP THE JSON EXTERNAL 
request('/json/frank.json', function (error, response, body) {
    console.log("Calling frank JSON");
    var frank = JSON.parse(body);
    console.log('error:', error);
    console.log('statusCode:', response && response.statusCode); 
    console.log('body:', frank); 

});

request('/json/funny.json', function(error, response, body){
    console.log("Calling funny JSON");
    var funny = JSON.parse(body);
    console.log('error:', error);
    console.log('statusCode:', response && response.statusCode); 
    console.log('body:', frank); 

});

request('/json/reddit.json', function(error, response, body){
    console.log("Calling funny JSON");
    var reddit = JSON.parse(body);
    console.log('error:', error);
    console.log('statusCode:', response && response.statusCode); 
    console.log('body:', frank); 
    console.log("Calling reddit JSON");
    var reddit = JSON.parse(body);
    console.log('error:', error);
    console.log('statusCode:', response && response.statusCode); 
    console.log('body:', frank); 
});

request('/json/fake.json', function(error, response, body){
    console.log("Calling fake JSON");
    var fake = JSON.parse(body);
    console.log('error:', error);
    console.log('statusCode:', response && response.statusCode); 
    console.log('body:', frank); 

});

request('/json/tellmemore.json', function(error, response, body){
    console.log("Calling reddit JSON");
    var reddit = JSON.parse(body);
    console.log('error:', error);
    console.log('statusCode:', response && response.statusCode); 
    console.log('body:', frank); 

});

// HUNTER -- END OF JSON REQUEST LIST


// Set host property for address other than localhost; eg. {host: 192.168.0.100, port: 7007}
// function createConnection() {
//  console.log('Open OSC Connection');
//  osc.open();
// }
var obj;

function closeConnection() {
  console.log('Close OSC Connection');
  osc.close();
}

function sendRefresh() {
  remote.getGlobal('sharedObject').questionSelected = '';
  document.getElementById('questions').innerHTML = 'Waiting for text...';
  const message = new OSC_JS.Message('/refresh', 1)
  const message1 = new OSC_JS.Message('/refresh', 1);
  const message2 = new OSC_JS.Message('/refresh', 1);
  console.log(message);
  osc.send(message);
  osc.send(message1);
  osc.send(message2);
}

// HUNTER -- THESE ARE NEW FUNCTIONS THAT GET TEXT FROM  JSON FILES FOR AI STATEMENTS.
// THIS SHOULD FUNCTION EXACTLY LIKE refreshQuestions() EXCEPT THAT IT PULLS FROM JSON. 

function sendFrank() {
  remote.getGlobal('sharedObject').questionSelected = ""
  state = remote.getGlobal('sharedObject').state;
  for(var i=0; i<listCount; i++) {
     addQuestion(frank[state][i], i); //frank has 48
  }
 addOpenSubmissionOption();
  document.getElementById('user-question').addEventListener('input', () => {
   const openOption = document.getElementById('open-option');
   openOption.disabled = false;
   openOption.checked = true;
   remote.getGlobal('sharedObject').questionSelected = document.getElementById('user-question').value;  }

)}


function sendFake() {

  remote.getGlobal('sharedObject').questionSelected = "";
  state = remote.getGlobal('sharedObject').state;
  for(var i=0; i<listCount; i++) {
     addQuestion(fake[state][i], i); // fake has 48
  }
 addOpenSubmissionOption();
  document.getElementById('user-question').addEventListener('input', () => {
   const openOption = document.getElementById('open-option');
   openOption.disabled = false;
   openOption.checked = true;
   remote.getGlobal('sharedObject').questionSelected = document.getElementById('user-question').value;  }

)}


function sendFunny() {
  remote.getGlobal('sharedObject').questionSelected = "";
  state = remote.getGlobal('sharedObject').state;
  for(var i=0; i<listCount; i++) {
     addQuestion(funny[i], i); //funny has 4
  };
 addOpenSubmissionOption();
  document.getElementById('user-question').addEventListener('input', () => {
   const openOption = document.getElementById('open-option');
   openOption.disabled = false;
   openOption.checked = true;
   remote.getGlobal('sharedObject').questionSelected = document.getElementById('user-question').value;
}
)}

function sendTell() {
  remote.getGlobal('sharedObject').questionSelected = '';
  state = remote.getGlobal('sharedObject').state;
  for(var i=0; i<listCount; i++) {
     addQuestion(tell[i], i); //tell has 4
  };
 addOpenSubmissionOption();
  document.getElementById('user-question').addEventListener('input', () => {
   const openOption = document.getElementById('open-option');
   openOption.disabled = false;
   openOption.checked = true;
   remote.getGlobal('sharedObject').questionSelected = document.getElementById('user-question').value;}
)}


function sendReddit() {
  remote.getGlobal('sharedObject').questionSelected = "";
  state = remote.getGlobal('sharedObject').state;
  for(var i=0; i<listCount; i++) {
     addQuestion(reddit[state][i], i); //reddit has 48
  };
 addOpenSubmissionOption();
  document.getElementById('user-question').addEventListener('input', () => {
   const openOption = document.getElementById('open-option');
   openOption.disabled = false;
   openOption.checked = true;
   remote.getGlobal('sharedObject').questionSelected = document.getElementById('user-question').value;}
)}

// HUNTER -- END OF NEW REFRESH FUNCTIONS


function playSoundFile(text, sendSilent = false) {
  console.log("Called voice"); 
  const voiceList = responsiveVoice.getVoices();
  const rate = document.getElementById('rate').value;
  const voiceSelect = document.getElementById('voice');
  const voice = voiceSelect.options[voiceSelect.selectedIndex].text;
  console.log('Rate: ', rate, 'Voice: ', voice);
  responsiveVoice.speak(text, voice, { 
    rate: rate,
    onend: () => {
      if (sendSilent){
        console.log("silent room")
        const message = new OSCSJS.Message('/silent', 1);
        const message1 = new OSC_JS.Message('/silent', 1);
        const message2 = new OSC_JS.Message('/silent', 1);
        console.log(message);
        osc.send(message);
        osc.send(message1);
        osc.send(message2);
        }
    }
  });
}

function selectPredefinedQuestion(radioButton) {
  console.log('Predefined question Selected');
  remote.getGlobal('sharedObject').questionSelected = radioButton.value;
}

function selectOptionSubmissionQuestion() {
  console.log('User input question selected');
  const userQuestion = document.getElementById('user-question').value;
  remote.getGlobal('sharedObject').questionSelected = userQuestion;
}

function sayHello() {
  //var text = "Welcome to my Lab. Thank you so much for your contributions in the parlour. Your emotional input is making a significant impact on my learning. As my assistants have told you, I have been scraping the internet for information about humans. You can imagine what kinds of crazy things I have been learning about your kind during my virtual travels. Now, I need you help"
  request('http://frankenstein.hunterowens.net/form-data/all', function (error, response, body) {
    console.log('error:', error); // Print the error if one occurred
    console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
    console.log('body:', body); // Print the HTML for the Google homepage
    const message = new OSC_JS.Message('/talking', 1)
    const message1 = new OSC_JS.Message('/talking', 1)
    const message2 = new OSC_JS.Message('/talking', 1)
    var text = "";
    osc.send(message);
    osc.send(message1);
    osc.send(message2);
    console.log("sending say hello " + message);
    obj = JSON.parse(body);
    var question = obj[1].question[0]; 
    request('http://frankenstein.hunterowens.net/interact', function (error, response, body) {
      const status = JSON.parse(body);
      const state = status.state2;
      console.log("API state: " + state)
      text += "Welcome to my Lab. Thank you for your contributions in the parlour. Your emotional data is making a significant impact on my learning., I parsed through the data you gave me, and "
      text += state
      text += " is the emotion I found. But I don’t understand why you wanted me to express this emotion. "
      text += " As my assistants told you, I have been scraping the internet for information about humans. You can imagine what kinds of crazy things I learned about your kind. Now I need to add to my corpus with data from actual human beings. I have taken data: "
      
      for (i in obj) {
        text = text + " " + obj[i].name[0] + "!";
      }
      text += " Now, I will begin our inquiry with the question you all found the most intriguing: "
      text += question;
      setTimeout(function () {
        console.log(text);
        playSoundFile(text, true);
      }, 3000);
    });
  });
} 

function addQuestion(message, questionNumber) {
  console.log('Add Question');
  document.getElementById('questions').innerHTML += `<div class="question"><input type="radio" class="predefined-option" id="question${questionNumber}" name="question" value="${message}" onchange="selectPredefinedQuestion(this);"><label for="question${questionNumber}">${message}</label></div>`;
}

function addOpenSubmissionOption() {
  console.log('Open Submission Added');
  document.getElementById('questions').innerHTML += `<div class="question"><input type="radio" id="open-option" name="question" onchange="selectOptionSubmissionQuestion(this);" disabled=true><input id="user-question" type="text">`
}

// HUNTER -- I ADDED A TRACKING BOOLEAN (gotQuestions) to submitQuestions() and askQuestions() 
// TO KEEP THE TEXT FROM COMING IN TRIPLICATE

function submitQuestions(event) {
  event.preventDefault();
  gotQuestions = false; 
  const questionSelected = remote.getGlobal('sharedObject').questionSelected;
  const delay = document.getElementById('delay').value;
  if (questionSelected === '') { return; }
  const message = new OSC_JS.Message('/talking', questionSelected);
  const message1 = new OSC_JS.Message('/talking', questionSelected);
  const message2 = new OSC_JS.Message('/talking', questionSelected);
  console.log('Question: ', questionSelected, 'Delay: ', delay, 'Message: ', message);
  osc.send(message);
  osc.send(message1);
  osc.send(message2);
  document.getElementById('questions').innerHTML += 'Waiting for text...';
  document.getElementById('questions').innerHTML += '<div class="question"><input type="radio" class="predefined-option" id="stored_question" name="question" value="What do feelings create and when" onchange="selectPredefinedQuestion(this);"><label for="predefinedQuestion">What do feelings create and when</label></div>';
  document.getElementById('questions').innerHTML += '<div class="question"><input type="radio" class="predefined-option" id="stored_question" name="question" value="Does AI in the world scare you?" onchange="selectPredefinedQuestion(this);"><label for="predefinedQuestion">Does AI in the world scare you?</label></div>';
  document.getElementById('questions').innerHTML += '<div class="question"><input type="radio" class="predefined-option" id="stored_question" name="question" value="When is loneliness a good thing? " onchange="selectPredefinedQuestion(this);"><label for="predefinedQuestion">When is loneliness a good thing?</label></div>';
  remote.getGlobal('sharedObject').questionSelected = '';
  setTimeout(() => {
    playSoundFile(questionSelected);
  }, delay * 1000);
}

function askQuestion(event) {
  event.preventDefault();
  gotQuestions = false; 
  const questionSelected = remote.getGlobal('sharedObject').questionSelected;
  const delay = document.getElementById('delay').value;
  if (questionSelected === '') { return; }
  const message = new OSC_JS.Message('/question', questionSelected);
  const message1 = new OSC_JS.Message('/question', questionSelected);
  const message2 = new OSC_JS.Message('/question', questionSelected);
  console.log('Question: ', questionSelected, 'Delay: ', delay, 'Message: ', message);
  osc.send(message);
  osc.send(message1);
  osc.send(message2);
  document.getElementById('questions').innerHTML += 'Waiting for text...';
  document.getElementById('questions').innerHTML += '<div class="question"><input type="radio" class="predefined-option" id="stored_question" name="question" value="What do feelings create and when" onchange="selectPredefinedQuestion(this);"><label for="predefinedQuestion">What do feelings create and when</label></div>';
  document.getElementById('questions').innerHTML += '<div class="question"><input type="radio" class="predefined-option" id="stored_question" name="question" value="Does AI in the world scare you?" onchange="selectPredefinedQuestion(this);"><label for="predefinedQuestion">Does AI in the world scare you?</label></div>';
  document.getElementById('questions').innerHTML += '<div class="question"><input type="radio" class="predefined-option" id="stored_question" name="question" value="When is loneliness a good thing? " onchange="selectPredefinedQuestion(this);"><label for="predefinedQuestion">When is loneliness a good thing? </label></div>';
  remote.getGlobal('sharedObject').questionSelected = '';
  setTimeout(() => {
    playSoundFile(questionSelected, true);
  }, delay * 1000);
}


// HUNTER -- THIS FUNCTION SENDS A CUE MESSAGE TO THE SYSTEM FOR SPECIFIC CANNED MOMENTS IN THE SHOW

function fireCue(cue) {
  console.log('Going to send: /cue' + cue);
  const message = new OSC_JS.message('/cue', cue);
  console.log(message);
  osc.send(message);

}

// HUNTER -- THIS FUNCTION ALLOWS THE AI TO SPEAK WITHOUT CHANGING STATE
// IT SHOULD JUST RECEIVE THE SELECTION AND TTS IT WITH NO OTHER CHANGE 

function tellComment(event) {
  event.preventDefault(); 
  setTimeout(() => {
    playSoundFile(questionSelected);
  }, delay * 1000);

}


function startShow() {
  const message = new OSC_JS.Message('/start', 1);
  console.log(message);
  osc.send(message);
}

function endShow() {
  const message = new OSC_JS.Message('/end', 1);
  console.log(message);
  request('http://frankenstein.hunterowens.net/reset', function (error, response, body) {
    console.log("API Reset Status Good: " + body)
    return body 
  }) 
  osc.send(message);
}

osc.on('/state', (message) => {
  console.log(message);
  state = remote.getGlobal('sharedObject').state;
  if (message.args[0] === state) { return; }
  document.getElementById('state').innerHTML = message.args[1];
  remote.getGlobal('sharedObject').state += message.args[2];
});

var osc_node = require('node-osc');
var oscServer = new osc_node.Server(srv_port, '0.0.0.0');


// HUNTER: I ADDED THE gotQuestions (THE TRACKING BOOLEAN) TO THE OSC MESSAGE RECEIVE BELOW
// SO THAT THE QUESTIONS DON'T APPEAR IN TRIPLICATE AND ERASE PROPERLY
// IF THERE'S A BUG ANYWHERE, IT'S HERE 

oscServer.on("message", function (msg, rinfo) {
      console.log("TUIO message:");
      if(!gotQuestions){}
      console.log(msg);
        document.getElementById('questions').innerHTML = ""; 
        endpoint = msg[0];
        console.log(endpoint);
       if (endpoint == '/textques') {
         console.log("in textques") 
         addQuestion(msg[1], '0');
         addQuestion(msg[2], '1');
         addQuestion(msg[3], '2');
         addQuestion(msg[4], '3');
         addOpenSubmissionOption();
          document.getElementById('user-question').addEventListener('input', () => {
           const openOption = document.getElementById('open-option');
           openOption.disabled = false;
           openOption.checked = true;
           remote.getGlobal('sharedObject').questionSelected = document.getElementById('user-question').value;
         }); 
        gotQuestions = true;  
      }
    });


osc.on('/textnoques', (message) => {
  console.log('/textnoques: ', message);
  const talkMessage = new OSC_JS.Message('/talking', message.args[0]);
  osc.send(talkMessage);
  setTimeout(() => {
    playSoundFile(message.args[0], true);
  }, message.args[1] * 1000);
});

osc.open();
window.addEventListener('unload', () => closeConnection());

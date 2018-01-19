const OSC = require('osc-js');
const remote = require('electron').remote;
const request = require('request');
const srv_port = 7007

const options = {
  open: { host: '192.168.1.255', port: srv_port },
  send: { host: '192.168.1.3', port: 7007 }
};
const osc = new OSC({ plugin: new OSC.DatagramPlugin(options) });
console.log('OSC: ', osc);

// Set host property for address other than localhost; eg. {host: 192.168.0.100, port: 7007}
// function createConnection() {
//  console.log('Open OSC Connection');
//  osc.open();
// }

function closeConnection() {
  console.log('Close OSC Connection');
  osc.close();
}

function sendRefresh() {
  remote.getGlobal('sharedObject').questionSelected = '';
  document.getElementById('questions').innerHTML = 'Waiting for text...';
  const message = new OSC.Message('/refresh', 1);
  console.log(message);
  osc.send(message);
}

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
      console.log("silent room")
      const message = new OSC.Message('/silent', 1);
      console.log(message);
      osc.send(message); 
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
  var text = "Hello";
  request('http://frankenstein.hunterowens.net/form-data/all', function (error, response, body) {
    console.log('error:', error); // Print the error if one occurred
    console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
    console.log('body:', body); // Print the HTML for the Google homepage
    var obj = JSON.parse(body);
    var name = obj[0].name[0];
    playSoundFile(text + name);
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

function submitQuestions(event) {
  event.preventDefault();
  const questionSelected = remote.getGlobal('sharedObject').questionSelected;
  const delay = document.getElementById('delay').value;
  if (questionSelected === '') { return; }
  const message = new OSC.Message('/talking', questionSelected);
  console.log('Question: ', questionSelected, 'Delay: ', delay, 'Message: ', message);
  osc.send(message);
  document.getElementById('questions').innerHTML = 'Waiting for text...';
  remote.getGlobal('sharedObject').questionSelected = '';
  setTimeout(() => {
    playSoundFile(questionSelected);
  }, delay * 1000);
}

function askQuestion(event) {
  event.preventDefault();
  const questionSelected = remote.getGlobal('sharedObject').questionSelected;
  const delay = document.getElementById('delay').value;
  if (questionSelected === '') { return; }
  const message = new OSC.Message('/question', questionSelected);
  console.log('Question: ', questionSelected, 'Delay: ', delay, 'Message: ', message);
  osc.send(message);
  document.getElementById('questions').innerHTML = 'Waiting for text...';
  remote.getGlobal('sharedObject').questionSelected = '';
  setTimeout(() => {
    playSoundFile(questionSelected);
  }, delay * 1000);
}

function startSurface() {
  const message = new OSC.Message('/startsurface', 1);
  console.log(message);
  osc.send(message);
}

function resetSurface() {
  const message = new OSC.Message('/resetsurface', 1);
  console.log(message);
  osc.send(message);
}

function stopSurface() {
  const message = new OSC.Message('/closesurface', 1);
  console.log(message);
  osc.send(message);
}

function endShow() {
  const message = new OSC.Message('/end', 1);
  console.log(message);
  osc.send(message);
}

osc.on('/state', (message) => {
  console.log(message);
  state = remote.getGlobal('sharedObject').state;
  if (message.args[0] === state) { return; }
    document.getElementById('state').innerHTML = message.args[0];
    remote.getGlobal('sharedObject').state = message.args[0];
    playSoundFile(message.args[0]);
});

var osc_node = require('node-osc');
var oscServer = new osc_node.Server(srv_port, '0.0.0.0');


oscServer.on("message", function (msg, rinfo) {
      console.log("TUIO message:");
      console.log(msg);
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
    }
  });


osc.on('/textnoques', (message) => {
  console.log('/textnoques: ', message);
  const talkMessage = new OSC.Message('/talking', message.args[0]);
  osc.send(talkMessage);
  setTimeout(() => {
    playSoundFile(message.args[0], true);
  }, message.args[1] * 1000);
});

osc.open();
window.addEventListener('unload', () => closeConnection());

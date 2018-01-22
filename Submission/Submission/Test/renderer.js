// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
const OSC = require('osc-js');

const options = {
  open: { host: '0.0.0.0', port: 7008 },
  send: { host: '192.168.1.3', port: 7007 }
};
const osc = new OSC({ plugin: new OSC.DatagramPlugin(options) });

// Set host property for address other than localhost; eg. {host: 192.168.0.100, port: 7007}
function createConnection() {
  osc.open();
  console.log("")
  console.log(osc);
}

function closeConnection() {
  osc.close();
}

function sendStartMessage() {
  const message = new OSC.Message('/reset', 1);
  console.log(message);
  osc.send(message);
  osc.send(message);
  osc.send(message);
  showIndex();
}

function showIndex() {
  window.location = './index.html';
}

function setEventListener() {
  const messageElement = document.querySelector('#message');
  messageElement.addEventListener('keyup', (event) => {
    if (messageElement.value !== '' && event.key === 'Enter') {
      event.preventDefault();
      const message = new OSC.Message('/answer', messageElement.value);
      console.log(message);
      osc.send(message);
      osc.send(message);
      osc.send(message);
      messageElement.value = '';
    }
  });
}

window.addEventListener('unload', () => closeConnection());
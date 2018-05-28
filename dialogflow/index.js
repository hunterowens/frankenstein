exports.helloHttp = function helloHttp (request, response) {
  var fs = require('fs');
  var questions = fs.readFileSync('questions.csv').toString().split("\n");
  
  var question = questions[Math.floor(Math.random()*questions.length)]
  response.json({ fulfillmentText: question});
};

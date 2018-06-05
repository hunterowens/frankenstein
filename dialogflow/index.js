

exports.helloHttp = function helloHttp (request, response) {
  var Airtable = require('airtable');
  var base = new Airtable({apiKey: 'keyLoE3zbLtTbI3VU'}).base('appTUc1Aznap8TIfJ');
  var questions = [];
  base('Table 1').select({
      // Selecting the first 3 records in Grid view:
      maxRecords: 3,
      view: "Grid view"
  }).eachPage(function page(records, fetchNextPage) {
      // This function (`page`) will get called for each page of records.

      records.forEach(function(record) {
          console.log('Retrieved', record.get('Question Text'));
          questions.push(record.get('Question Text'));
      });

      // To fetch the next page of records, call `fetchNextPage`.
      // If there are more records, `page` will get called again.
      // If there are no more records, `done` will get called.
      fetchNextPage();

  }, function done(err) {
      if (err) { console.error(err); return; }
      response.json({ fulfillmentText: questions[Math.floor(Math.random()*questions.length)]});
  });
    
};

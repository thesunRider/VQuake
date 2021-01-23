var express = require("express");
var app = express();

const sqliteJson = require('sqlite-json');
const exporter = sqliteJson('./filtered.db');

app.use(express.json({type: '*/*'}));

app.post("/client", express.json({type: '*/*'}),(req, res) => {
	rqust = req.body;
	console.log(rqust['query']);
	if ( rqust['query'] == 'url_filter') {

			exporter.json('select * FROM url_filter', function (err, jsn) {
		  		res.send(jsn);
		});
	}

	if ( rqust['query'] == 'tor_filter') {

			exporter.json('select * FROM tor_filter', function (err, jsn) {
		  		res.send(jsn);
		});
	}

});



app.listen(3000, () => {
 console.log("Server running on port 3000");
});
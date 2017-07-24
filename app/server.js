const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const logger = require('morgan');
const MongoClient = require('mongodb').MongoClient;
const app = express();
var db;

MongoClient.connect('mongodb://localhost:27017/fall-2017-06-01-15-54', (err, database) => {
  if (err) return console.log(err);
  db = database //Global Variable
});

app.use(logger('dev'));
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());
app.use('/dist', express.static(__dirname + '/dist'));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, './src/index.html'));
 });

app.get('/classes/:department', (req, res) => {
  db.collection(req.params.department).find().toArray((err, data) => {
    if (err) return console.log(err);
    res.send(data)
  });
});

app.get('/department', (req,res) => {
  db.listCollections().toArray((err,data) => {
    let data_array = [];
    if (err) return console.log(err);
    for (let i = 0; i < data.length; i++){
      db.collection(data[i].name).find().toArray((err,item) => {
        data_array.push(item[0].Subject);
        if (data_array.length === data.length){
          data_array.sort( (a,b) => {
            return a.toLowerCase().localeCompare(b.toLowerCase());
          });
          res.json(data_array);
        }
      });
    }
  });
});

app.get('*', (req, res) => {
  res.sendFile(path.resolve(__dirname, './src/index.html'));
});

app.listen(9000, () => {
    console.log('Listening on Port 9000');
});


var bodyParser = require('body-parser');
var express = require('express');

// Set up configuration
var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static('static'));
app.set('view engine', 'pug');

// Read in the questions from the input json file.
var questions = require('./data/gapfill_questions.json');

// Index endpoint.
app.get('/', function (req, res) {
    res.render('index');
});

// Endpoint that returns a random next question to show the user.
app.post('/next_question', function (req, res) {
    var questionId = Math.floor(Math.random() * questions.length);
    var sentence = questions[questionId].sentence;
    var keyword = questions[questionId].keyword;

    // generate a string of underscores to replace the blanked-out keyword in the sentence
    var blanks = "";
    for (var i = 0; i < keyword.length; i++) {
        blanks += "_";
    }

    res.send({
        questionId: questionId,
        sentence: sentence.replace(keyword, blanks),
    });
});

// Endpoint that checks an answer submitted by the user.
app.post('/check_answer', function (req, res) {
    var questionId = parseInt(req.body.questionId, 10);
    var answerGuess = req.body.answerGuess;

    var sentence = questions[questionId].sentence;
    var keyword = questions[questionId].keyword;

    res.send({
        sentence: sentence,
        answer: keyword,
        isCorrect: answerGuess.trim().toLowerCase() === keyword.trim().toLowerCase(),
    });
});

// Run the app on port 3000.
app.listen(3000, function () {
    console.log('App listening on port 3000');
});

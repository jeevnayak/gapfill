class App {
    constructor() {
        // ID of the current question being answered.
        this.questionId = null;
        // Sentence to display. If the user is answering the question, the sentence will have a series
        // of underscores where the answer should be. If the user has answered it, it will be unchanged.
        this.sentence = null;
        // Correct answer to the current question. This will only be populated after the user has guessed.
        this.answer = null;
        // Whether the user's answer to the current question was correct. This will only be populated after the user has guessed.
        this.isCorrect = null;

        // set up button and key listeners
        var app = this;
        $('#submit-button').on('click', function(event){
            app.checkAnswer();
        });
        $('#next-button').on('click', function(event){
            app.getNextQuestion();
        });
        $(document).keypress(function (event) {
            // listen to when Enter is pressed
            if (event.keyCode === 13) {
                if (app.answer === null) {
                    app.checkAnswer();
                } else {
                    app.getNextQuestion();
                }
            }
        });

        // initialize by getting the first question from the server
        this.getNextQuestion();
    }

    render() {
        // Refreshes the entire UI with the current data.

        // clear everything out
        $('#sentence').empty();
        $('#guess-form').hide();
        $('#results').hide();

        if (this.answer === null) {
            // render the question to be answered
            $('#sentence').text(this.sentence);
            $('#answer-input').val("");
            $('#guess-form').show();
            $('#answer-input').focus();
        } else {
            // render the result of the user's submitted answer
            this.renderSentenceWithHighlightedAnswer();
            this.renderResults();
            $('#results').show();
        }
    }

    renderSentenceWithHighlightedAnswer() {
        // Renders the sentence with the answer word highlighted.

        var sentenceDiv = $('#sentence');
        var sentenceParts = this.sentence.split(this.answer);
        if (sentenceParts.length === 2) {
            // highlight the answer word based on whether or not the user was correct
            var answerClass = this.isCorrect ? "correct" : "incorrect";
            $("<span>" + sentenceParts[0] + "</span>").appendTo(sentenceDiv);
            $("<span class=" + answerClass + ">" + this.answer + "</span>").appendTo(sentenceDiv);
            $("<span>" + sentenceParts[1] + "</span>").appendTo(sentenceDiv);
        } else {
            // we hit a bad case because of our naive substring detection, so just don't highlight
            $('#sentence').text(this.sentence);
        }
    }

    renderResults() {
        // Renders the results (whether the user's answer was correct).

        var answerGuess = $('#answer-input').val();
        var resultSpan = $('#result');
        resultSpan.empty();
        if (this.isCorrect) {
            $("<span class='correct'>" + answerGuess + "</span>").appendTo(resultSpan);
            $("<span> is correct!</span>").appendTo(resultSpan);
        } else {
            $("<span class='incorrect'>" + answerGuess + "</span>").appendTo(resultSpan);
            $("<span> is incorrect</span>").appendTo(resultSpan);
        }
    }

    getNextQuestion() {
        // Fetches the next question from the server.

        var app = this;
        $.ajax("/next_question", {
            type: "POST",
            success: function(resp) {
                // refresh the UI with the new question
                app.questionId = resp.questionId;
                app.sentence = resp.sentence;
                app.answer = null;
                app.isCorrect = null;
                app.render();
            }
        });
    }

    checkAnswer() {
        // Checks the user's answer with the server.

        var app = this;
        $.ajax("/check_answer", {
            type: "POST",
            data: {
                questionId: app.questionId,
                answerGuess: $('#answer-input').val(),
            },
            success: function(resp) {
                // refresh the UI with the results
                app.sentence = resp.sentence;
                app.answer = resp.answer;
                app.isCorrect = resp.isCorrect;
                app.render();
            }
        });
    }
}

$(function() {
    new App();
});

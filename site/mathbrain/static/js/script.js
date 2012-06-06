
// Our exam class
function Exam() {
    // some private variables
    var TOTALMARKS = 12;
    var TOTALQUESTIONS = 12;

    
    this.currQuestion = function() {
    };

    this.currMarks = function() {

    };

}


var currentQuestion = function(question) {
    // Gets what questions we have done
    if (typeof(question) === 'number') {
        this.question = question;
    }
};



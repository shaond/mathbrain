/* Most of our external functions */

var saveQuestions = function(questions) {
    // saves the questions JSON object using local storage
    if (localStorage) {
        localStorage.setItem("questions", JSON.stringify(questions));
    }
};

var prefetchImages = function(questions) {
    // prefetch all images for this exam
    URL = '/questions/';
    if (questions.length > 0) {
        for (var i; i < questions.length; i++) {
            $.ajax({
		url: URL + questions[i].fields.img, 
		cache: true, 
		async: true, 
	        success: function() {
		   //Insert into the DOM but display as NONE 
		   //This 'caches' image in DOM so when it's called it is available 
		   //$(this).

	    }});        
        }
    }
};

var recordQuestionTime = function(qid, qtime) {
    // Save the time
    if (localStorage) {
        localStorage.setItem(qid, qtime);
    }
};

// This should only be called in onbeforeunload
var recordTotalTime = function(ttime) {
    // Save the time
    if (localStorage) {
        localStorage.setItem("total_time", ttime);
    }
};

// This should only be called in onbeforeunload
var recordLastState = function(qid, nxt, prev) {
    // Save the state of timer app
    if (localStorage) {
        localStorage.setItem("last_qid", qid);
        localStorage.setItem("nxt", nxt);
        localStorage.setItem("prev", prev);
    }
};

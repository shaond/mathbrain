/* Most of our external functions */

var saveQuestions = function(questions) {
    // saves the questions JSON object using local storage
    if (localStorage) {
        localStorage.setItem("questions", JSON.stringify(questions));
    }
};

var prefetchImages = function(questions) {
    // prefetch all images for this exam
    if (questions.length > 0) {
        for (var i = 0; i < questions.length; i++) {
            $.ajax({
            url: "/" + questions[i].fields.question_img, 
            cache: true, 
            async: true, 
	        success: function() {
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

var reportCard = function() {
    if (localStorage) {
        // Get all values who's key starts with "questions/"
	var totalTime = localStorage.getItem("total_time");
	var subject = JSON.parse(localStorage.getItem("questions"))[0].fields.subject;
	var allocatedTime = [];
	var qnTime = [];
        for (var key in localStorage) {
            if (key.match(/^questions\/[0-9]/)) {
                qnTime.push(localStorage.getItem(key));
	        switch (parseInt(subject)) {
		    case 2:
		        // 2 Unit question
                        allocatedTime.push(parseInt(key.split("_")[4].split("m")[0]) * 180/120 * 60);
		        break;
		    case 3:
		        // 3 Unit question
                        allocatedTime.push(parseInt(key.split("_")[4].split("m")[0]) * 120/84 * 60);
		        break;
		    case 4:
		        // 4 Unit question
                        allocatedTime.push(parseInt(key.split("_")[4].split("m")[0]) * 180/120 * 60);
		    break;
	        }
            }
        }

        // Show the report card and hide the questions
        $("#question_container").hide();
        $("#reportcard_container").removeClass("hidden");
    }
};

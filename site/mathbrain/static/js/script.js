/* Most of our external functions */

var saveQuestions = function(questions) {
    // saves the questions JSON object using local storage
    localStorage.setItem("questions", questions);
};

var prefetchImages = function(questions) {
    // prefetch all images for this exam
    URL = '/questions/';
    if (questions.length > 0){
        for (var i; i < questions.length; i++) {
            $.ajax({url: URL + questions[i].fields.img, cache: true, async: true, success: function() {} });        
        }
    }
};

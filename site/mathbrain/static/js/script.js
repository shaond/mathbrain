Ext.require([
    'Ext.data.*',
    'Ext.chart.*',
    'Ext.grid.Panel',
    'Ext.layout.container.Column'
]);

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
	var totalTime = localStorage.getItem("total_time"); //Actually total time left on clock
	var subject = JSON.parse(localStorage.getItem("questions"))[0].fields.subject;
	var allocatedTime = 0; // Accounts for when we don't get exactly the question marks due to small pool of questions

	// Clear any recordCard calcs stored
	switch (parseInt(subject)) {
	    case 2:
		// 2 Unit question
		localStorage.removeItem("q1-allocatedTime");
		localStorage.removeItem("q2-allocatedTime");
		localStorage.removeItem("q3-allocatedTime");
		localStorage.removeItem("q4-allocatedTime");
		localStorage.removeItem("q5-allocatedTime");
		localStorage.removeItem("q6-allocatedTime");
		localStorage.removeItem("q7-allocatedTime");
		localStorage.removeItem("q8-allocatedTime");
		localStorage.removeItem("q9-allocatedTime");
		localStorage.removeItem("q10-allocatedTime");

		localStorage.removeItem("q1-totalLeft");
		localStorage.removeItem("q2-totalLeft");
		localStorage.removeItem("q3-totalLeft");
		localStorage.removeItem("q4-totalLeft");
		localStorage.removeItem("q5-totalLeft");
		localStorage.removeItem("q6-totalLeft");
		localStorage.removeItem("q7-totalLeft");
		localStorage.removeItem("q8-totalLeft");
		localStorage.removeItem("q9-totalLeft");
		localStorage.removeItem("q10-totalLeft");
		break;
	    case 3:
		// 3 Unit question
		localStorage.removeItem("q1-allocatedTime");
		localStorage.removeItem("q2-allocatedTime");
		localStorage.removeItem("q3-allocatedTime");
		localStorage.removeItem("q4-allocatedTime");
		localStorage.removeItem("q5-allocatedTime");
		localStorage.removeItem("q6-allocatedTime");
		localStorage.removeItem("q7-allocatedTime");
		localStorage.removeItem("q8-allocatedTime");

		localStorage.removeItem("q1-totalLeft");
		localStorage.removeItem("q2-totalLeft");
		localStorage.removeItem("q3-totalLeft");
		localStorage.removeItem("q4-totalLeft");
		localStorage.removeItem("q5-totalLeft");
		localStorage.removeItem("q6-totalLeft");
		localStorage.removeItem("q7-totalLeft");
		localStorage.removeItem("q8-totalLeft");
		break;
	    case 4:
		// 4 Unit question
		localStorage.removeItem("q1-allocatedTime");
		localStorage.removeItem("q2-allocatedTime");
		localStorage.removeItem("q3-allocatedTime");
		localStorage.removeItem("q4-allocatedTime");
		localStorage.removeItem("q5-allocatedTime");
		localStorage.removeItem("q6-allocatedTime");
		localStorage.removeItem("q7-allocatedTime");
		localStorage.removeItem("q8-allocatedTime");
		localStorage.removeItem("q9-allocatedTime");
		localStorage.removeItem("q10-allocatedTime");

		localStorage.removeItem("q1-totalLeft");
		localStorage.removeItem("q2-totalLeft");
		localStorage.removeItem("q3-totalLeft");
		localStorage.removeItem("q4-totalLeft");
		localStorage.removeItem("q5-totalLeft");
		localStorage.removeItem("q6-totalLeft");
		localStorage.removeItem("q7-totalLeft");
		localStorage.removeItem("q8-totalLeft");
		localStorage.removeItem("q9-totalLeft");
		localStorage.removeItem("q10-totalLeft");
	    break;
	}

        // Accumulate time left for each question 
        for(var i = 0; i < localStorage.length; i++) {
            if (localStorage.key(i).match(/^questions\/[0-9]/)) {
	        var minLeft = parseInt(localStorage.getItem(localStorage.key(i)).split(":")[0]);
		var secLeft = parseInt(localStorage.getItem(localStorage.key(i)).split(":")[1]);
		var qnTimeLeft = 0;
	        if (localStorage.getItem(localStorage.key(i).split("_")[2]+"-totalLeft")) {
		    qnTimeLeft = minLeft*60 + secLeft + parseInt(localStorage.getItem(localStorage.key(i).split("_")[2]+"-totalLeft"));
	        }
	        else {
		    qnTimeLeft = minLeft*60 + secLeft;
	        }
	        localStorage.setItem(localStorage.key(i).split("_")[2]+"-totalLeft", qnTimeLeft);

	        switch (parseInt(subject)) {
		    case 2:
		        // 2 Unit question
			if (localStorage.getItem(localStorage.key(i).split("_")[2]+"-allocatedTime")) {
			    localStorage.setItem(localStorage.key(i).split("_")[2]+"-allocatedTime", parseInt(localStorage.getItem(localStorage.key(i).split("_")[2]+"-allocatedTime")) + parseInt(localStorage.key(i).split("_")[4].split("m")[0]) * 180/120 * 60);
			}
			else {
			    localStorage.setItem(localStorage.key(i).split("_")[2]+"-allocatedTime", parseInt(localStorage.key(i).split("_")[4].split("m")[0]) * 180/120 * 60);
			}
		        break;
		    case 3:
		        // 3 Unit question
			if (localStorage.getItem(localStorage.key(i).split("_")[2]+"-allocatedTime")) {
			    localStorage.setItem(localStorage.key(i).split("_")[2]+"-allocatedTime", parseInt(localStorage.getItem(localStorage.key(i).split("_")[2]+"-allocatedTime")) + parseInt(localStorage.key(i).split("_")[4].split("m")[0]) * 120/84 * 60);
			}
			else {
			    localStorage.setItem(localStorage.key(i).split("_")[2]+"-allocatedTime", parseInt(localStorage.key(i).split("_")[4].split("m")[0]) * 120/84 * 60);
			}
		        break;
		    case 4:
		        // 4 Unit question
			if (localStorage.getItem(localStorage.key(i).split("_")[2]+"-allocatedTime")) {
			    localStorage.setItem(localStorage.key(i).split("_")[2]+"-allocatedTime", parseInt(localStorage.getItem(localStorage.key(i).split("_")[2]+"-allocatedTime")) + parseInt(localStorage.key(i).split("_")[4].split("m")[0]) * 180/120 * 60);
			}
			else {
			    localStorage.setItem(localStorage.key(i).split("_")[2]+"-allocatedTime", parseInt(localStorage.key(i).split("_")[4].split("m")[0]) * 180/120 * 60);
			}
		    break;
	        }
            }
        }

        // Populate the data set for charting
	var store = null;
	switch (parseInt(subject)) {
	    case 2:
		// 2 Unit question
		store = new Ext.data.JsonStore({
		    fields:['name', 'total'],
		    data: [
			{name:'Question One', total: localStorage.getItem("q1-allocatedTime") - parseInt(localStorage.getItem("q1-totalLeft")) + 50},
			{name:'Question Two', total: localStorage.getItem("q2-allocatedTime") - parseInt(localStorage.getItem("q2-totalLeft")) + 50},
			{name:'Question Three', total: localStorage.getItem("q3-allocatedTime") - parseInt(localStorage.getItem("q3-totalLeft")) + 50},
			{name:'Question Four', total: localStorage.getItem("q4-allocatedTime") - parseInt(localStorage.getItem("q4-totalLeft")) + 50},
			{name:'Question Five', total: localStorage.getItem("q5-allocatedTime") - parseInt(localStorage.getItem("q5-totalLeft")) + 50},
			{name:'Question Six', total: localStorage.getItem("q6-allocatedTime") - parseInt(localStorage.getItem("q6-totalLeft")) + 50},
			{name:'Question Seven', total: localStorage.getItem("q7-allocatedTime") - parseInt(localStorage.getItem("q7-totalLeft")) + 50},
			{name:'Question Eight', total: localStorage.getItem("q8-allocatedTime") - parseInt(localStorage.getItem("q8-totalLeft")) + 50},
			{name:'Question Nine', total: localStorage.getItem("q9-allocatedTime") - parseInt(localStorage.getItem("q9-totalLeft")) + 50},
			{name:'Question Ten', total: localStorage.getItem("q10-allocatedTime") - parseInt(localStorage.getItem("q10-totalLeft")) + 50}
		    ]
		});
		break;
	    case 3:
		// 3 Unit question
		store = new Ext.data.JsonStore({
		    fields:['name', 'total'],
		    data: [
			{name:'Question One', total: localStorage.getItem("q1-allocatedTime") - parseInt(localStorage.getItem("q1-totalLeft")) + 50},
			{name:'Question Two', total: localStorage.getItem("q2-allocatedTime") - parseInt(localStorage.getItem("q2-totalLeft")) + 50},
			{name:'Question Three', total: localStorage.getItem("q3-allocatedTime") - parseInt(localStorage.getItem("q3-totalLeft")) + 50},
			{name:'Question Four', total: localStorage.getItem("q4-allocatedTime") - parseInt(localStorage.getItem("q4-totalLeft")) + 50},
			{name:'Question Five', total: localStorage.getItem("q5-allocatedTime") - parseInt(localStorage.getItem("q5-totalLeft")) + 50},
			{name:'Question Six', total: localStorage.getItem("q6-allocatedTime") - parseInt(localStorage.getItem("q6-totalLeft")) + 50},
			{name:'Question Seven', total: localStorage.getItem("q7-allocatedTime") - parseInt(localStorage.getItem("q7-totalLeft")) + 50},
			{name:'Question Eight', total: localStorage.getItem("q8-allocatedTime") - parseInt(localStorage.getItem("q8-totalLeft")) + 50},
		    ]
		});
		break;
	    case 4:
		// 4 Unit question
		store = new Ext.data.JsonStore({
		    fields:['name', 'total'],
		    data: [
			{name:'Question One', total: localStorage.getItem("q1-allocatedTime") - parseInt(localStorage.getItem("q1-totalLeft")) + 50},
			{name:'Question Two', total: localStorage.getItem("q2-allocatedTime") - parseInt(localStorage.getItem("q2-totalLeft")) + 50},
			{name:'Question Three', total: localStorage.getItem("q3-allocatedTime") - parseInt(localStorage.getItem("q3-totalLeft")) + 50},
			{name:'Question Four', total: localStorage.getItem("q4-allocatedTime") - parseInt(localStorage.getItem("q4-totalLeft")) + 50},
			{name:'Question Five', total: localStorage.getItem("q5-allocatedTime") - parseInt(localStorage.getItem("q5-totalLeft")) + 50},
			{name:'Question Six', total: localStorage.getItem("q6-allocatedTime") - parseInt(localStorage.getItem("q6-totalLeft")) + 50},
			{name:'Question Seven', total: localStorage.getItem("q7-allocatedTime") - parseInt(localStorage.getItem("q7-totalLeft")) + 50},
			{name:'Question Eight', total: localStorage.getItem("q8-allocatedTime") - parseInt(localStorage.getItem("q8-totalLeft")) + 50},
			{name:'Question Nine', total: localStorage.getItem("q9-allocatedTime") - parseInt(localStorage.getItem("q9-totalLeft")) + 50},
			{name:'Question Ten', total: localStorage.getItem("q10-allocatedTime") - parseInt(localStorage.getItem("q10-totalLeft")) + 50}
		    ]
		});
	    break;
	}

        // Draw the reportcard
	var chart = Ext.create('Ext.chart.Chart', {
	    width: 600,
	    height: 500,
	    animate: true,
	    shadow: true,
	    store: store,
	    renderTo: 'reportcard_container',
	    legend: {
		position: 'right'
	    },
	    insetPadding: 20,
	    theme: 'Base:gradients',
	    series: [{
		type: 'pie',
		field: 'total',
		highlight: {
		  segment: {
		    margin: 20
		  }
		},
		listeners:{
		    itemmousedown : function(obj) {
			// We need to subtract the fudge factor of 50. We are using 50 as if we don't nothing appears for things < 10 in pie chart
			alert(obj.storeItem.data['name'] + ' spent ' + String(parseInt(obj.storeItem.data['total']) - 50) + ' seconds');
		    }
		},
		label: {
		    field: 'name',
		    display: 'rotate',
		    contrast: true,
		    font: '13px Arial'
		}
	    }], 
            items: [{
                type  : 'text',
                text  : 'Time Spent Chart',
                font  : '18px Arial',
                width : 100,
                height: 30,
                x : 50, //the sprite x position
                y : 20  //the sprite y position
            }]
	});

        // Show the report card and hide the questions
        $("#question_container").hide();
        $("#reportcard_container").removeClass("hidden");

	// Change cursor to mouse pointer when hovering over chart
	$('div[id^=chart]').css("cursor", "pointer");  
    }
};

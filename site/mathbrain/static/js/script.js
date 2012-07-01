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
	var subject = parseInt(JSON.parse(localStorage.getItem("questions"))[0].fields.subject);
	var allocatedTime = 0; // Accounts for when we don't get exactly the question marks due to small pool of questions

    var allocatedTime = {}, totalLeft = {};
	// Clear any recordCard calcs stored

        // Accumulate time left for each question 
        for(var i = 0; i < localStorage.length; i++) {
            if (localStorage.key(i).match(/^questions\/[0-9]/)) {
		        var qnTimeLeft = 0;
                var minLeft = parseInt(localStorage.getItem(localStorage.key(i)).split(":")[0], 10);
		        var secLeft = parseInt(localStorage.getItem(localStorage.key(i)).split(":")[1], 10);
		        var totalLeftValKey = localStorage.key(i).split("_")[2]+"-totalLeft";
		        //var totalLeftVal = localStorage.getItem(totalLeftValKey);
	            if (totalLeft[totalLeftValKey]) {
		            qnTimeLeft = minLeft*60 + secLeft + totalLeft[totalLeftValKey];
	            }
	            else {
		            qnTimeLeft = minLeft*60 + secLeft;
	            }
	            totalLeft[totalLeftValKey] = qnTimeLeft;

		        var allocatedTimeValKey = localStorage.key(i).split("_")[2]+"-allocatedTime";
		        var allocatedMarkVal = parseInt(localStorage.key(i).split("_")[4].split("m")[0], 10);
	            switch (subject) {
		            case 2: // 2 Unit question
			            if (allocatedTime[allocatedTimeValKey]) {
			                allocatedTime[allocatedTimeValKey] = allocatedTime[allocatedTimeValKey] + allocatedMarkVal * 180/120 * 60;
			            }
			            else {
			                allocatedTime[allocatedTimeValKey] =  allocatedMarkVal * 180/120 * 60;
			            }
		                break;
		            case 3: // 3 Unit question
			            if (allocatedTime[allocatedTimeValKey]) {
			                allocatedTime[allocatedTimeValKey] = allocatedTime[allocatedTimeValKey] + allocatedMarkVal * 120/84 * 60;
			            }
			            else {
			                allocatedTime[allocatedTimeValKey] =  allocatedMarkVal * 120/84 * 60;
			            }
		                break;
		            case 4: // 4 Unit question
			            if (allocatedTime[allocatedTimeValKey]) {
			                allocatedTime[allocatedTimeValKey] = allocatedTime[allocatedTimeValKey] + allocatedMarkVal * 180/120 * 60;
			            }
			            else {
			                allocatedTime[allocatedTimeValKey] =  allocatedMarkVal * 180/120 * 60;
			            }
		                break;
	            }
            }
        }

        // Populate the data set for charting
	    var store = null;
        var fudgeFactor = 50; // This applies to ExtJS Pie Charts as if we get something < 10 we cannot hover & click on it
        switch (subject) {
            case 2: // 2 Unit question
                store = new Ext.data.JsonStore({
                    fields:['name', 'total'],
                    data: [
                    {name:'Question One', total: allocatedTime["q1-allocatedTime"] - totalLeft["q1-totalLeft"] + fudgeFactor},
                    {name:'Question Two', total: allocatedTime["q2-allocatedTime"] - totalLeft["q2-totalLeft"] + fudgeFactor},
                    {name:'Question Three', total: allocatedTime["q3-allocatedTime"] - totalLeft["q3-totalLeft"] + fudgeFactor},
                    {name:'Question Four', total: allocatedTime["q4-allocatedTime"] - totalLeft["q4-totalLeft"] + fudgeFactor},
                    {name:'Question Five', total: allocatedTime["q5-allocatedTime"] - totalLeft["q5-totalLeft"] + fudgeFactor},
                    {name:'Question Six', total: allocatedTime["q6-allocatedTime"] - totalLeft["q6-totalLeft"] + fudgeFactor},
                    {name:'Question Seven', total: allocatedTime["q7-allocatedTime"] - totalLeft["q7-totalLeft"] + fudgeFactor},
                    {name:'Question Eight', total: allocatedTime["q8-allocatedTime"] - totalLeft["q8-totalLeft"] + fudgeFactor},
                    {name:'Question Nine', total: allocatedTime["q9-allocatedTime"] - totalLeft["q9-totalLeft"] + fudgeFactor},
                    {name:'Question Ten', total: allocatedTime["q10-allocatedTime"] - totalLeft["q10-totalLeft"] + fudgeFactor}
                    ]
                });
                break;
            case 3: // 3 Unit question
                store = new Ext.data.JsonStore({
                    fields:['name', 'total'],
                    data: [
                    {name:'Question One', total: allocatedTime["q1-allocatedTime"] - totalLeft["q1-totalLeft"] + fudgeFactor},
                    {name:'Question Two', total: allocatedTime["q2-allocatedTime"] - totalLeft["q2-totalLeft"] + fudgeFactor},
                    {name:'Question Three', total: allocatedTime["q3-allocatedTime"] - totalLeft["q3-totalLeft"] + fudgeFactor},
                    {name:'Question Four', total: allocatedTime["q4-allocatedTime"] - totalLeft["q4-totalLeft"] + fudgeFactor},
                    {name:'Question Five', total: allocatedTime["q5-allocatedTime"] - totalLeft["q5-totalLeft"] + fudgeFactor},
                    {name:'Question Six', total: allocatedTime["q6-allocatedTime"] - totalLeft["q6-totalLeft"] + fudgeFactor},
                    {name:'Question Seven', total: allocatedTime["q7-allocatedTime"] - totalLeft["q7-totalLeft"] + fudgeFactor}
                    ]
                });
                break;
            case 4: // 4 Unit question
                store = new Ext.data.JsonStore({
                    fields:['name', 'total'],
                    data: [
                    {name:'Question One', total: allocatedTime["q1-allocatedTime"] - totalLeft["q1-totalLeft"] + fudgeFactor},
                    {name:'Question Two', total: allocatedTime["q2-allocatedTime"] - totalLeft["q2-totalLeft"] + fudgeFactor},
                    {name:'Question Three', total: allocatedTime["q3-allocatedTime"] - totalLeft["q3-totalLeft"] + fudgeFactor},
                    {name:'Question Four', total: allocatedTime["q4-allocatedTime"] - totalLeft["q4-totalLeft"] + fudgeFactor},
                    {name:'Question Five', total: allocatedTime["q5-allocatedTime"] - totalLeft["q5-totalLeft"] + fudgeFactor},
                    {name:'Question Six', total: allocatedTime["q6-allocatedTime"] - totalLeft["q6-totalLeft"] + fudgeFactor},
                    {name:'Question Seven', total: allocatedTime["q7-allocatedTime"] - totalLeft["q7-totalLeft"] + fudgeFactor},
                    {name:'Question Eight', total: allocatedTime["q8-allocatedTime"] - totalLeft["q8-totalLeft"] + fudgeFactor}
                    ]
                });
                break;
        }

        renderReportCard(store);
    }
};

function renderReportCard(store) {
    var fudgeFactor = 50; // This applies to ExtJS Pie Charts as if we get something < 10 we cannot hover & click on it
    
    // Draw the reportcard
	var chart = Ext.create('Ext.chart.Chart', {
	    //width: 600,
	    //height: 500,
	    width: 700,
	    height: 600,
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
                alert(obj.storeItem.data['name'] + ' spent ' + String(parseInt((obj.storeItem.data['total']) - fudgeFactor), 10) + ' seconds');
                /*var detailPanel = Ext.create('Ext.grid.Panel', {
                    id: 'results-form',
                    flex: 0.60,
                    //store: store,
                    title:'Question Breakdown Data',
                    renderTo: 'reportcard_container',
                    columns: [
                        {
                            id       :'question',
                            text   : 'Question',
                            flex: 1,
                            sortable : true
                            //dataIndex: 'question'
                        },
                        {
                            text   : 'Time Spent',
                            width    : 75,
                            sortable : true,
                            align: 'right'
                            //dataIndex: 'growth %',
                            //renderer: perc
                        },
                        {
                            text   : 'Time Allocated',
                            width    : 75,
                            sortable : true,
                            align: 'right'
                            //dataIndex: 'product %',
                            //renderer: perc
                        },
                        {
                            text   : 'Answer',
                            width    : 75,
                            sortable : true,
                            align: 'right'
                            //dataIndex: 'market %',
                            //renderer: perc
                        }
                    ],

                });*/
		    }
		},
		label: {
		    field: 'name',
		    display: 'rotate',
		    contrast: true,
		    minMargin: 100,
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

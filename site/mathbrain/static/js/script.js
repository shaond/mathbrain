Ext.require([
    'Ext.data.*',
    'Ext.chart.*',
    'Ext.grid.Panel',
    'Ext.grid.RowNumberer',
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

        // Clear any recordCard calcs stored
        var allocatedTime = {}, totalLeft = {};
        var qList = {}, q1 = [], q2 = [], q3 = [], q4 = [], q5 = [], q6 = [], q7 = [], q8 = [], q9 = [], q10 = [];

        // Accumulate time left for each question 
        for(var i = 0; i < localStorage.length; i++) {
            if (localStorage.key(i).match(/^questions\/[0-9]/)) {
		        var qnTime = 0;
		        var qnTimeLeft = 0;
		        var keyLoc = localStorage.key(i);
		        var itemVal = localStorage.getItem(keyLoc);
                var minLeft = parseInt(itemVal.split(":")[0], 10);
		        var secLeft = parseInt(itemVal.split(":")[1], 10);
		        var questionType = keyLoc.split("_")[2];
		        var totalLeftValKey = questionType+"-totalLeft";
                qnTime = minLeft*60 + secLeft;
	            if (totalLeft[totalLeftValKey]) {
		            qnTimeLeft = qnTime + totalLeft[totalLeftValKey];
	            }
	            else {
		            qnTimeLeft = qnTime;
	            }
	            totalLeft[totalLeftValKey] = qnTimeLeft;

		        var allocatedTimeValKey = keyLoc.split("_")[2]+"-allocatedTime";
		        var allocatedMarkVal = parseInt(keyLoc.split("_")[4].split("m")[0], 10);
		        var allocAddedTime = 0;
	            switch (subject) {
		            case 2: // 2 Unit question
                        allocAddedTime = allocatedMarkVal * 180/120 * 60;
		                break;
		            case 3: // 3 Unit question
                        allocAddedTime = allocatedMarkVal * 120/84 * 60;
		                break;
		            case 4: // 4 Unit question
                        allocAddedTime = allocatedMarkVal * 180/120 * 60;
		                break;
	            }

                if (allocatedTime[allocatedTimeValKey]) {
                    allocatedTime[allocatedTimeValKey] = allocatedTime[allocatedTimeValKey] + allocAddedTime;
                }
                else {
                    allocatedTime[allocatedTimeValKey] =  allocAddedTime;
                }

                // Extract values for the DetailedReportCard
                var qSrc = "(Q" + keyLoc.split("_")[2][1] + keyLoc.split("_")[3] + ") " + keyLoc.split("_")[1] + " " + keyLoc.split("_")[5];
                qnTime = Math.floor(allocAddedTime - qnTime);
                if (qnTime < 1)
                    qnTime = 0;
                var qDetail = [keyLoc, itemVal, sprintf("%02f:%02f", Math.floor(qnTime/60), Math.floor(qnTime%60)), sprintf("%02f:%02f", Math.floor(allocAddedTime/60), Math.ceil(allocAddedTime%60)), qSrc];
	            switch (questionType) {
		            case "q1": // Question 1
			            // Assume each key unique (no need for conditional)
                        q1.push(qDetail);
		                break;
		            case "q2": // Question 2
                        q2.push(qDetail);
		                break;
		            case "q3": // Question 3
                        q3.push(qDetail);
		                break;
		            case "q4": // Question 4
                        q4.push(qDetail);
		                break;
		            case "q5": // Question 5
                        q5.push(qDetail);
		                break;
		            case "q6": // Question 6
                        q6.push(qDetail);
		                break;
		            case "q7": // Question 7
                        q7.push(qDetail);
		                break;
		            case "q8": // Question 8
                        q8.push(qDetail);
		                break;
		            case "q9": // Question 9
                        q9.push(qDetail);
		                break;
		            case "q10": // Question 10
                        q10.push(qDetail);
		                break;
	            }
            }
        }

        qList['q1'] = q1;
        qList['q2'] = q2;
        qList['q3'] = q3;
        qList['q4'] = q4;
        qList['q5'] = q5;
        qList['q6'] = q6;
        qList['q7'] = q7;
        qList['q8'] = q8;
        qList['q9'] = q9;
        qList['q10'] = q10;


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

        renderReportCard(store, qList);
    }
};

function renderReportCard(store, qList) {
    var fudgeFactor = 50; // This applies to ExtJS Pie Charts as if we get something < 10 we cannot hover & click on it
    var detailPanel = null;
    
    // Draw the reportcard
	var chart = Ext.create('Ext.chart.Chart', {
        id: 'time-spent-chart',
	    width: 500,
	    height: 400,
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
                //alert(obj.storeItem.data['name'] + ' spent ' + String(parseInt((obj.storeItem.data['total']) - fudgeFactor), 10) + ' seconds');
                var questionData = null;
                if (obj.storeItem.data['name'] === "Question One") 
                    questionData = qList['q1'];
                else if (obj.storeItem.data['name'] === "Question Two") 
                    questionData = qList['q2'];
                else if (obj.storeItem.data['name'] === "Question Three") 
                    questionData = qList['q3'];
                else if (obj.storeItem.data['name'] === "Question Four") 
                    questionData = qList['q4'];
                else if (obj.storeItem.data['name'] === "Question Five") 
                    questionData = qList['q5'];
                else if (obj.storeItem.data['name'] === "Question Six") 
                    questionData = qList['q6'];
                else if (obj.storeItem.data['name'] === "Question Seven") 
                    questionData = qList['q7'];
                else if (obj.storeItem.data['name'] === "Question Eight") 
                    questionData = qList['q8'];
                else if (obj.storeItem.data['name'] === "Question Nine") 
                    questionData = qList['q9'];
                else if (obj.storeItem.data['name'] === "Question Ten") 
                    questionData = qList['q10'];

                var detailedReportStore = Ext.create('Ext.data.ArrayStore', {
                    // store configs
                    autoDestroy: true,
                    storeId: 'detailedQuestion',
                    // reader configs
                    idIndex: 0,
                    fields: [
                       'id',
                       'time_left',
                       'time_spent',
                       'time_allocated',
                       'source'
                    ], 
                    data: questionData
                });

                if (detailPanel) {
                    detailPanel.close();
                }
                detailPanel = Ext.create('Ext.grid.Panel', {
                    id: 'results-form',
                    flex: 0.60,
                    store: detailedReportStore,
                    width: 700,
                    title: obj.storeItem.data['name'] + ' Breakdown Data',
                    renderTo: 'reportcard_container',
                    columns: [
                        /*{
                            id       :'question',
                            text   : 'Question',
                            //flex: 1,
                            width    : 75,
                            sortable : true,
                            dataIndex: 'id'
                        },*/
                        {xtype: 'rownumberer'},
                        {
                            text   : 'Time Spent',
                            width    : 75,
                            sortable : true,
                            align: 'right',
                            dataIndex: 'time_spent'
                            //renderer: perc
                        },
                        {
                            text   : 'Time Left',
                            width    : 75,
                            sortable : true,
                            align: 'right',
                            dataIndex: 'time_left'
                            //renderer: perc
                        },
                        {
                            text   : 'Time Allocated',
                            width    : 120,
                            sortable : true,
                            align: 'right',
                            dataIndex: 'time_allocated'
                            //renderer: perc
                        },
                        {
                            text   : 'Source',
                            width    : 95,
                            sortable : true,
                            align: 'right',
                            dataIndex: 'source'
                            //dataIndex: 'market %',
                            //renderer: perc
                        }
                    ],

                });
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

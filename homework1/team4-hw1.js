//TODO

//next button
//save and load json
var difficulty = 5;
var time = new Date();
var difset = [3,5,10,25,50,85,130,170,210,255];
var turnss = 10;
var totalRunningScore = 0;
var currentTurn = 1;

//lv 1 = 3 options
//lv 2 = 5 options
//lv 3 = 10 options
//lv 4 = 25 options
//lv 5 = 50 options
//lv 6 = 85 options
//lv 7 = 130 options
//lv 8 = 170 options
//lv 9 = 210 options
//lv 10 = 255 options

//Takes in R,G,B, outputs hex value
function hexFromRGB(r, g, b) {
    var hex = [
        r.toString(16),
        g.toString(16),
        b.toString(16)
    ];
    $.each(hex, function (nr, val) {
        if (val.length === 1) {
            hex[nr] = "0" + val;
        }
    });
    return hex.join("").toUpperCase();
}

//Update the sliders based on text input values
function refreshSwatch() {
    var red = $("#red").slider("value"),
        green = $("#green").slider("value"),
        blue = $("#blue").slider("value"),
        hex = hexFromRGB(red, green, blue);
    // $( "#swatch" ).css( "background-color", "#" + hex );
    $("input[name=redin]").val(hex[0] + hex[1]);
    $("input[name=greenin]").val(hex[2] + hex[3]);
    $("input[name=bluein]").val(hex[4] + hex[5]);
}


function percentDifferent(guessColor, expectedColor) { //example of call: var redOff = percentDifferent(rin, settings.color[0]+settings.color[1]);
    var guessColorInt, expectedColorInt;
    guessColorInt = parseInt(guessColor, 16); // Converting the color hex string into a integer
    expectedColorInt = parseInt(expectedColor, 16); // Converting the expected color hex string into a integer

    var percent_off = (Math.abs(guessColorInt - expectedColorInt) / 255) * 100;  // calculating each color Percentage off //
    percent_off = percent_off.toFixed(2);
    return percent_off;
}

function scoringFormula(redOff, blueOff, greenOff, difficulty, milliseconds_taken) { //example of call: var currentRoundScore = scoringFormula(redOff, blueOff, greenOff,difficulty, milliseconds_taken);
    var percent_off = (parseInt(redOff) + parseInt(blueOff) + parseInt(greenOff)) / 3;
    var currentRoundScore = ((15 - difficulty - percent_off) / (15 - difficulty)) * (15000 - milliseconds_taken); // this game is way too hard at 15 seconds

    if (currentRoundScore < 0) { //If the score would be less than zero for a color, it should be counted as zero.
        currentRoundScore = 0;
    }

    currentRoundScore = currentRoundScore.toFixed(2); // Scores should not have more than 2 points precision. (ie round to the nearest 100th)

    return currentRoundScore;
}

//Main plugin function
(function ($) {
    //Init
    $.fn.hexed = function (options) {
        //Get random values for RGB
        var colorR = Math.floor((Math.random() * 256));
        var colorG = Math.floor((Math.random() * 256));
        var colorB = Math.floor((Math.random() * 256));

        //Default values
        var settings = $.extend({
            // These are the defaults.
            color: hexFromRGB(colorR, colorG, colorB),
            difficulty: 5,
            turns: turnss
        }, options);

        //Start adding html for game

    	var totalTurns = settings.turns;
        $('#placeholder').append("<div style= 'text-align: center'> Round "  + currentTurn + " of " + settings.turns + "</div>");
        $('#placeholder').append('<div id="scoreArea"> Running Score: <div id="totalRunningScore"> ' + totalRunningScore + '</div></div><br>'); 

        $(this).append("<div id='game'> Guess This Color! </div>");
        $("#game").css("background-color", "rgb(" + colorR + "," + colorG + "," + colorB + ")");
        $(this).append("<div id='inputs'></div>")
        //add html for sliders
        $("#inputs").append("<br></br> Red:    <div id='red'></div>    <input type='text' name='redin'>");
        $("#inputs").append("<br></br> Green:  <div id='green'></div>  <input type='text' name='greenin'>");
        $("#inputs").append("<br></br> Blue:   <div id='blue'></div>   <input type='text' name='bluein'><br><br>");


        //Sliders are now added with css to make them functional
        //read difficulty level
        // read random red value
        // find difficulty value set length
        // pick random number of size of set
        // set lower bound of red bar
        // put it under the red bar left side
        // set higher bound of red bar
        // put it under the red bar right side

        //set red ranges
        //if max difficulty, set to full range
        if (difficulty == 10){
            redmax = 255;
            redmin = 0;
            redcent = 127;
        }
        //else set to smaller range
        else{
            //read the max level of variance from the difficulty
        var varied = difset[difficulty-1];
            //get random value to modulo and modulo it
        var redrand = Math.floor((Math.random() * 256));
        var redrand = redrand % varied;
            //set max and min from modulo
        var redmax = colorR + redrand;
        var redmin = colorR - (varied - redrand);
        //check edge cases
        if (redmax > 255){
            var diff = redmax-255;
            redmax = 255;
            redmin -= diff;
        }
        if (redmin < 0){
            var diff = Math.abs(redmin);
            redmin = 0;
            redmax += diff;
        }
        //set centerpoint
        var redcent = ((redmax-redmin)/2)+redmin;
        //console.log(redrand, redmax, redmin);
        }

        //set green ranges
        //if max difficulty, set to full range
        if (difficulty == 10){
            greenmax = 255;
            greenmin = 0;
            greencent = 127;
        }
        //else set to smaller range
        else{
            //read the max level of variance from the difficulty
        var varied = difset[difficulty-1];
            //get random value to modulo and modulo it
        var greenrand = Math.floor((Math.random() * 256));
        var greenrand = greenrand % varied;
            //set max and min from modulo
        var greenmax = colorG + greenrand;
        var greenmin = colorG - (varied - greenrand);
        //check edge cases
        if (greenmax > 255){
            var diff = greenmax-255;
            greenmax = 255;
            greenmin -= diff;
        }
        if (greenmin < 0){
            var diff = Math.abs(greenmin);
            greenmin = 0;
            greenmax += diff;
        }
        //set centerpoint
        var greencent = ((greenmax-greenmin)/2)+greenmin;
        //console.log(redrand, redmax, redmin);
        }


        //set blue ranges
        //if max difficulty, set to full range
        if (difficulty == 10){
            bluemax = 255;
            bluemin = 0;
            bluecent = 127;
        }
        //else set to smaller range
        else{
            //read the max level of variance from the difficulty
        var varied = difset[difficulty-1];
            //get random value to modulo and modulo it
        var bluerand = Math.floor((Math.random() * 256));
        var bluerand = bluerand % varied;
            //set max and min from modulo
        var bluemax = colorB + bluerand;
        var bluemin = colorB - (varied - bluerand);
        //check edge cases
        if (bluemax > 255){
            var diff = bluemax-255;
            bluemax = 255;
            bluemin -= diff;
        }
        if (bluemin < 0){
            var diff = Math.abs(bluemin);
            bluemin = 0;
            bluemax += diff;
        }
        //set centerpoint
        var bluecent = ((bluemax-bluemin)/2)+bluemin;
        //console.log(redrand, redmax, redmin);
        }


        $("#red").slider({
            orientation: "horizontal",
            range: "min",
            max: redmax,
            min: redmin,
            value: redcent,
            slide: refreshSwatch,
            change: refreshSwatch
        });
        $("#green").slider({
            orientation: "horizontal",
            range: "min",
            max: greenmax,
            min: greenmin,
            value: greencent,
            slide: refreshSwatch,
            change: refreshSwatch
        });
        $("#blue").slider({
            orientation: "horizontal",
            range: "min",
            max: bluemax,
            min: bluemin,
            value: bluecent,
            slide: refreshSwatch,
            change: refreshSwatch
        });

        //We call refreshSwatch to update the textboxes to each slider value
        refreshSwatch();
        //Create button for user
        $("#inputs").append("<button id='check' class='button'>Check values </button>");

        //When the user checks the input
        $("#check").click(function () {

            //Aquire values for red, green, blue from input
            var rin = $("input[name=redin]").val();
            var gin = $("input[name=greenin]").val();
            var bin = $("input[name=bluein]").val();
            //Result is the combination of RGB
            var result = rin + gin + bin;
            //Create a square in the color of the input color
            $(this).after("<div id='result'> " + result + " </div>");
            $("#result").css("background-color", "rgb(" + parseInt(rin, 16) + "," + parseInt(gin, 16) + "," + parseInt(bin, 16));
            //Calculate how far off we are from the expected RGB
            var redOff = percentDifferent(rin, settings.color[0] + settings.color[1]);
            var greenOff = percentDifferent(gin, settings.color[2] + settings.color[3]);
            var blueOff = percentDifferent(bin, settings.color[4] + settings.color[5]); // all 3 of these fuction calls called for Rin, I fixed them,

            var milliseconds_taken = new Date().getTime() - time.getTime(); // Use function to add time taken
            console.log(milliseconds_taken);
            var currentRoundScore = scoringFormula(redOff, blueOff, greenOff, settings.difficulty, milliseconds_taken);
            totalRunningScore = parseInt(currentRoundScore) + parseInt(totalRunningScore);
            totalRunningScore = parseInt(totalRunningScore).toFixed(2);
            $("#totalRunningScore").html(totalRunningScore);

            //Print out the % off for the user
      			$("#result").after("<br> This round's Score is " + currentRoundScore);
            $("#result").after("Your red was " + redOff + "% off. Your green was " + greenOff + "% off. Your blue was " + blueOff + "% off.");


      			$("#check").after('<button id="next_button" class="button">Next</button>'); //adding next button after check, when the check button is removed, the next button will replace it.
      			$("#next_button").click(function () {
      				$("#placeholder").html("");
			        $("#placeholder").hexed({});
            });

            //Check to see if the guess was correct
            if (result == settings.color) {
                alert("Success! You found the color");
            }
            //If not correct
            else {
                console.log("The correct color is: " + settings.color + " Input: " + result);
                //Next turn
                alert("You fail. You have " + (settings.turns - currentTurn) + " turns left. Good luck");

            }
            //No more turns
            if (settings.turns == currentTurn) {
                alert("Game Over, Your final score was " + totalRunningScore);
                $("#scoresubmit").css("display", "block");
            }
			      currentTurn = currentTurn + 1;

            $("#submit").click(function () {
                var player_name = $("#player").val();
                if (player_name != "") {
                    var data_obj = {
                        "playerName": player_name,
                        "difficulty": settings.difficulty,
                        "turns": settings.turns,
                        "score": totalRunningScore,
                        "timestamp": new Date()
                    };
                    localStorage.setItem(player_name, JSON.stringify(data_obj));
                }
                var retrievedObject = localStorage.getItem(player_name);
                console.log('retrievedObject: ', JSON.parse(retrievedObject));
            });

            $("#check").remove(); // Removing "check value" button after it has been clicked.
        });

        function check() {
            //Uncomment for easy debugging / ezwin
            // alert(settings.color);
        }

        check();

        //Called whenever an input box is changed
        //Changes sliders to match input
        $("input").change(function () {
            var value = this.value.substring(1);
            var rin = parseInt($("input[name=redin]").val(), 16);
            var gin = parseInt($("input[name=greenin]").val(), 16);
            var bin = parseInt($("input[name=bluein]").val(), 16);
            //Log user input to console
            console.log("R: ", rin, " B: ", gin, " C: ", bin);
            $("#red").slider("value", rin);
            $("#green").slider("value", gin);
            $("#blue").slider("value", bin);
        });

        this.css({
            color: settings.color,
            backgroundColor: settings.backgroundColor
        });
        return this;

    };

}(jQuery));
//Init
//This section is used to create the game.
$(function () {
    //When the button is clicked for the first time
    $("#random_color").click(function () {
        difficulty = $("input[name=difficulty]").val();

    		if (!(parseInt(difficulty) >= 1 &&  parseInt(difficulty) <= 10)) {
    			alert("Difficulty must be set from 1 to 10");
    			$("input[name=difficulty]").val(5);
    			return;
    		}

            turnss = $("input[name=turns]").val();
    		currentTurn = 1;

    		if (!(parseInt(turnss) >=1)) {
    			alert("Turns must be set to a positive number.");
    			$("input[name=turns]").val(10);
    			return;
    		}
            //Create a game section
            //Init plugin to game
        $("#placeholder").hexed({});

    });

    $("#random_color").click(function(){
        $("#b1").hide();
    });


    refreshSwatch();
});

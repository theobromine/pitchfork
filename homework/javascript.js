//TODO
//Create a timer
//Scoreboard: Move to javascript.js, add code to work with timer
//difficulty
//next button
//save and load json

var time = new Date();
var difset = [3,5,10,25,50,85,130,170,210,255]
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


var runningScore = 0;

function percentDifferent(guessColor, expectedColor) { //example of call: var redOff = percentDifferent(rin, settings.color[0]+settings.color[1]);
    var guessColorInt, expectedColorInt;
    guessColorInt = parseInt(guessColor, 16); // Converting the color hex string into a integer
    expectedColorInt = parseInt(expectedColor, 16); // Converting the expected color hex string into a integer

    var percent_off = (Math.abs(guessColorInt - expectedColorInt) / 255) * 100;  // calculating each color Percentage off //
    percent_off = percent_off.toFixed(2);
    return percent_off;
}

function scoringFormula(redOff, blueOff, greenOff, difficulty, milliseconds_taken) { //example of call: var finnalScore = scoringFormula(redOff, blueOff, greenOff,difficulty, milliseconds_taken);
    var percent_off = (parseInt(redOff) + parseInt(blueOff) + parseInt(greenOff)) / 3;
    var finnalScore = ((15 - difficulty - percent_off) / (15 - difficulty)) * (15000 - milliseconds_taken);

    if (finnalScore < 0) { //If the score would be less than zero for a color, it should be counted as zero.
        finnalScore = 0;
    }

    finnalScore = finnalScore.toFixed(2); // Scores should not have more than 2 points precision. (ie round to the nearest 100th)

    return finnalScore;
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
            backgroundColor: "MistyRose",
            difficulty: 5,
            turns: 10
        }, options);
        //Start adding html for game
        // $(this).append("\n\n<p>Color Game</p>Difficulty: <input type='text' name='difficulty' value='5'><br> Turns: <input type='text' name='turns' value='10'><br>");
        $(this).append("\n\n<h1 align='center'>Color Game</h1>");
        $(this).css("width", "80%", "margin", "0 auto");
        $(this).css("margin", "0 auto");
        $(this).css("padding", "10px 5px 10px 5px");

        $(this).append("<div id='game' style='height: 100px; width: 100px; text-align:center; margin: 0 auto;' > Guess This Color! </div>");
        $("#game").css("background-color", "rgb(" + colorR + "," + colorG + "," + colorB + ")");
        $(this).append("<div id='inputs' style='width: 70%; text-align:center; margin: 0 auto;''></div>")
        //add html for sliders
        $("#inputs").append("<br></br> Red:    <div id='red'></div>    <input type='text' name='redin'><br></br>  ");
        $("#inputs").append("<br></br> Green:  <div id='green'></div>  <input type='text' name='greenin'><br></br>");
        $("#inputs").append("<br></br> Blue:   <div id='blue'></div>   <input type='text' name='bluein'><br></br> ");


        //Sliders are now added with css to make them functional
        //read difficulty level
        // read random red value
        // find difficulty value set length
        // pick random number of size of set
        // set lower bound of red bar
        // put it under the red bar left side
        // set higher bound of red bar
        // put it under the red bar right side
        var difficulty = 1;

        var varied = difset[difficulty-1];
        var redrand = Math.floor((Math.random() * 256)); 
        var redrand = redrand % varied;
        var redmax = colorR + redrand;
        var redmin = colorR - (varied - redrand);
         console.log(redrand, redmax, redmin);
        


        $("#red").slider({
            orientation: "horizontal",
            range: "min",
            max: redmax,
            value: redmin,
            slide: refreshSwatch,
            change: refreshSwatch
        });
        $("#green").slider({
            orientation: "horizontal",
            range: "min",
            max: 255,
            value: 127,
            slide: refreshSwatch,
            change: refreshSwatch
        });
        $("#blue").slider({
            orientation: "horizontal",
            range: "min",
            max: 255,
            value: 127,
            slide: refreshSwatch,
            change: refreshSwatch
        });

        //We call refreshSwatch to update the textboxes to each slider value
        refreshSwatch();
        //Create button for user
        $("#inputs").append("<button id='check'>Check values </button>");

        //When the user checks the input
        $("#check").click(function () {

            //Aquire values for red, green, blue from input
            var rin = $("input[name=redin]").val();
            var gin = $("input[name=greenin]").val();
            var bin = $("input[name=bluein]").val();
            //Result is the combination of RGB
            var result = rin + gin + bin;
            //Create a square in the color of the input color
            $(this).after("<div id='result' style='height: 100px; width: 100px;' > " + result + " </div>");
            $("#result").css("background-color", "rgb(" + parseInt(rin, 16) + "," + parseInt(gin, 16) + "," + parseInt(bin, 16));
            //Calculate how far off we are from the expected RGB
            var redOff = percentDifferent(rin, settings.color[0] + settings.color[1]);
            var greenOff = percentDifferent(gin, settings.color[2] + settings.color[3]);
            var blueOff = percentDifferent(bin, settings.color[4] + settings.color[5]); // all 3 of these fuction calls called for Rin, I fixed them,

            var milliseconds_taken = new Date().getTime() - time.getTime(); // Use function to add time taken
            console.log(milliseconds_taken);
            var finnalScore = scoringFormula(redOff, blueOff, greenOff, settings.difficulty, milliseconds_taken);
            runningScore = finnalScore + runningScore;
            runningScore = parseInt(runningScore).toFixed(2);

            $("#runningScore").html(runningScore);

            //Print out the % off for the user
            $("#result").after("Your red was %" + redOff + " off. Your green was %" + greenOff + " off. Your blue was %" + blueOff + " off.");

            //WIP: Create an area to place the score, and a method to update it.
            // From the doc:
            //  After each guess, the score earned should be added to a visible running tally,
            //  along with how many points were earned for that color.
            //  If the score would be less than zero for a color,
            //  it should be counted as zero.  Scores should not have more than 2 points precision.
            //  (ie round to the nearest 100th)


            //Check to see if the guess was correct
            if (result == settings.color) {
                alert("Success! You found the color");
            }
            //If not correct
            else {
                console.log("The correct color is: " + settings.color + " Input: " + result);
                //Take one turn away
                settings.turns = settings.turns - 1;
                alert("You fail. You have " + settings.turns + " turns left. Good luck");
            }
            //No more turns
            if (settings.turns == 0) {
                alert("You really failed. GG no re");
            }

            //WIP: Create a next button, have it properly set the new color
            // From the doc:
            //  Clicking "Next" will present a new color, until the predetermined
            //  number of turns have passed, at which point the final score is
            //  presented and the user is prompted to play again (using the same
            //  or different settings).


            $("#submit").click(function () {
                var player_name = $("#player").val();
                if (player_name != "") {
                    var data_obj = {
                        "playerName": player_name,
                        "difficulty": settings.difficulty,
                        "turns": settings.turns,
                        "score": finnalScore,
                        "timestamp": new Date()
                    };
                    localStorage.setItem(player_name, JSON.stringify(data_obj));
                }
                var retrievedObject = localStorage.getItem(player_name);
                console.log('retrievedObject: ', JSON.parse(retrievedObject));
            });


            //WIP: Create an area to save our score.
            // From the doc:
            //  At the end of the game, provide a form for users to provide their
            //  name and save their score. Once the user clicks on the "Submit Score"
            //  button, use the Web Storage API to store a list of high scores as a
            //  JSON string in the user's localStorage (you'll have to parse and
            //  stringify the JSON each time you want to load and save the high score list).
            // Each high score should include the following, collected at the end of each game:
            //    Player Name
            //    Difficulty
            //    Turns
            //    Score
            //    Timestamp
            //WIP PART 2:
            //  Create a new page, Team#Scores.html, using HTML5.
            //  This page will read from localStorage to retrieve
            //  the high scores list, and print them in a neatly
            //  formatted table, sorted by score, then timestamp.


        });

        function check() {
            alert(settings.color);
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
    $("#random_color").one("click", (function () {
        //Create a game section
        //Init plugin to game
        $("#placeholder").hexed({
            difficulty: $("input[name=difficulty]").val(),
            turns: $("input[name=turns]").val()
        });
        // alert($("#game").hexed.settings);
        // console.log($("#game"));
    }));
    //If clicked a second time +
    $("#random_color").click(function () {
        var colorR = Math.floor((Math.random() * 256));
        var colorG = Math.floor((Math.random() * 256));
        var colorB = Math.floor((Math.random() * 256));
        // $("#game").css("background-color", "rgb(" + colorR + "," + colorG + "," + colorB + ")");

    });
    $("#check").click(function () {

    });


    // Css for sliders. Now not used as they are no longer in the html.
    // $( "#red, #green, #blue" ).slider({
    //     orientation: "horizontal",
    //     range: "min",
    //     max: 255,
    //     value: 127,
    //     slide: refreshSwatch,
    //     change: refreshSwatch
    //   });


    refreshSwatch();
});

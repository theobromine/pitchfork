//Takes in R,G,B, outputs hex value
function hexFromRGB(r, g, b) {
    var hex = [
      r.toString( 16 ),
      g.toString( 16 ),
      b.toString( 16 )
    ];
    $.each( hex, function( nr, val ) {
      if ( val.length === 1 ) {
        hex[ nr ] = "0" + val;
      }
    });
    return hex.join( "" ).toUpperCase();
  }

//Update the sliders based on text input values
function refreshSwatch() {
        var red = $( "#red" ).slider( "value" ),
          green = $( "#green" ).slider( "value" ),
          blue = $( "#blue" ).slider( "value" ),
          hex = hexFromRGB( red, green, blue );
        // $( "#swatch" ).css( "background-color", "#" + hex );
        $("input[name=redin]").val(hex[0]+hex[1]);
        $("input[name=greenin]").val(hex[2]+hex[3]);
        $("input[name=bluein]").val(hex[4]+hex[5]);
    }


//WIP
//Takes in two hex colors and returns the % difference.

//From the doc
// Percentage off is calculated as follow:
// (|expected value – actual value| / 255) * 100

function percentDifferent(guessColor, expectedColor){
  return 1;
}
//Main plugin function
(function ( $ ) {
    //Init
    $.fn.hexed = function( options ) {
        //Get random values for RGB
        var colorR = Math.floor((Math.random() * 256));
        var colorG = Math.floor((Math.random() * 256));
        var colorB = Math.floor((Math.random() * 256));

        //Default values
        var settings = $.extend({
            // These are the defaults.
            color: hexFromRGB(colorR, colorG, colorB),
            backgroundColor: "white",
            difficulty: 5,
            turns: 10
        }, options );
        //Start adding html for game
        // $(this).append("\n\n<p>Color Game</p>Difficulty: <input type='text' name='difficulty' value='5'><br> Turns: <input type='text' name='turns' value='10'><br>");
        $(this).append("\n\n<p>Color Game</p>");
        $(this).append("<div id='game' style='height: 100px; width: 100px;' > Guess This Color! </div>");
        $("#game").css("background-color", "rgb(" + colorR + "," + colorG + "," + colorB + ")");

        //add html for sliders
        $(this).append("<br></br> Red:    <div id='red'></div>    <input type='text' name='redin'><br></br>   </div>");
        $(this).append("<br></br> Green:  <div id='green'></div>  <input type='text' name='greenin'><br></br> </div>");
        $(this).append("<br></br> Blue:   <div id='blue'></div>   <input type='text' name='bluein'><br></br>  </div>");

        //Sliders are now added with css to make them functional
        $( "#red, #green, #blue" ).slider({
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
          $(this).append("<button id='check'>Check values </button>");

          //When the user checks the input
          $("#check").click( function(){
            //Aquire values for red, green, blue from input
            var rin = $("input[name=redin]").val();
            var gin = $("input[name=greenin]").val();
            var bin = $("input[name=bluein]").val();
            //Result is the combination of RGB
            var result = rin+gin+bin;
            //Create a square in the color of the input color
            $(this).after("<div id='result' style='height: 100px; width: 100px;' > "+result+" </div>");
            $("#result").css("background-color", "rgb("+parseInt(rin,16)+","+parseInt(gin,16)+","+parseInt(bin,16));
            //Calculate how far off we are from the expected RGB
            var redOff = percentDifferent(rin, settings.color[0]+settings.color[1]);
            var greenOff = percentDifferent(rin, settings.color[2]+settings.color[3]);
            var blueOff = percentDifferent(rin, settings.color[4]+settings.color[5]);
            //Print out the % off for the user
            $("#result").after("Your red was %" + redOff + " off. Your green was %"+ greenOff+ " off. Your blue was %"+blueOff+" off.");

            //WIP: Create an area to place the score, and a method to update it.
            // From the doc:
            //  After each guess, the score earned should be added to a visible running tally,
            //  along with how many points were earned for that color.
            //  If the score would be less than zero for a color,
            //  it should be counted as zero.  Scores should not have more than 2 points precision.
            //  (ie round to the nearest 100th)


            //Check to see if the guess was correct
            if (result == settings.color){
              alert("Sucess! You found the color");
            }
            //If not correct
            else {
              console.log("The correct color is: " + settings.color + " Input: " + result );
              //Take one turn away
              settings.turns = settings.turns - 1;
              alert("You fail. You have " + settings.turns + " turns left. Good luck");
            }
            //No more turns
            if(settings.turns == 0){
              alert("You really failed. GG no re");
            }

            //WIP: Create a next button, have it properly set the new color
            // From the doc:
            //  Clicking "Next" will present a new color, until the predetermined
            //  number of turns have passed, at which point the final score is
            //  presented and the user is prompted to play again (using the same
            //  or different settings).



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

          function check(){
            alert(settings.color);
          }
          check();

          //Called whenever an input box is changed
          //Changes sliders to match input
          $("input").change(function () {

            var value = this.value.substring(1);
            var rin = parseInt($("input[name=redin]").val(),16);
            var gin = parseInt($("input[name=greenin]").val(),16);
            var bin = parseInt($("input[name=bluein]").val(),16);
            console.log(rin, "B, ", gin, "C", bin);
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

}( jQuery ));
//Init
//This section is used to create the game.
$(function() {
  //When the button is clicked for the first time
  $("#random_color").one("click", (function() {
      //Create a game section
      //Init plugin to game
      $( "#placeholder" ).hexed({
          difficulty: $("input[name=difficulty]").val(),
          turns: $("input[name=turns]").val()
      });
      // alert($("#game").hexed.settings);
      // console.log($("#game"));
  }));
  //If clicked a second time +
  $("#random_color").click(function() {
    var colorR = Math.floor((Math.random() * 256));
    var colorG = Math.floor((Math.random() * 256));
    var colorB = Math.floor((Math.random() * 256));
    // $("#game").css("background-color", "rgb(" + colorR + "," + colorG + "," + colorB + ")");

  });
  $("#check").click(function() {

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

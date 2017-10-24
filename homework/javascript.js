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
        $(this).before("\n\n<p>Color Game</p>Difficulty: <input type='text' name='difficulty' value='5'><br> Turns: <input type='text' name='turns' value='10'><br>");
        //add html for sliders
        $(this).after(" <br></br>Blue: <div id='blue'> </div> <input type='text' name='bluein'><br></br>  </div>");
        $(this).after("<br></br> Green: <div id='green'> </div> <input type='text' name='greenin'><br></br>  </div>\n");
        $(this).after("<br></br>Red: <div id='red'> </div> <input type='text' name='redin'><br></br> </div>\n");
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
          //Create input for user
          $(this).after(" <input type='text' name='guess' value='Enter Hex Here'><br></br>  </div>");
          $(this).after("<button id='check'>Check values </button>");

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
            var redOff;
            var greenOff;
            var blueOff;
            $("#result").after("You were % " + + " SEttings: " + settings.color );
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
$(function() {
  //When the button is clicked for the first time
  $("#random_color").one("click", (function() {
      //Create a game section
      $(this).after("<div id='game' style='height: 100px; width: 100px;' > test </div>");
      //Init plugin to game
      $( "#game" ).hexed({
          difficulty: $("input[name=difficulty]").val(),
          turns: $("input[name=turns]").val()
      });
      // alert($("#game").hexed.settings);
      console.log($("#game"));
  }));
  //If clicked a second time +
  $("#random_color").click(function() {
    var colorR = Math.floor((Math.random() * 256));
    var colorG = Math.floor((Math.random() * 256));
    var colorB = Math.floor((Math.random() * 256));
    $("#game").css("background-color", "rgb(" + colorR + "," + colorG + "," + colorB + ")");

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

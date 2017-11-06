Team Members: 
 Isaac Llewellyn, SummerRay A. Morrow, Elisa Franssen, Ruowen Qin, Sydney Ruzicka

 Readme Author: Elisa Franssen



1) What are the advantages to writing a jQuery plugin over regular JavaScript that uses jQuery?

If one creates a plugin, the plugin can be used on any number of webpages without having to customize it for each. Furthermore, if one needs to edit functionality, then editing the plugin can allow the user to fix a problem with all instances of the jQuery, rather than having to manually do it to each. 

2) Explain how your jQuery plugin adheres to best practices in JavaScript and jQuery development.

Our plugin adheres to best practices by keeping everything succinct, by making it so all javascript is external to the html, requiring only the button and initial input fields be present in the html to run the plugin. Variables remain within the scope of the html document only, and we utilize functions where available to simplify aspects of the plugin. 

3) Does anything prevent you from POSTing high scores to a server on a different domain? If so, what? If not, how would we go about it (written explanation/pseudocode is fine here)?

Yes. Javascript abides from the same origin policy, making it so a script from one origin cannot interact with resources from another origin without very specific permisisons. If one would do it, we could use AJAX to cross-origin resource share to send a request from the other domain. If approved and authenticated, the other domain can accept the POST. 

4) Now that you've used Web Storage, what other information would you store there in other Web-based applications? Is there any information you wouldn't store?

It depends on the site. I would primarily store only basic things, as in some implementations I would not want others to send false info or damage my computer. Because ours seeks only set types of values and is parsed to json, i dont fear this as much, but would still worry about individuals maliciously sending fake scores. Anything I ( or my users) wouldn't want recived and viewed by the website I would not store. 
// This file deals with the creation of Grid and some important tasks

$(document).ready(function() {
  $(window).on('load',function() {setTimeout(function () { $('html,body').scrollTop(0) },1); });
  $('[data-toggle="tooltip"]').tooltip();  
  //creating grid
  const svg1 = document. createElementNS("http://www.w3.org/2000/svg", "svg");
  // set width and height
  svg1.setAttribute("id", "work-area");
  svg1.setAttribute("width", "1920");
  svg1.setAttribute("height", "1080");
  svg1.setAttribute("style","overflow: hidden; position: relative;background-color: rgba(0, 0, 0, 0.65);"); 
  svg1.setAttribute("viewBox","0 0 1920 1080");

  // create a rectangle
  var i,j;
  for(i=0;i<1920;i=i+30){
    for(j=0;j<1080;j=j+30){
      const rect1 = document. createElementNS("http://www.w3.org/2000/svg", "rect");
      if(i===420 && j===360){
        rect1.setAttribute("id","start");
      }else if(i===720 && j==360){
        rect1.setAttribute("id","end");
      }else{
        rect1.setAttribute("class","box");
      }
      rect1.setAttribute("x",i.toString());
      rect1.setAttribute("y",j.toString());
      rect1.setAttribute("name",i.toString()+" "+j.toString());
      svg1.appendChild(rect1);
    }
  }


  // attach svg to div
  document. getElementById("svg-area").appendChild(svg1);
  //fade in effect for svg-area
  $("body").fadeIn("slow");

});

// for applying css styles to grid
var linkElement = document.createElement("link");
linkElement.rel = "stylesheet";
linkElement.href="/static/css/box.css"; //Replace here
document.head.appendChild(linkElement);


//This file deals with the onClick functions of all choice buttons in the app

// In order to change button color on click
function changeColor(self){
  $("button").removeClass("active1");
  $(self).addClass("active1");
}

//to remove existing addEventListeners
function removeAllEventListeners() {
  var el = document.getElementById("svg-area"),
  elClone = el.cloneNode(true);
  el.parentNode.replaceChild(elClone, el);
  return;
}

// to replace the event.target with start position
function getStartTarget(event) {
  var startElem = document.getElementById("start");
  var endElem = document.getElementById("end");
  var elem = event.target;
  var port1 = document.getElementById("port-1");
  var port2 = document.getElementById("port-2");
  if (elem != endElem && elem != port1 && elem != port2) {
      startElem.removeAttribute("id");
      startElem.setAttribute("class", "box");
      elem.removeAttribute("class");
      elem.setAttribute("id", "start");
    
  }
}


//when start button is clicked
function setStart() {
  changeColor(document.getElementById("set-start-button"));
  removeAllEventListeners();
  let svgElem = document.querySelector("#svg-area");
  svgElem.addEventListener("mousedown", getStartTarget.bind(event));
}

//when end button is clicked
function setEnd() {
  changeColor(document.getElementById("set-end-button"));
  removeAllEventListeners();
  let svgElem = document.querySelector("#svg-area");
  svgElem.addEventListener("mousedown", function(e, svgElem) {
    var startElem = document.getElementById("start");
    var endElem = document.getElementById("end");
    var port1 = document.getElementById("port-1");
    var port2 = document.getElementById("port-2");
    var elem = event.target;
    if (elem != startElem && elem != port1 && elem != port2) {
        endElem.removeAttribute("id");
        endElem.setAttribute("class", "box");
        elem.removeAttribute("class");
        elem.setAttribute("id", "end");
      
    }
  });
}

// Native js function which allows to click n' drag over the grid
function makeDraggable(class1,class2) {
  let svgElem = document.querySelector("#svg-area");
  svgElem.addEventListener('mousedown', startDrag);
  svgElem.addEventListener('mousemove', drag);
  svgElem.addEventListener('mouseup', endDrag);
  // svg.addEventListener('mouseleave', endDrag);
  var selectedElement = false;
  var str1 = class1;
  var str2 = class2;
  function startDrag(evt) {
    if (evt.target.getAttribute("class") == str1) {
      evt.target.setAttribute("class", str2);
    }
    if (selectedElement == false) {
      selectedElement = true;
    } else {
      selectedElement = false;
    }
  }

  function drag(evt) {
    if (selectedElement == true)
    {
      if (evt.target.getAttribute("class") == str1) {
        evt.target.setAttribute("class", str2);
      }
    }
  }

  function endDrag(evt) {
    selectedElement = false;
  }
}

//when set blocks is clicked
function setBlocks() {
  changeColor(document.getElementById("set-block-button"));
  removeAllEventListeners();
  makeDraggable("box","block");
  makeDraggable("visited","block");
  makeDraggable("path","block");
}

//when erase blocks is clicked
function setEraseBlocks() {
  changeColor(document.getElementById("set-erase-button"));
  removeAllEventListeners();
  makeDraggable("block","box");
}

//when clear Blocks is clicked
function clearBlocks() {
  changeColor(document.getElementById("set-clear-button"));
  removeAllEventListeners();
  var x=document.querySelectorAll(".block");
  x.forEach(function(item){
    item.setAttribute("class","box")
  });
}

// For removing the ports from the grid
function removePorts(){
  var elem1 = document.getElementById("port-1");
  var elem2 = document.getElementById("port-2");
  if(elem1 && elem2){
    elem1.removeAttribute("id");
    elem2.removeAttribute("id");
    elem1.setAttribute("class", "box");
    elem2.setAttribute("class", "box");
  }
}


//For adding ports to the Grid
function setInitialPorts(){
  removePorts();
  var startElem = document.getElementById("start");
  var endElem = document.getElementById("end");

  var position1 = "480 360";
  var selection1 = document.querySelector(`rect[name="${position1}"]`);
  if(selection1 != startElem && selection1 != endElem){ 
    selection1.removeAttribute("class");
    selection1.setAttribute("id", "port-1");
  }
  else{
    var s = 510, t =390;
    while(selection1 == startElem || selection1 == endElem){
      var sample_str = s.toString() + " " +t.toString();
      selection1 = document.querySelector(`rect[name="${sample_str}"]`);
      s += 30;
      t += 30;
    }
    selection1.removeAttribute("class");
    selection1.setAttribute("id", "port-1");
  }

  var position2 = "660 360";
  var selection2 = document.querySelector(`rect[name="${position2}"]`);
  if(selection2 != startElem && selection2 != endElem){ 
    selection2.removeAttribute("class");
    selection2.setAttribute("id", "port-2");
  }
  else{
    var s = 690, t =390;
    while(selection2 == startElem || selection2 == endElem){
      var sample_str = s.toString() + " " +t.toString();
      selection2 = document.querySelector(`rect[name="${sample_str}"]`);
      s += 30;
      t += 30;
    }
    selection2.removeAttribute("class");
    selection2.setAttribute("id", "port-2");
  }
  
  
}

//When set Port-1 is clicked

function setPort1(){
  changeColor(document.getElementById("port-1-button"));
  removeAllEventListeners();
  let svgElem = document.querySelector("#svg-area");
  svgElem.addEventListener("mousedown", function(e, svgElem) {
    var startElem = document.getElementById("start");
    var endElem = document.getElementById("end");
    var prevPort = document.getElementById("port-1")
    var port2 = document.getElementById("port-2");
    var elem = event.target;
    if(elem != startElem && elem != endElem && elem != port2){
      prevPort.removeAttribute("id");
      prevPort.setAttribute("class", "box");
      elem.removeAttribute("class");
      elem.setAttribute("id", "port-1");
    }
  });

  
}

//when set Port-2 is clicked

function setPort2(){
  changeColor(document.getElementById("port-2-button"));
  removeAllEventListeners();
  let svgElem = document.querySelector("#svg-area");
  svgElem.addEventListener("mousedown", function(e, svgElem) {
    var startElem = document.getElementById("start");
    var endElem = document.getElementById("end");
    var prevPort = document.getElementById("port-2")
    var port1 = document.getElementById("port-1");
    var elem = event.target;
    if(elem != startElem && elem != endElem && elem != port1){
      prevPort.removeAttribute("id");
      prevPort.setAttribute("class", "box");
      elem.removeAttribute("class");
      elem.setAttribute("id", "port-2");
    }
  });
  
}
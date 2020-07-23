//this file deals with the onClick functions of the buttons in the control-panel

var my_arr = null;
var my_path = null;
var time = null;
var stop = false;

//to remove existing addEventListeners
function removeAllEventListeners() {
  var el = document.getElementById("svg-area"),
  elClone = el.cloneNode(true);
  el.parentNode.replaceChild(elClone, el);
  return;
}

// to change button color on click
function changeColorOnClick(self){
  $("button").removeClass("active2");
  $(self).addClass("active2");
}

// to get the Selected Heuristic
function getSelectedHeuristic(name){
  const selection = document.querySelector(`input[name="${name}"]:checked`);
  if (selection){
    return selection.value;
  }
  else return -1;
}

// to get the enabled options
function getSelectedCheckboxValues(name) {
    const checkboxes = document.querySelectorAll(`input[name="${name}"]:checked`);
    let values = [];
    checkboxes.forEach((checkbox) => {
        values.push(checkbox.value);
    });
    return values;
}

// to get the weight, if present
function getInputFromTextBox(name){
  const selection = document.getElementById(name);
  if (selection){
    return selection.value;
  }
  else return 0;
}

// a function which collects all the Grid data and stores them in a dictionary
function getGridData(){
  var x = document.querySelectorAll('button.algo-button:not(.collapsed)');
  if(x.length === 0){
    alert("Please select an algorithm");
    toggleChoiceButtons(true);
    return -1;
  }
  var start = {
    x: document.getElementById("start").getAttribute("x").toString(),
    y: document.getElementById("start").getAttribute("y").toString(),
  };
  var end = {
    x: document.getElementById("end").getAttribute("x").toString(),
    y: document.getElementById("end").getAttribute("y").toString(),
  };
  var blocks = document.getElementsByClassName("block");
  var blocks_dict = {};
  for(var i=0;i<blocks.length;i=i+1){
    blocks_dict["x"+i.toString()] = blocks[i].getAttribute("x");
    blocks_dict["y"+i.toString()] = blocks[i].getAttribute("y");
  }

  var heuristic = getSelectedHeuristic(x[0].getAttribute("id")+'heuristics');
  var options = getSelectedCheckboxValues(x[0].getAttribute("id")+'options');
  var weight = getInputFromTextBox(x[0].getAttribute("id")+'weight');
  var ports;

  if(x[0].getAttribute("id") == "Teleport"){
    var port1 = {
      x: document.getElementById("port-1").getAttribute("x").toString(),
      y: document.getElementById("port-1").getAttribute("y").toString(),
    };
    var port2 = {
      x: document.getElementById("port-2").getAttribute("x").toString(),
      y: document.getElementById("port-2").getAttribute("y").toString(),
    };
    ports = [port1, port2];
  }
  else{
    ports = [];
  }

  var entry = {
    algo: x[0].getAttribute("id"),
    start: start,
    end: end,
    heuristic: heuristic,
    blocks: blocks_dict,
    options: options,
    weight: weight,
    ports: ports
  };
  return entry;
}


// Native JS function for Sleep operation
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
 }

// for updating the UI with the path found
async function animate(){
  if(my_arr){
    if(my_arr[0] != "bidirectional"){
      for (var i=0;stop!=true && i<my_arr.length;i++){
      var position = my_arr[i];
      await sleep(5);
      var selection = document.querySelector(`rect[name="${position}"]`);
      if(stop!=true){
        selection.setAttribute("class","visited");
      }
      

      }
    }
    else{
      for(var i=j=0 ;stop!=true && i<my_arr[1].length && j<my_arr[2].length ;i++,j++){
        var position1 = my_arr[1][i];
        var position2 = my_arr[2][j];
        await sleep(10);
        var selection1 = document.querySelector(`rect[name="${position1}"]`);
        var selection2 = document.querySelector(`rect[name="${position2}"]`);
        if(stop!=true){
          selection1.setAttribute("class","visited");
          selection2.setAttribute("class","visited");
        }

      }
    }
  }
  if(my_path){
    if(my_path[0] != "two-paths"){
      my_str = "M"
      for (var i=0; i<my_path.length;i++){
        var position = my_path[i];
        // await sleep(2);
        var selection = document.querySelector(`rect[name="${position}"]`);
        position = position.replace(" ",",");
        my_str+=position
        if (i<(my_path.length)-1){
          my_str+="L"
        }
        selection.setAttribute("class","path");
      }
      const line = document.createElementNS("http://www.w3.org/2000/svg", "path");
      line.setAttribute("fill","none");
      line.setAttribute("id","line");
      line.setAttribute("transform","translate(15,15)");
      line.setAttribute("stroke","#ffffff");
      line.setAttribute("stroke-dasharray","15, 7");
      line.setAttribute("stroke-width","5px");
      line.setAttribute("stroke-linejoin","round");
      line.setAttribute("d",my_str);
      var elem = document.getElementById("work-area");
      elem.appendChild(line);
      showResults(line.getTotalLength() / 30);
      $("#line").fadeOut(400).fadeIn(400).fadeOut(400).fadeIn(400).fadeOut(400).fadeIn(400).fadeOut(400).fadeIn(400);
    }
    else{
      var my_str1 = "M";
      for (var i=0; i<my_path[1].length;i++){
        var position = my_path[1][i];
        // await sleep(2);
        var selection = document.querySelector(`rect[name="${position}"]`);
        position = position.replace(" ",",");
        my_str1+=position
        if (i<(my_path[1].length)-1){
          my_str1+="L"
        }
        selection.setAttribute("class","path");
      }

      var my_str2 = "M";
      for (var i=0; i<my_path[2].length;i++){
        var position = my_path[2][i];
        // await sleep(2);
        var selection = document.querySelector(`rect[name="${position}"]`);
        position = position.replace(" ",",");
        my_str2+=position
        if (i<(my_path[2].length)-1){
          my_str2+="L"
        }
        selection.setAttribute("class","path");
      }

      const line1 = document.createElementNS("http://www.w3.org/2000/svg", "path");
      const line2 = document.createElementNS("http://www.w3.org/2000/svg", "path");

      line1.setAttribute("fill","none");
      line2.setAttribute("fill","none");

      line1.setAttribute("id","line1");
      line2.setAttribute("id","line2");

      line1.setAttribute("transform","translate(15,15)");
      line2.setAttribute("transform","translate(15,15)");

      line1.setAttribute("stroke","#ffffff");
      line2.setAttribute("stroke","#ffffff");

      line1.setAttribute("stroke-dasharray","15, 7");
      line2.setAttribute("stroke-dasharray","15, 7");

      line1.setAttribute("stroke-width","5px");
      line2.setAttribute("stroke-width","5px");

      line1.setAttribute("d",my_str1);
      line2.setAttribute("d",my_str2);


      var elem = document.getElementById("work-area");
      elem.appendChild(line1);
      elem.appendChild(line2);
      showResults((line1.getTotalLength() / 30)+(line2.getTotalLength() / 30));

      var lastElem1 = my_path[1][my_path[1].length-1];
      var temp = document.querySelector(`rect[name="${lastElem1}"]`);
      if(temp.getAttribute("id") == "port-1" || temp.getAttribute("id") == "port-2"){
        lastElem1 = lastElem1.replace(" ",",");
        var firstElem2 = my_path[2][0];
        firstElem2 = firstElem2.replace(" ",",");
        var new_str = "M";
        new_str = new_str + lastElem1 + "L" + firstElem2;
        const portLine = document.createElementNS("http://www.w3.org/2000/svg", "path");
        portLine.setAttribute("fill","none");
        portLine.setAttribute("id","portLine");
        portLine.setAttribute("transform","translate(15,15)");
        portLine.setAttribute("stroke","rgb(255, 72, 0)");
        portLine.setAttribute("stroke-dasharray","7, 7");
        portLine.setAttribute("stroke-width","8px");
        portLine.setAttribute("d",new_str);
        var elem = document.getElementById("work-area");
        elem.appendChild(portLine);
        $("#portLine").fadeOut(400).fadeIn(400).fadeOut(400).fadeIn(400).fadeOut(400).fadeIn(400).fadeOut(400).fadeIn(400).fadeOut(400).fadeIn(400).fadeOut(400).fadeIn(400).fadeOut(400).fadeIn(400).fadeOut(400).fadeIn(400).fadeOut(400).fadeIn(400).fadeOut(400).fadeIn(400);

      }
      
      
    }
    

  }

}

function showResults(len){
  toggleChoiceButtons(true);
  var pathLength = len;
  var elem = document.getElementById("results");
  $("#results").fadeIn("slow");
  elem.innerHTML = `<div>Path Length: `+pathLength.toFixed(1).toString()+`</div>\n`+`<div>Time   : `+time.toFixed(1).toString()+ ` ms</div>`;
}

// For clearing the Grid
function removeAnimationPatch(){
  var elem = document.getElementById("results");
  $("#results").fadeOut();  

  if(my_arr){
    if(my_arr[0] != "bidirectional"){
      for (var i=0; i<my_arr.length;i++){
        var position = my_arr[i];
        var selection = document.querySelector(`rect[name="${position}"]`);
        if(selection.getAttribute("class") == "visited"){
          selection.setAttribute("class","box");
        }
      }
    }
    else{
      for(var i=j=0;i<my_arr[1].length&&j<my_arr[2].length;i++,j++){
        var position1 = my_arr[1][i];
        var position2 = my_arr[2][j];
        var selection1 = document.querySelector(`rect[name="${position1}"]`);
        var selection2 = document.querySelector(`rect[name="${position2}"]`);
        if(selection1.getAttribute("class") == "visited"){
          selection1.setAttribute("class","box");
        }
        if(selection2.getAttribute("class") == "visited"){
          selection2.setAttribute("class","box");
        }
      }
    }
  }
  my_arr = null;
  if(my_path){
    if(my_path[0] != "two-paths"){
      var pathLine = document.getElementById("line");
      if(pathLine){
      pathLine.remove();
      }
      for (var i=0; i<my_path.length;i++){
        var position = my_path[i];
        var selection = document.querySelector(`rect[name="${position}"]`);
        if(selection.getAttribute("class") == "path"){
        selection.setAttribute("class","box");
        }
      }
    }
    else{
      document.getElementById("line1").remove();
      document.getElementById("line2").remove();
      document.getElementById("portLine").remove();
      for (var i=0; i<my_path[1].length;i++){
        var position = my_path[1][i];
        var selection = document.querySelector(`rect[name="${position}"]`);
        if(selection.getAttribute("class") == "path"){
        selection.setAttribute("class","box");
        }
      }
      for (var i=0; i<my_path[2].length;i++){
        var position = my_path[2][i];
        var selection = document.querySelector(`rect[name="${position}"]`);
        if(selection.getAttribute("class") == "path"){
        selection.setAttribute("class","box");
        }
      }
    }
    
  }
  my_path = null;

}

// for enabling/disabling choice buttons
function toggleChoiceButtons(state){
  var c = document.querySelectorAll(".choice-buttons");
  if(state == true)
  {
    c.forEach(function(i) {
    i.removeAttribute("disabled");
  });
  }
  else
  {
    c.forEach(function(i) {
    i.setAttribute("disabled", true);
  });
  }
}

// when Start Search is clicked
function startSearch(){
  removeAllEventListeners();
  $("button").removeClass("active1");
  $('[data-toggle="tooltip"]').tooltip("hide");  
  stop = false;
  toggleChoiceButtons(false);
  removeAnimationPatch();
  changeColorOnClick(document.getElementById("start-button"));
  var x = getGridData();
  if(x === -1){
    return;
  }
  var req = $.ajax({
    url: "get_data",
    type: "POST",
    data: JSON.stringify(x),
    dataType: "json",
    contentType: "application/json",
    success: function(resp){
        my_arr = resp['traversal'];
        my_path = resp['path'];
        time = resp['time'];
        animate();
    }
  });
  
}

// When clear search is clicked
function clearPath(){
  changeColorOnClick(document.getElementById("clear-path-button"));
  removeAnimationPatch();
}

// when Cancel Search is clicked
function cancelSearch(){
  changeColorOnClick(document.getElementById("cancel-button"));
  stop = true;
  toggleChoiceButtons(true);
  removeAnimationPatch();
}

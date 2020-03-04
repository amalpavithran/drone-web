let forward = document.getElementById('forward');
let backward = document.getElementById('backward');
let left = document.getElementById('left');
let right = document.getElementById('right');
let rotate = document.getElementById('rotate');

function delay();
function resetval(obj)=>{
    while(obj.value!=50){
        setTimeout(delay,500);
        
    }
}

$(function() {
  
    // Set the command-line prompt to include the user's IP Address
    //$('.prompt').html('[' + codehelper_ip["IP"] + '@HTML5] # ');
      $('.prompt').html('[user@HTML5] # ');
  
    // Initialize a new terminal object
    var term = new Terminal('#input-line .cmdline', '#container output');
    term.init();
    
    // Update the clock every second
    setInterval(function() {
      function r(cls, deg) {
        $('.' + cls).attr('transform', 'rotate('+ deg +' 50 50)')
      }
      var d = new Date()
      r("sec", 6*d.getSeconds())  
      r("min", 6*d.getMinutes())
      r("hour", 30*(d.getHours()%12) + d.getMinutes()/2)
    }, 1000);
    
});
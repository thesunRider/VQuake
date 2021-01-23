var divs = ["Div1", "Div2", "Div3", "Div4", "Div5", "Div6","Div7"];
var clientserial;

    var visibleDivId = null;
    
function queryandhide_urlfilter(divId){
  divVisibility(divId);
  queryserver_urlfilter();
}

    function divVisibility(divId) {
      if(visibleDivId === divId) {
        visibleDivId = divId;
      } else {
        visibleDivId = divId;
      }
      hideNonVisibleDivs();
    }

    function hideNonVisibleDivs() {
      var i, divId, div;
      for(i = 0; i < divs.length; i++) {
        divId = divs[i];
        div = document.getElementById(divId);
        if(visibleDivId === divId) {
          div.style.display = "";
        } else {
          div.style.display = "none";
        }
      } $(".connection").css("overflow", "auto");
    }

    window.addEventListener('pywebviewready', function() {
      console.log('Re-established connection');
    })


    function quit() {
    console.log('quiting');
     pywebview.api.quit();
    }

    function registerserial(serial){
      clientserial = serial;
    }

    function queryserver_urlfilter(){
      //the ending .then is necessary since this is a promise 
      pywebview.api.get_urlblocked(clientserial).then(function(response) {
          resp = JSON.parse(response);
          var injectml = '';
          for (var i = 0; i < resp.length; i++) {
            injectml += '<tr class="priority-300"> <td class="name">'+resp[i].url +'</td></tr>';
          }

          document.getElementById('urlfilter_base').innerHTML +=  injectml;
      });
    }

    function catchException() {
        pywebview.api.error().catch(showResponse);
    }
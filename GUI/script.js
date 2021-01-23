var divs = ["Div1", "Div2", "Div3", "Div4", "Div5", "Div6","Div7"];
    var visibleDivId = null;
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

    function catchException() {
        pywebview.api.error().catch(showResponse);
    }
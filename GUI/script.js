var divs = ["Div1", "Div2", "Div3", "Div4"];
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
          div.style.display = "block";
        } else {
          div.style.display = "none";
        }
      }
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
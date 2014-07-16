function showHide(shID) {
   if (document.getElementById(shID)) {
      if (document.getElementById(shID).style.display != 'block') {
         document.getElementById(shID).style.display = 'block';
	  document.getElementById(shID+'-show').className = "hideLink";
	  console.log(document.getElementById(shID).className);
      }
      else {
         document.getElementById(shID).style.display = 'none';
	  document.getElementById(shID+'-show').className = "showLink";
      }
   }
}
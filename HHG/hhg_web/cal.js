function init_cal() {
	dayslist = document.getElementsByTagName("time")
	for (var i=0;i<dayslist.length;i++) {
		dayslist[i].onmouseover=function(){
			document.getElementById("t").innerHTML=this.id;
		}
	}
	document.getElementById("scrollview").scrollTop = document.getElementById("scrollview").scrollHeight;
}

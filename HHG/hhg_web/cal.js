function init_cal() {
	dayslist = document.getElementsByTagName("time")
	for (var i=0;i<dayslist.length;i++) {
		dayid = dayslist[i].getAttribute("dayid")
		if (!eval("typeof dn"+dayid+" === 'undefined'")) {
			eval("dn = dn"+dayid)
			eval("da = da"+dayid)
			new Chart(document.getElementById("dvn"+dayid).getContext("2d")).Bar(dn,{});
			new Chart(document.getElementById("dva"+dayid).getContext("2d")).Line(da,{});
		}
		dayslist[i].onmouseover=function(){
			document.getElementById("t").innerHTML=this.id;
		}
		dayslist[i].onmousedown=function(){
			window.open ('./'+this.getAttribute("dayid")+'/index.html?strtt=0'+
					'&stopt=86400&dayid='+this.getAttribute("dayid"),'_self',false)
		}
	}
	document.getElementById("scrollview").scrollTop = document.getElementById("scrollview").scrollHeight;
}

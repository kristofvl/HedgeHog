function init_cal() {
	dayslist = document.getElementsByTagName("time")
	for (var i=0;i<dayslist.length;i++) {
		dayid = dayslist[i].getAttribute("dayid")
		if (!eval("typeof ps"+dayid+" === 'undefined'")) { // data?
			eval('var dn'+dayid+'={l:[],ds:[{fc:"#dd0",sc:"#ddd",d:ls'+dayid+'},{fc:"#000",sc:"#ddd",d:ps'+dayid+'}]};')
			eval('var da'+dayid+'={l:[],ds:[{sc:"#d00",d:xs'+dayid+'},{sc:"#0a0",d:ys'+dayid+'},{sc:"#00d",d:zs'+dayid+'}]};')
			var lcanv = document.createElement("canvas");
			var acanv = document.createElement("canvas");
			lcanv.setAttribute('width',160)
			acanv.setAttribute('width',160)
			lcanv.setAttribute('height',30)
			acanv.setAttribute('height',63)
			lcanv.setAttribute('id','"dvn'+dayid+'"')
			acanv.setAttribute('id','"dva'+dayid+'"')
			lcanv.setAttribute('style','position:absolute;top:14px;')
			acanv.setAttribute('style','position:absolute;top:42px;')
			dayslist[i].appendChild(lcanv);
			dayslist[i].appendChild(acanv);
			new Chart(lcanv.getContext("2d")).Bar(eval("dn"+dayid),{});
			new Chart(acanv.getContext("2d")).Line(eval("da"+dayid),{});
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

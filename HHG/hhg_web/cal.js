var monthns = ["January", "February", "March", "April","May","June",
	"July","August","September","October","November","December"];

var start_day = -1
var scrollTO = null;

// fills the month table with numbers
function fill_table(month,year)
{ 
  day=1
  if (start_day==-1) 
	start_day=(new Date(year,month,1)).getDay()
  stop_day=(new Date(year,month+1,0)).getDate()
  document.write("<td><table class='calm' cellspacing=0><tr>")
  document.write("<td colspan=7><b>"+monthns[month]+" "+year+"</b><tr>")
  if (start_day==8) 
	start_day=1
  for (var i=1;i<start_day;i++){
        document.write("<td></td>")
  }
  for (var i=start_day;i<8;i++){
        document.write("<td>"+day+"</td>")
        day++
  }
  document.write("</tr>")
  while (day <= stop_day) {
     for (var i=1;i<=7 && day<=stop_day;i++){
         document.write("<td>"+day+"</td>")
         day++
     }
     document.write("</tr><tr>")
  }
  if (start_day-1+stop_day<36)
	document.write("</tr><tr><td></td>")
  start_day = i
  document.write("</tr></table></td>")
}

function addMonthBrowser(year) {
	document.write('<div id="ycal" style="display:none;"><table class="calt"><tr>')
	for (var i=0; i<12; i++) {
		fill_table(i,year)
		if ((i+1)%4==0)
			document.write("</tr><tr>")
	}
	document.write("</tr></table>")
	document.write("</div>")
}

function browseMonth(){
	if (document.getElementById('ycal').style.display=="none")
		document.getElementById('ycal').style.display="inline-block"
	else
		document.getElementById('ycal').style.display="none"
}

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

// auto-scroll to day
function onScroll(div) {
	if (window.devicePixelRatio==1) {
		function animScroll(div, to, duration) {
		if (duration<=0) return;
		setTimeout(function() {
				div.scrollTop = div.scrollTop+(to-div.scrollTop)/duration*10;
				animScroll(div,to,duration-10);
			},10);
		}
		if (scrollTO) clearTimeout(scrollTO);
		scrollTO = setTimeout(function(){
			var cellh = 108
			animScroll(div,Math.round(Math.round(div.scrollTop/cellh)*cellh),70);},200);
	}
}

function fillDays(d0, d1) {
	function toDate(did) {return new Date((did-719163)*8.64e7)}
	day0 = toDate(d0);
	day1 = toDate(d1);
	for (var di=d0; di<d1+1;di++) {
		dayi = toDate(di);
		dstr = ('<time id="'+("00"+dayi.getDate()).slice(-2)+' '
					+monthns[dayi.getMonth()]+' '+dayi.getFullYear()
					+'" dayid="'+di+'"><a>'+dayi.getDate()+'</a>'
					+'<script src="./'+di+'/ds.js"></script></time>');
		document.write(dstr);
	}
}

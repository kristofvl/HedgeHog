
// obtain day id and start and stop times:
	function delineate(str,start,c1,c2){
		lft = str.indexOf(c1,start)+1;
		rgt = str.indexOf(c2,lft);
		if (rgt==-1) rgt=str.length
		return {subs:(str.substring(lft,rgt)),ind:rgt}
	}
	var ret=delineate(window.location.href,0,"=","&");
	var strtt = parseInt(ret.subs);
	ret=delineate(window.location.href,ret.ind,"=","&");
	var stopt = parseInt(ret.subs);
	var dayid = parseInt(delineate(window.location.href,ret.ind,"=","&").subs);

	if (isNaN(dayid)) {
		var idx = window.location.href.indexOf("/index")-8
		var ret=delineate(window.location.href,idx,"/","/");
		dayid = parseInt(ret.subs)
		strtt=0; stopt=86400
	}

// check ans and truncate ans to today's entries:
if (typeof ans === 'undefined') {
	var ans = []
}
else {
	var tmp_ans = [];
	for(var i=0;i<ans.length;i++)
		if (ans[i][3]==dayid)
			tmp_ans.push(ans[i]);
	ans = tmp_ans;
}

// calculate data boundaries and skips:
var sspan=(stopt-strtt), soff=strtt;
var skipxyz=2,skipenv=32;
for(var i=3;i<24;i+=2){if((sspan/3600)>i){skipxyz+=4;skipenv+=64;}}

// load icon images:
var imgsa = [
	["unknown",'../img/unknown.png'],
	["look","../img/zoom.png"],
	["sleep", "../img/sleep.png"],
	["bike","../img/riding_bike.png"],
	["car","../img/driving_car.png"],
	["walk","../img/walk.gif"],
	["smoke","../img/smoking.gif"],
	["inj","../img/injecting.gif"],
	["meas","../img/meas.png"],
	];
var imga = new Array()
function loadIcons(arr) {
	var loadedimgs=0
	var postaction=function(){}
	function imageloadpost(){
		loadedimgs++
		if (loadedimgs==arr.length){postaction(imga)}
	}
	for (var i=0;i<arr.length;i++){
		imga[i] = new Image()
		imga[i].src = imgsa[i][1]
		imga[i].onload=function(){imageloadpost()}
		imga[i].onerror=function(){imageloadpost()}
	}
	return { done:function(f){postaction=f || postaction}}
}


function toTime(tfrac){
	hrs = Math.floor(tfrac/(60*60))%24;
	mns = Math.floor( (tfrac%(60*60))/60 );
	return ("00"+hrs).slice(-2)+":"+("00"+mns).slice(-2);
}

function ftoTime(tfrac){
	hrs = Math.floor(tfrac*24)%24;
	mns = Math.round(Math.abs(60*((tfrac*24)-Math.floor(tfrac*24))))%60;
	return ("00"+hrs).slice(-2)+":"+("00"+mns).slice(-2);
}

function toDate(did){
	var d = new Date((did-719163)*8.64e7)
	return ("0000"+d.getUTCFullYear()).slice(-4)+"-"+
			("00"+(d.getUTCMonth()+1)).slice(-2)+"-"+
			("00"+d.getUTCDate()).slice(-2);
}

function goRight(){
	if (sspan==86400){
		dayid++;
		window.open('../'+dayid+
		'/index.html?strtt=0&stopt=86400&dayid='+dayid,'_self',false)
	}else{
		strtt+=sspan/2;stopt+=sspan/2
		if (stopt>86400) { dayid++; strtt=0; stopt=sspan;}
		window.open('../'+dayid+'/index_zoom.html?strtt='+
			strtt+"&stopt="+stopt+"&dayid="+dayid,'_self',false)
	}
}

function goLeft(){
	if (sspan==86400){
		dayid--;
		window.open('../'+dayid+
		'/index.html?strtt=0&stopt=86400&dayid='+dayid,'_self',false)
	}else{
		strtt-=sspan/2;stopt-=sspan/2
		if (strtt<0) { dayid--; strtt=86400-sspan; stopt=86400;}
		window.open('../'+dayid+'/index_zoom.html?strtt='+
			strtt+"&stopt="+stopt+"&dayid="+dayid,'_self',false)
	}
}

function goUp(){
	window.open(((sspan==86400)?'.':'')+'./index.html','_self',false)
}

function subSample(skipVal,strVals,sta,sto){
	var ret='';
	if (sta%2!=0) sta-=1;
	for (var i=sta;i<sto;i+=skipVal)
		ret+=strVals.charAt(i)+strVals.charAt(i+1);
	return ret;
}

function fillLabels(numTicks,labelLen,sspan,soff){
	var ll= new Array(labelLen+1).join('0').split('');
	for (var i=0;i<numTicks;i++) {
		idx = Math.floor(i*labelLen/(numTicks-1));
		ll[idx]=ftoTime((soff+i*sspan/(numTicks-1))/86400);
	}
	return ll;
}
				
function drawAll(x,y,z,l,p, strtt,stopt, skipenv, skipxyz, ticks){
	var sta=Math.round(x.length*(strtt/86400)); 
	var sto=Math.round(x.length*(stopt/86400));
	var pstart = Math.round(p.length*(strtt/86400));
	var pstop  = Math.round(p.length*(stopt/86400));
	var anim=false;if ((strtt==0)&&(stopt==86400)) anim=true;
	ps = subSample(2,p,pstart,pstop);
	ls = subSample(skipenv,l,sta,sto);
	xs = subSample(skipxyz,x,sta,sto);
	ys = subSample(skipxyz,y,sta,sto);
	zs = subSample(skipxyz,z,sta,sto);
	ll = fillLabels(ticks,xs.length/2,sspan,soff);
	var d_light={l:[],ds:[{fc:"#dd0",sc:"#ddd",d:ls}]};
	var d_acc3d={l:ll,ds:[{sc:"#d00",d:xs},{sc:"#0c0",d:ys},{sc:"#00d",d:zs}]};
	var d_night={l:[],ds:[{fc:"#111",sc:"#ddd",d:ps}]};
	var bopts = {scaleShowLabels:true,scaleFontSize:12,scaleShowGridLines:true,animation:anim,scaleStepWidth:32,sspan:sspan,soff:soff}
	var lopts = {scaleSteps:8,scaleShowLabels:true,scaleFontSize:12,scaleLineWidth:1,datasetStrokeWidth:0.5,scaleStepWidth:32,sspan:sspan,soff:soff}
	var light = new Chart(document.getElementById("day_view_light").getContext("2d")).Bar(d_light,bopts);
	var acc3d = new Chart(document.getElementById("day_view_acc3d").getContext("2d")).Line(d_acc3d,lopts);
	var night = new Chart(document.getElementById("night_view_prb").getContext("2d")).Bar(d_night,bopts);
	var ansca = new Ans(document.getElementById("dvans").getContext("2d"))
}

function reDrawAll(nhoff,nhspan){
	sspan = nhspan; soff = nhoff
	skipxyz=2,skipenv=32;
	for(var i=3;i<24;i+=2){if(hspan>i){skipxyz+=4;skipenv+=64;}}
	drawAll(x,y,z,l,p,(soff/86400),(soff+sspan)/86400, skipenv, skipxyz, 7)
}

function Ans(ac){
	var drag,dragL,dragR = false,
    mouseX, mouseY,
    closeEnough = 10,
    cur_rect = -1,
    ldist, rdist = 0;
	var co = 32 ;
	var cw = ac.canvas.width-co;
	
	loadIcons(imgsa).done(function(imga){});
	
	function init_ans() {
		if (window.devicePixelRatio) {
			ac.canvas.style.width = ac.canvas.width +"px";
			ac.canvas.style.height = ac.canvas.height +"px";
			ac.canvas.height= ac.canvas.height*window.devicePixelRatio;
			ac.canvas.width = ac.canvas.width *window.devicePixelRatio;
			ac.scale(window.devicePixelRatio, window.devicePixelRatio);
		}
		if (typeof(ans)=="undefined"){
			var ans_str = localStorage.getItem('hhg_ans');
			if (ans_str!=null) {
				ans = JSON.parse(ans_str);	
			}
		}
		ac.canvas.addEventListener('mousedown', mouseDown, false);
		ac.canvas.addEventListener('mouseup', mouseUp, false);
		ac.canvas.addEventListener('mousemove', mouseMove, false);
		ac.canvas.addEventListener('dblclick', mouseDbl, false);
		loadIcons(imgsa).done(function(imga){draw_ans()})
	}

	function toCanCoord(x){
		return co-2+(86400/sspan)*(x-(soff/86400))*cw;
	}
	function fromCanCoord(y){
		return ((y-co+2)/(cw*(86400/sspan)))+(soff/86400) 
	}

	function mouseDown(e) {
		if (e.offsetX) {
			mouseX = e.offsetX; mouseY = e.offsetY;
		}
		else if (e.layerX){
			mouseX = e.layerX; mouseY = e.layerY;
		}
		for(var i=0;i<ans.length;i++){
			if( checkCloseEnough(mouseX, toCanCoord(ans[i][1])) && 
				 checkCloseEnough(mouseY,7) ){
				dragL = true; cur_rect = i; break;
			}
			else if( checkCloseEnough(mouseX, toCanCoord(ans[i][2])) && 
					checkCloseEnough(mouseY,7) ){
				dragR = true; cur_rect = i; break;
			}
			else if((mouseX<toCanCoord(ans[i][2]))&&
					  (mouseX>toCanCoord(ans[i][1]))){
				if (mouseY>55) {
					if (ans[i][4]!=undefined)
						window.open(ans[i][4]);
				} else {
					drag = true; cur_rect = i; 
					ldist = mouseX-toCanCoord(ans[i][1]);
					rdist = toCanCoord(ans[i][2])-mouseX;
				}
				break;
			}
		}
	}
	function checkCloseEnough(p1, p2){
		return Math.abs(p1-p2)<closeEnough;
	}
	function mouseUp() {
		if (cur_rect!=-1){
			localStorage.setItem('hhg_ans', JSON.stringify(ans));
			console.log('[\"%s\",%f,%f,%i],', ans[cur_rect][0],
				parseFloat(ans[cur_rect][1].toFixed(5)),
				parseFloat(ans[cur_rect][2].toFixed(5)),ans[cur_rect][3]);
		}
		drag=dragL=dragR=false; ldist=rdist=0; cur_rect = -1;	
	}
	function mouseMove(e) {
		ac.canvas.style.cursor = 'pointer';
		if (e.offsetX) {
			mouseX = e.offsetX; mouseY = e.offsetY;
		}
		else if (e.layerX){
			mouseX = e.layerX; mouseY = e.layerY;
		}
		if((mouseX-ldist>=co-2)&&(mouseX+rdist<cw+co+2)){
			if(dragL){
				ac.canvas.style.cursor = 'col-resize';
				ans[cur_rect][1] = fromCanCoord(mouseX);
			} else if(dragR) {
				ac.canvas.style.cursor = 'col-resize';
				ans[cur_rect][2] = fromCanCoord(mouseX);
			} else if(drag) {
				ac.canvas.style.cursor = 'col-resize';
				ans[cur_rect][1] = fromCanCoord(mouseX-ldist);
				ans[cur_rect][2] = fromCanCoord(mouseX+rdist);
			} else { ac.canvas.style.cursor = 'default';}
		}
		if (dragL || dragR || drag) { draw_ans(); }
	}
	function mouseDbl(e) {
		if (e.offsetX) { mouseX = e.offsetX; mouseY = e.offsetY; }
		else if (e.layerX){ mouseX = e.layerX; mouseY = e.layerY; }
		var hndld = false
		for(var i=0;i<ans.length;i++){
			if((mouseX<toCanCoord(ans[i][2]))&&
				(mouseX>toCanCoord(ans[i][1]))){
				if (mouseY>55) {
					if (ans[i][4]!=undefined) 
						window.open(ans[i][4]);
					hndld=true;
				}
				else {
					ans.splice(i,1);
					hndld=true;
				}
				break;
			}
		}
		if (!hndld) {
			ans.push(["new",fromCanCoord(mouseX-17),
					fromCanCoord(mouseX+17),dayid]);
		}
		draw_ans();
	}

	function draw_ans() {
		function loadIcon(ret,x,y) {ac.drawImage(imga[ret],x,y,17,17);}
		ac.beginPath();
		ac.fillStyle = "white";
		ac.fillRect(0,0,ac.canvas.width,ac.canvas.height);
		ac.font="8pt Arial"; ac.fillStyle = "black";
		if (typeof(ans)!="undefined"){
			for(var i=0;i<ans.length;i++){
			if ((ans[i][2]>(soff/86400))&&(ans[i][1]<((soff+sspan)/86400))){
				ac.rect(toCanCoord(ans[i][1]),-2,
						  (86400/sspan)*(ans[i][2]-ans[i][1])*cw,17);
				tw = ac.measureText(ans[i][0]).width/2;
				ret = 0;
				for (var k=0;k<imgsa.length;k++){
					if (ans[i][0]==imgsa[k][0]) {ret=k;break;}
				}
				loadIcon(ret,toCanCoord((ans[i][1]+ans[i][2])/2)-8,22);
				ac.fillText(ans[i][0],toCanCoord((ans[i][1]+ans[i][2])/2)-tw,53);
				if (ans[i][4]!=undefined)
					loadIcon(1,toCanCoord((ans[i][1]+ans[i][2])/2)-8,60);
				ac.stroke();
			}}
		}
	}
	init_ans();
}

window.addEventListener("keydown", handleKey, false);
 
function handleKey(e){
	function timeStr(from,to){
		return "_"+toTime(from).replace(':','')+toTime(to).replace(':','')
	}
	var hstr = '', update=false
	if (e.keyCode==37) goLeft()
	else if (e.keyCode==38) { // up
				update=true
	}
	else if (e.keyCode==39) goRight()
	if (update)
		window.open('../'+dayid+'/index.html','_self',false);
}

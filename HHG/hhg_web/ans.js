// truncate ans to today's entries:
var tmp_ans = [];
for(var i=0;i<ans.length;i++)
	if (ans[i][3]==dayid)
		tmp_ans.push(ans[i]);
ans = tmp_ans;

// load icon images:
var imgsa = [
	["unknown",'../img/unknown.png'],
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
			
// calculate data boundaries and skips:
var hspan=Math.round(24*(stopt-strtt)), hoff=strtt*24;
var skipxyz=2,skipenv=32;
for(var i=3;i<24;i+=2){if(hspan>i){skipxyz+=4;skipenv+=64;}}

function toTime(tfrac){
	hrs = Math.floor(tfrac*24)%24;
	mns = Math.round(Math.abs(60*((tfrac*24)-Math.floor(tfrac*24))))%60;
	return ("00"+hrs).slice(-2)+":"+("00"+mns).slice(-2);
};

function subSample(skipVal,strVals,sta,sto){
	var ret='';
	if (sta%2!=0) sta-=1;
	if (sto%2!=0) sto-=1;
	for (var i=sta;i<sto;i+=skipVal)
		ret+=strVals.charAt(i)+strVals.charAt(i+1);
	return ret;
};

function fillLabels(numTicks,labelLen,hspan,hoff){
	var ll= new Array(labelLen+1).join('0').split('');
	for (var i=0;i<numTicks;i++) {
		idx = Math.floor(i*labelLen/(numTicks-1));
		ll[idx]=toTime((hoff+i*hspan/(numTicks-1))/24);
	}
	return ll;
};
				
function drawAll(x,y,z,l,p, strtt,stopt, skipenv, skipxyz, ticks){
	var sta=x.length*strtt; var sto=x.length*stopt;
	var anim=false;if ((strtt==0)&&(stopt==1)) anim=true;
	var pstart = Math.round(p.length*strtt);
	var pstop  = Math.round(p.length*stopt);
	ps = subSample(2,p,pstart,pstop);
	ls = subSample(skipenv,l,sta,sto);
	xs = subSample(skipxyz,x,sta,sto);
	ys = subSample(skipxyz,y,sta,sto);
	zs = subSample(skipxyz,z,sta,sto);
	ll = fillLabels(ticks,xs.length/2,hspan,hoff);
	var d_light={l:[],ds:[{fc:"#dd0",sc:"#ddd",d:ls}]};
	var d_acc3d={l:ll,ds:[{sc:"#d00",d:xs},{sc:"#0c0",d:ys},{sc:"#00d",d:zs}]};
	var d_night={l:[],ds:[{fc:"#111",sc:"#ddd",d:ps}]};
	var light = new Chart(document.getElementById("day_view_light").getContext("2d")).Bar(d_light,{scaleShowLabels:true,scaleFontSize:12,scaleShowGridLines:true,animation:anim,scaleStepWidth:32,hspan:hspan,hoff:hoff});
	var acc3d = new Chart(document.getElementById("day_view_acc3d").getContext("2d")).Line(d_acc3d,{scaleSteps:8,scaleShowLabels:true,scaleFontSize:12,scaleLineWidth:1,datasetStrokeWidth:0.5,scaleStepWidth:32,hspan:hspan,hoff:hoff});
	var night = new Chart(document.getElementById("night_view_prb").getContext("2d")).Bar(d_night,{scaleShowLabels:true,scaleFontSize:12,scaleShowGridLines:true,animation:anim,scaleStepWidth:32,hspan:hspan,hoff:hoff});
	var ansca = new Ans(document.getElementById("dvans").getContext("2d"))
}



function Ans(ac) {
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
			ac.canvas.style.width = ac.canvas.width + "px";
			ac.canvas.style.height = ac.canvas.height + "px";
			ac.canvas.height = ac.canvas.height * window.devicePixelRatio;
			ac.canvas.width = ac.canvas.width * window.devicePixelRatio;
			ac.scale(window.devicePixelRatio, window.devicePixelRatio);
		}
		if (typeof(ans)=="undefined"){
			var ans_str = localStorage.getItem('hhg_ans');
			if (ans_str!=null) {
				ans = JSON.parse(ans_str);
				console.log("loaded: %s", ans_str);		
			}
		}
		console.log("dayid: %d", dayid);
		ac.canvas.addEventListener('mousedown', mouseDown, false);
		ac.canvas.addEventListener('mouseup', mouseUp, false);
		ac.canvas.addEventListener('mousemove', mouseMove, false);
		ac.canvas.addEventListener('dblclick', mouseDbl, false);
		loadIcons(imgsa).done(function(imga){
		draw_ans()})
	}

	function toCanCoord(x){
		return co-2+(24/hspan)*(x-(hoff/24))*cw;
	}
	function fromCanCoord(y){
		return ((y-co+2)/(cw*(24/hspan)))+(hoff/24);
	}

	function mouseDown(e) {
		if (e.offsetX) {
			mouseX = e.offsetX; mouseY = e.offsetY;
		}
		else if (e.layerX){
			mouseX = e.layerX; mouseY = e.layerY;
		}
		for(var i=0;i<ans.length;i++){
		if (ans[i][3]==dayid){
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
				drag = true; cur_rect = i; 
				ldist = mouseX-toCanCoord(ans[i][1]);
				rdist = toCanCoord(ans[i][2])-mouseX;
				break;
			}
		}}
	}
	function checkCloseEnough(p1, p2){
		return Math.abs(p1-p2)<closeEnough;
	}
	function mouseUp() {
		if (cur_rect!=-1){
			localStorage.setItem('hhg_ans', JSON.stringify(ans));
			console.log("new: %s", ans[cur_rect]);	
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
		var deleted = false
		for(var i=0;i<ans.length;i++){
		if (ans[i][3]==dayid){
			if((mouseX<toCanCoord(ans[i][2]))&&
				(mouseX>toCanCoord(ans[i][1])) ){
				ans.splice(i,1);
				deleted = true;
				break;
			}
		}}
		if (!deleted) {
			ans.push(["new",fromCanCoord(mouseX-17),fromCanCoord(mouseX+17),dayid]);
		}
		draw_ans();
	}

	function draw_ans() {
		ac.beginPath();
		ac.fillStyle = "white";
		ac.fillRect(0,0,ac.canvas.width,ac.canvas.height);
		ac.font="8pt Arial"; ac.fillStyle = "black";
		if (typeof(ans)!="undefined"){
			for(var i=0;i<ans.length;i++){
			if ((ans[i][3]==dayid)&&
				 (ans[i][2]>(hoff/24))&&(ans[i][1]<((hoff+hspan)/24))){
				ac.rect(toCanCoord(ans[i][1]),-2,
						  (24/hspan)*(ans[i][2]-ans[i][1])*cw,17);
				tw = ac.measureText(ans[i][0]).width/2;
				function loadIcon(ret,x,y) {
					ac.drawImage(imga[ret],x,y,17,17);
				}
				ret = 0;
				for (var k=0;k<imgsa.length;k++){
					if (ans[i][0]==imgsa[k][0]) {ret=k;break;}
				}
				loadIcon(ret,toCanCoord((ans[i][1]+ans[i][2])/2)-8,22);
				ac.fillText(ans[i][0],toCanCoord((ans[i][1]+ans[i][2])/2)-tw,53);
				ac.stroke();
			}}
		}
	}
	
	init_ans();
	
}

window.addEventListener("keydown", handleKey, false);
 
function handleKey(e){
	var newdayid = dayid;
	var hstr = '';
	if (e.keyCode==37) { // left
		if (hspan==24) newdayid--;
		else if (hspan==6) {
				if (hoff<3) {	newdayid--; hoff=21; }
				hstr = "_"+("00"+(hoff-3)).slice(-2)+"00"+("00"+(hoff+3)%24).slice(-2)+"00";
		}
		else if (hspan==1) {
				if (hoff<1) {	newdayid--; hoff=23; }
				hstr = "_"+("00"+(hoff-.5)).slice(-2)+"00"+("00"+(hoff+.5)%24).slice(-2)+"00";
		}
	}
	else if (e.keyCode==38) { // up
		
	}
	else if (e.keyCode==39) { // right
		if (hspan==24) newdayid++;
		else if (hspan==6) {
				if (hoff>17) {	newdayid++; hoff=-3; }
				hstr = "_"+("00"+(hoff+3)).slice(-2)+"00"+("00"+(hoff+9)%24).slice(-2)+"00";
		}
		else if (hspan==1) {
				if (hoff>22.5) {	newdayid--; hoff=-.5; }
				hstr = "_"+("00"+(hoff+.5)).slice(-2)+"00"+("00"+(hoff+1.5)%24).slice(-2)+"00";
		}
	}
	window.open('../'+newdayid+'/index'+hstr+'.html','_self',false);
}

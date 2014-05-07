
var imgsa = [
["unknown",'../img/unknown.png'],
["sleep", "../img/sleep.png"],
["bike","../img/riding_bike.png"],
["car","../img/driving_car.png"],
["walk","../img/walk.gif"],
["smoke","../img/smoking.gif"],
["inj","../img/injecting.gif"]
];

var imga = new Array();
for (var i=0;i<imga.length;i++){
	imga[i] = new Image();
	imga[i].src = imgsa[i][1];
}

var anscanvas = document.getElementById("dvans");
var ac=anscanvas.getContext("2d");

var co = 32 ;
var cw = ac.canvas.width-co;

if (window.devicePixelRatio) {
	ac.canvas.style.width = anscanvas.width + "px";
	ac.canvas.style.height = anscanvas.height + "px";
	ac.canvas.height = anscanvas.height * window.devicePixelRatio;
	ac.canvas.width = anscanvas.width * window.devicePixelRatio;
	ac.scale(window.devicePixelRatio, window.devicePixelRatio);
}

var drag,dragL,dragR = false,
    mouseX, mouseY,
    closeEnough = 10,
    cur_rect = -1,
    ldist, rdist = 0;

function init_ans() {
	if (typeof(ans)=="undefined"){
		var ans_str = localStorage.getItem('hhg_ans');
		if (ans_str!=null) {
			ans = JSON.parse(ans_str);
			console.log("loaded: %s", ans_str);		
		} 
	}
	console.log("dayid: %d", dayid);
	anscanvas.addEventListener('mousedown', mouseDown, false);
	anscanvas.addEventListener('mouseup', mouseUp, false);
	anscanvas.addEventListener('mousemove', mouseMove, false);
	anscanvas.addEventListener('dblclick', mouseDbl, false);
	draw_ans();
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
	anscanvas.style.cursor = 'pointer';		
	if (e.offsetX) {
		mouseX = e.offsetX; mouseY = e.offsetY;
	}
	else if (e.layerX){
		mouseX = e.layerX; mouseY = e.layerY;
	}
	if((mouseX-ldist>=co-2)&&(mouseX+rdist<cw+co+2)){
		if(dragL){
			anscanvas.style.cursor = 'col-resize';
			ans[cur_rect][1] = fromCanCoord(mouseX);
		} else if(dragR) {
			anscanvas.style.cursor = 'col-resize';
			ans[cur_rect][2] = fromCanCoord(mouseX);
		} else if(drag) {
			anscanvas.style.cursor = 'col-resize';
			ans[cur_rect][1] = fromCanCoord(mouseX-ldist);
			ans[cur_rect][2] = fromCanCoord(mouseX+rdist);
		} else { anscanvas.style.cursor = 'default';}
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
		ans.push(["new", fromCanCoord(mouseX-17),fromCanCoord(mouseX+17),dayid]);
	}
	draw_ans();
}

function draw_ans() {
	ac.beginPath();
	ac.fillStyle = "white";
	ac.fillRect(0,0,cw+co+2,100);
	ac.font="8pt Arial"; ac.fillStyle = "black";
	if (typeof(ans)!="undefined"){
		for(var i=0;i<ans.length;i++){
		if ((ans[i][3]==dayid)&&
			 (ans[i][2]>(hoff/24))&&(ans[i][1]<((hoff+hspan)/24))){
			ac.rect(toCanCoord(ans[i][1]),-2,
					  (24/hspan)*(ans[i][2]-ans[i][1])*cw,17);
			tw = ac.measureText(ans[i][0]).width/2;
			function loadIcon(src,x,y) {
				var img = new Image();img.src= src;
				img.onload = function(){ac.drawImage(img,x,y,17,17);}
			}
			ret = 0;
			for (var k=0;k<imgsa.length;k++){
				if (ans[i][0]==imgsa[k][0]) {ret=k;break;}
			}
			loadIcon(imgsa[ret][1],toCanCoord((ans[i][1]+ans[i][2])/2)-8,22);
			ac.fillText(ans[i][0],toCanCoord((ans[i][1]+ans[i][2])/2)-tw,53);
			ac.stroke();
		}}
	}
}

init_ans();

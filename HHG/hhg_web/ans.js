


var anscanvas = document.getElementById("dvans")
var ac=anscanvas.getContext("2d");

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
	draw_ans();
}

function mouseDown(e) {
	if (e.offsetX) {
		mouseX = e.offsetX; mouseY = e.offsetY;
	}
	else if (e.layerX){
		mouseX = e.layerX; mouseY = e.layerY;
	}
	// check where was was clicked:
	for(var i=0;i<ans.length;i++){
	if (ans[i][3]==dayid){
		if( checkCloseEnough(mouseX, 30+ans[i][1]*800) && 
			 checkCloseEnough(mouseY,7) ){
			dragL = true; cur_rect = i; break;
		}
		else if( checkCloseEnough(mouseX, 30+(ans[i][2])*800) && 
				checkCloseEnough(mouseY,7) ){
			dragR = true; cur_rect = i; break;
		}
		else if((mouseX<30+(ans[i][2])*800)&&(mouseX>30+(ans[i][1])*800)){
			drag = true; cur_rect = i; 
			ldist = mouseX-(30+ans[i][1]*800);
			rdist = (30+ans[i][2]*800)-mouseX;
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
	if (e.offsetX) {
		mouseX = e.offsetX; mouseY = e.offsetY;
	}
	else if (e.layerX){
		mouseX = e.layerX; mouseY = e.layerY;
	}
	if((mouseX-ldist>29)&&(mouseX+rdist<832)){		
		if(dragL){
			ans[cur_rect][1] = (mouseX-30)/800;
		} else if(dragR) {
			ans[cur_rect][2] = (mouseX-30)/800;
		} else if(drag) {
			ans[cur_rect][1] = ((mouseX-ldist)-30)/800;
			ans[cur_rect][2] = ((mouseX+rdist)-30)/800;
		}
	}
	if (dragL || dragR || drag) {
		draw_ans();
	}
}

function draw_ans() {
	ac.beginPath();
	ac.fillStyle = "white";
	ac.fillRect(0,0,832,100);
	ac.font="12px Helvetica"; ac.fillStyle = "black";
	if (typeof(ans)!="undefined"){
		for(var i=0;i<ans.length;i++){
		if (ans[i][3]==dayid){	
			ac.rect(30+ans[i][1]*800,-2,(ans[i][2]-ans[i][1])*800,17);
			tw = ac.measureText(ans[i][0]).width/2;
			ac.fillText(ans[i][0],30+(ans[i][1]+ans[i][2])*400-tw,27);
			ac.stroke();
		}}
	}
}

init_ans()

/*!
 * Chart.js
 * http://chartjs.org/
 *
 * Copyright 2013 Nick Downie
 * Released under the MIT license
 * https://github.com/nnnick/Chart.js/blob/master/LICENSE.md
 * 
 * heavily modified by KristofVL for the HedgeHog project
 */

//Define the global Chart Variable as a class.
window.Chart = function(context){

	var chart = this;
	
	//Easing functions adapted from Robert Penner's easing equations
	//http://www.robertpenner.com/easing/
	var animationOptions = {
		linear : function (t){
			return t;
		},
		easeInQuad: function (t) {
			return t*t;
		},
		easeOutQuad: function (t) {
			return -1 *t*(t-2);
		}
	};

	//Variables global to the chart
	var width = context.canvas.width;
	var height = context.canvas.height;

	//High pixel density displays - multiply the size of the canvas height/width by the device pixel ratio, then scale.
	if (window.devicePixelRatio) {
		context.canvas.style.width = width + "px";
		context.canvas.style.height = height + "px";
		context.canvas.height = height * window.devicePixelRatio;
		context.canvas.width = width * window.devicePixelRatio;
		context.scale(window.devicePixelRatio, window.devicePixelRatio);
	}

	this.Line = function(data,options){
	
		chart.Line.defaults = {
			scaleOverlay : false,
			scaleOverride : true,
			scaleSteps : 4,
			scaleStepWidth : 64,
			scaleStartValue : 0,
			scaleLineColor : "rgba(0,0,0,.1)",
			scaleLineWidth : 0,
			scaleShowLabels : false,
			scaleLabel : "<%=value%>",
			scaleFontFamily : "'Arial'",
			scaleFontSize : 0,
			scaleFontStyle : "normal",
			scaleFontColor : "#666",
			scaleShowGridLines : true,
			scaleGridLineColor : "rgba(0,0,0,.05)",
			scaleGridLineWidth : 1,
			bezierCurve : false,
			pointDot : false,
			pointDotRadius : 4,
			pointDotStrokeWidth : 2,
			datasetStroke : true,
			datasetStrokeWidth : 0.5,
			datasetFill : false,
			animation : false,
			animationSteps : 2,
			animationEasing : "linear",
			onAnimationComplete : null
		};		
		var config = (options) ? mergeChartConfig(chart.Line.defaults,options) : chart.Line.defaults;
		
		return new Line(data,config,context);
	}
	
	this.Bar = function(data,options){
		chart.Bar.defaults = {
			scaleOverlay : false,
			scaleOverride : true,
			scaleSteps : 4,
			scaleStepWidth : 32,
			scaleStartValue : 0,
			scaleLineColor : "rgba(0,0,0,.1)",
			scaleLineWidth : 1,
			scaleShowLabels : false,
			scaleLabel : "<%=value%>",
			scaleFontFamily : "'Arial'",
			scaleFontSize : 0,
			scaleFontStyle : "normal",
			scaleFontColor : "#666",
			scaleShowGridLines : false,
			scaleGridLineColor : "rgba(0,0,0,.05)",
			scaleGridLineWidth : 1,
			barShowStroke : false,
			barStrokeWidth : 0,
			barValueSpacing : 0,
			barDatasetSpacing : 0,
			animation : false,
			animationSteps : 17,
			animationEasing : "linear",
			onAnimationComplete : null
		};		
		var config = (options) ? mergeChartConfig(chart.Bar.defaults,options) : chart.Bar.defaults;
		
		return new Bar(data,config,context);		
	}
	
	var clear = function(c){
		c.clearRect(0, 0, width, height);
	};

	var Line = function(data,config,ctx){
		var maxSize, scaleHop, calculatedScale, labelHeight, scaleHeight, valueBounds, labelTemplateString, valueHop,widestXLabel, xAxisLength,yAxisPosX,xAxisPosY;
			
		for (var i=0; i<data.ds.length; i++){
			var d = [];
			while (data.ds[i].d.length) {
				d.push(parseInt(data.ds[i].d.substr(0,2),16));
				data.ds[i].d = data.ds[i].d.substr(2);
			}
			data.ds[i].d = d;
		}
		
		calculateDrawingSizes();
		
		valueBounds = getValueBounds();
		//Check and set the scale
		labelTemplateString = (config.scaleShowLabels)? config.scaleLabel : "";
		if (!config.scaleOverride){
			calculatedScale = calculateScale(scaleHeight,valueBounds.maxSteps,valueBounds.minSteps,valueBounds.maxValue,valueBounds.minValue,labelTemplateString);
		}
		else {
			calculatedScale = {
				steps : config.scaleSteps,
				stepValue : config.scaleStepWidth,
				graphMin : config.scaleStartValue,
				labels : []
			}
			populateLabels(labelTemplateString, calculatedScale.labels,calculatedScale.steps,config.scaleStartValue,config.scaleStepWidth);
		}
		
		scaleHop = Math.floor(scaleHeight/calculatedScale.steps);
		calculateXAxisSize();
		animationLoop(config,drawScale,drawLines,ctx);		
		
		function drawLines(animPc){
			for (var i=0; i<data.ds.length; i++){
				ctx.strokeStyle = data.ds[i].sc;
				ctx.lineWidth = config.datasetStrokeWidth;
				ctx.beginPath();
				ctx.moveTo(yAxisPosX, xAxisPosY - animPc*(calculateOffset(data.ds[i].d[0],calculatedScale,scaleHop)))

				for (var j=1; j<data.ds[i].d.length; j++){
					ctx.lineTo(xPos(j),yPos(i,j));
				}
				ctx.stroke();
				ctx.closePath();
				if(config.pointDot){
					ctx.fillStyle = data.ds[i].pointColor;
					ctx.strokeStyle = data.ds[i].pointStrokeColor;
					ctx.lineWidth = config.pointDotStrokeWidth;
					for (var k=0; k<data.ds[i].d.length; k++){
						ctx.beginPath();
						ctx.arc(yAxisPosX + (valueHop *k),xAxisPosY - animPc*(calculateOffset(data.ds[i].d[k],calculatedScale,scaleHop)),config.pointDotRadius,0,Math.PI*2,true);
						ctx.fill();
						ctx.stroke();
					}
				}
			}
			
			function yPos(dataSet,iteration){
				return xAxisPosY - animPc*(calculateOffset(data.ds[dataSet].d[iteration],calculatedScale,scaleHop));			
			}
			function xPos(iteration){
				return yAxisPosX + (valueHop * iteration);
			}
		}
		function drawScale(){
			//X axis line
			ctx.lineWidth = config.scaleLineWidth;
			ctx.strokeStyle = config.scaleLineColor;
			ctx.beginPath();
			ctx.moveTo(width-widestXLabel/2+5,xAxisPosY);
			ctx.lineTo(width-(widestXLabel/2)-xAxisLength-5,xAxisPosY);
			ctx.stroke();
			ctx.fillStyle = config.scaleFontColor;
			if (data.l != []) {
				ctx.textAlign = "center";
				
				for (var i=0; i<data.l.length; i++){
					ctx.save();
					if (data.l[i]!='') {
						ctx.fillText(data.l[i], yAxisPosX + i*valueHop,xAxisPosY + config.scaleFontSize+3);					
					}
					ctx.beginPath();
					ctx.moveTo(yAxisPosX + i * valueHop, xAxisPosY+3);
					//Check i isnt 0, so we dont go over the Y axis twice.
					if(config.scaleShowGridLines && i>0 && (data.l[i]!='')){
						ctx.lineWidth = config.scaleGridLineWidth;
						ctx.strokeStyle = config.scaleGridLineColor;					
						ctx.lineTo(yAxisPosX + i * valueHop, 5);
					}
					else{
						ctx.lineTo(yAxisPosX + i * valueHop, xAxisPosY+3);				
					}
					ctx.stroke();
				}
			}
			
			//Y axis
			ctx.lineWidth = config.scaleLineWidth;
			ctx.strokeStyle = config.scaleLineColor;
			ctx.beginPath();
			ctx.moveTo(yAxisPosX,xAxisPosY+5);
			ctx.lineTo(yAxisPosX,5);
			ctx.stroke();
			ctx.textAlign = "right";
			ctx.textBaseline = "middle";
			for (var j=0; j<calculatedScale.steps; j++){
				ctx.beginPath();
				ctx.moveTo(yAxisPosX-3,xAxisPosY - ((j+1) * scaleHop));
				if (config.scaleShowGridLines){
					ctx.lineWidth = config.scaleGridLineWidth;
					ctx.strokeStyle = config.scaleGridLineColor;
					ctx.lineTo(yAxisPosX + xAxisLength + 5,xAxisPosY - ((j+1) * scaleHop));					
				}
				else{
					ctx.lineTo(yAxisPosX-0.5,xAxisPosY - ((j+1) * scaleHop));
				}
				ctx.stroke();
				if (config.scaleShowLabels){
					ctx.fillText(calculatedScale.labels[j],yAxisPosX-8,xAxisPosY - ((j+1) * scaleHop));
				}
			}
		}
		function calculateXAxisSize(){
			var longestText = 1;
			//if we are showing the labels
			if (config.scaleShowLabels){
				longestText +=30;
			}
			xAxisLength = width - longestText - widestXLabel;
			valueHop = xAxisLength/(data.ds[0].d.length-1);
			yAxisPosX = width-widestXLabel/2-xAxisLength;
			xAxisPosY = scaleHeight + config.scaleFontSize/2;				
		}		
		function calculateDrawingSizes(){
			maxSize = height;
			ctx.font = config.scaleFontStyle + " " + config.scaleFontSize+"px " + config.scaleFontFamily;
			widestXLabel = 1;
			maxSize -= config.scaleFontSize;
			labelHeight = config.scaleFontSize;
			if (config.scaleShowLabels){
				//Add a little padding between the x line and the text
				maxSize -= 9;
				maxSize -= labelHeight;
			}
			scaleHeight = maxSize;
		}
		function getValueBounds() {
			return {
				maxValue : 255,
				minValue : 0,
				maxSteps : Math.floor((scaleHeight / (labelHeight*0.66))),
				minSteps : Math.floor((scaleHeight / labelHeight*0.5))
			};
		}
		

	}
	
	
	var Bar = function(data,config,ctx){
		var maxSize, scaleHop, calculatedScale, labelHeight, scaleHeight, valueBounds, labelTemplateString, valueHop,widestXLabel, xAxisLength,yAxisPosX,xAxisPosY,barWidth;
		
		for (var i=0; i<data.ds.length; i++){
			var d = [];
			while (data.ds[i].d.length) {
				d.push(parseInt(data.ds[i].d.substr(0,2),16));
				data.ds[i].d = data.ds[i].d.substr(2);
			}
			data.ds[i].d = d;
		}
		
		calculateDrawingSizes();
		
		valueBounds = getValueBounds();
		//Check and set the scale
		labelTemplateString = (config.scaleShowLabels)? config.scaleLabel : "";
		if (!config.scaleOverride){
			calculatedScale = calculateScale(scaleHeight,valueBounds.maxSteps,valueBounds.minSteps,valueBounds.maxValue,valueBounds.minValue,labelTemplateString);
		}
		else {
			calculatedScale = {
				steps : config.scaleSteps,
				stepValue : config.scaleStepWidth,
				graphMin : config.scaleStartValue,
				labels : []
			}
			populateLabels(labelTemplateString, calculatedScale.labels,calculatedScale.steps,config.scaleStartValue,config.scaleStepWidth);
		}
		
		scaleHop = Math.floor(scaleHeight/calculatedScale.steps);
		calculateXAxisSize();
		animationLoop(config,drawScale,drawBars,ctx);		
		
		function drawBars(animPc){
			ctx.lineWidth = config.barStrokeWidth;
			for (var i=0; i<data.ds.length; i++){
					ctx.fillStyle = data.ds[i].fc;
					ctx.strokeStyle = data.ds[i].sc;
				for (var j=0; j<data.ds[i].d.length; j++){
					var barOffset = yAxisPosX + config.barValueSpacing + valueHop*j + barWidth*i + config.barDatasetSpacing*i + config.barStrokeWidth*i;
					ctx.beginPath();
					ctx.moveTo(barOffset, xAxisPosY);
					ctx.lineTo(barOffset, xAxisPosY - animPc*calculateOffset(data.ds[i].d[j],calculatedScale,scaleHop)+(config.barStrokeWidth/2));
					ctx.lineTo(barOffset + barWidth, xAxisPosY - animPc*calculateOffset(data.ds[i].d[j],calculatedScale,scaleHop)+(config.barStrokeWidth/2));
					ctx.lineTo(barOffset + barWidth, xAxisPosY);
					if(config.barShowStroke){
						ctx.stroke();
					}
					ctx.closePath();
					ctx.fill();
				}
			}
			
		}
		function drawScale(){
			//X axis line
			ctx.lineWidth = config.scaleLineWidth;
			ctx.strokeStyle = config.scaleLineColor;
			ctx.beginPath();
			ctx.moveTo(width-widestXLabel/2+5,xAxisPosY);
			ctx.lineTo(width-(widestXLabel/2)-xAxisLength-5,xAxisPosY);
			ctx.fillStyle = config.scaleFontColor;
			for (var i=0; i<data.ds[0].d.length; i++){
				ctx.save();
				ctx.beginPath();
				ctx.moveTo(yAxisPosX + (i+1) * valueHop, xAxisPosY+3);
				if(config.scaleShowGridLines)
				{
					ctx.lineWidth = config.scaleGridLineWidth;
					ctx.strokeStyle = config.scaleGridLineColor;					
					ctx.lineTo(yAxisPosX + (i+1) * valueHop, 5);
				}
				ctx.stroke();
			}
			
			//Y axis
			ctx.lineWidth = config.scaleLineWidth;
			ctx.strokeStyle = config.scaleLineColor;
			ctx.beginPath();
			ctx.moveTo(yAxisPosX,xAxisPosY+5);
			ctx.lineTo(yAxisPosX,5);
			ctx.stroke();
			ctx.textAlign = "right";
			ctx.textBaseline = "middle";
			for (var j=0; j<calculatedScale.steps; j++){
				ctx.beginPath();
				ctx.moveTo(yAxisPosX-3,xAxisPosY - ((j+1) * scaleHop));
				if (config.scaleShowGridLines){
					ctx.lineWidth = config.scaleGridLineWidth;
					ctx.strokeStyle = config.scaleGridLineColor;
					ctx.lineTo(yAxisPosX + xAxisLength + 5,xAxisPosY - ((j+1) * scaleHop));					
				}
				else{
					ctx.lineTo(yAxisPosX-0.5,xAxisPosY - ((j+1) * scaleHop));
				}
				
				ctx.stroke();
				if (config.scaleShowLabels){
					ctx.fillText(calculatedScale.labels[j],yAxisPosX-8,xAxisPosY - ((j+1) * scaleHop));
				}
			}
		}
		function calculateXAxisSize(){
			var longestText = 1;
			if (config.scaleShowLabels){
				ctx.font = config.scaleFontStyle + " " + config.scaleFontSize+"px " + config.scaleFontFamily;
				longestText +=30;
			}
			xAxisLength = width - longestText - widestXLabel;
			valueHop = xAxisLength/(data.ds[0].d.length);
			
			barWidth = (valueHop - config.scaleGridLineWidth*2 - (config.barValueSpacing*2) - (config.barDatasetSpacing*data.ds.length-1) - ((config.barStrokeWidth/2)*data.ds.length-1))/data.ds.length;
			
			yAxisPosX = width-widestXLabel/2-xAxisLength;
			xAxisPosY = scaleHeight + config.scaleFontSize/2;		
		}		
		function calculateDrawingSizes(){
			maxSize = height;

			ctx.font = config.scaleFontStyle + " " + config.scaleFontSize+"px " + config.scaleFontFamily;
			widestXLabel = 1;
			maxSize -= config.scaleFontSize;
			
			//Add a little padding between the x line and the text
			labelHeight = config.scaleFontSize;
			
			maxSize -= labelHeight;
			scaleHeight = maxSize;
		}		
		function getValueBounds() {
			return {
				maxValue : 127,
				minValue : 0,
				maxSteps : Math.floor((scaleHeight / (labelHeight*0.66))),
				minSteps : Math.floor((scaleHeight / labelHeight*0.5))
			};	
		}
	}
	
	function writeMsg(msg){
		context.clearRect(787,0,50,17);
		context.font = '10pt Courier';
		context.fillStyle = 'black';
		context.fillText(msg, 830,7);
	}
	function getMousePos(e){
		var rect = context.canvas.getBoundingClientRect();
		return {x: e.clientX-rect.left, y: e.clientY-rect.top};
	}
	context.canvas.addEventListener('mousemove',function(e) {
			var p=getMousePos(e);
			if (p.x>35) { var ofs = (p.x-35);
			writeMsg(''+Math.floor(24*ofs/797)+':'+
				('00'+Math.floor((24*ofs/797-Math.floor(24*ofs/797))*60)).slice(-2))
			};}, false);
	
	function calculateOffset(val,calculatedScale,scaleHop){
		var outerValue = calculatedScale.steps * calculatedScale.stepValue;
		var adjustedValue = val - calculatedScale.graphMin;
		var scalingFactor = CapValue(adjustedValue/outerValue,1,0);
		return (scaleHop*calculatedScale.steps) * scalingFactor;
	}
	
	function animationLoop(config,drawScale,drawData,ctx){
		var animFrameAmount = (config.animation)? 1/CapValue(config.animationSteps,Number.MAX_VALUE,1) : 1,
			easingFunction = animationOptions[config.animationEasing],
			percentAnimComplete =(config.animation)? 0 : 1;
		
	
		
		if (typeof drawScale !== "function") drawScale = function(){};
		
		requestAnimFrame(animLoop);
		
		function animateFrame(){
			var easeAdjustedAnimationPercent =(config.animation)? CapValue(easingFunction(percentAnimComplete),null,0) : 1;
			clear(ctx);
			if(config.scaleOverlay){
				drawData(easeAdjustedAnimationPercent);
				drawScale();
			} else {
				drawScale();
				drawData(easeAdjustedAnimationPercent);
			}				
		}
		function animLoop(){
			//We need to check if the animation is incomplete (less than 1), or complete (1).
				percentAnimComplete += animFrameAmount;
				animateFrame();	
				//Stop the loop continuing forever
				if (percentAnimComplete <= 1){
					requestAnimFrame(animLoop);
				}
				else{
					if (typeof config.onAnimationComplete == "function") config.onAnimationComplete();
				}
			
		}		
		
	}

	//Declare global functions to be called within this namespace here.
	
	
	// shim layer with setTimeout fallback
	var requestAnimFrame = (function(){
		return window.requestAnimationFrame ||
			window.webkitRequestAnimationFrame ||
			window.mozRequestAnimationFrame ||
			window.oRequestAnimationFrame ||
			window.msRequestAnimationFrame ||
			function(callback) {
				window.setTimeout(callback, 1000 / 60);
			};
	})();

	function calculateScale(drawingHeight,maxSteps,minSteps,maxValue,minValue,labelTemplateString){
			var graphMin,graphMax,graphRange,stepValue,numberOfSteps,valueRange,rangeOrderOfMagnitude,decimalNum;
			
			valueRange = maxValue - minValue;
			
			rangeOrderOfMagnitude = calculateOrderOfMagnitude(valueRange);

        	graphMin = Math.floor(minValue / (1 * Math.pow(10, rangeOrderOfMagnitude))) * Math.pow(10, rangeOrderOfMagnitude);
            
            graphMax = Math.ceil(maxValue / (1 * Math.pow(10, rangeOrderOfMagnitude))) * Math.pow(10, rangeOrderOfMagnitude);
            
            graphRange = graphMax - graphMin;
            
            stepValue = Math.pow(10, rangeOrderOfMagnitude);
            
	        numberOfSteps = Math.round(graphRange / stepValue);
	        
	        //Compare number of steps to the max and min for that size graph, and add in half steps if need be.	        
	        while(numberOfSteps < minSteps || numberOfSteps > maxSteps) {
	        	if (numberOfSteps < minSteps){
			        stepValue /= 2;
			        numberOfSteps = Math.round(graphRange/stepValue);
		        }
		        else{
			        stepValue *=2;
			        numberOfSteps = Math.round(graphRange/stepValue);
		        }
	        };

	        var labels = [];
	        populateLabels(labelTemplateString, labels, numberOfSteps, graphMin, stepValue);
		
	        return {
		        steps : numberOfSteps,
				stepValue : stepValue,
				graphMin : graphMin,
				labels : labels		        
		        
	        }
		
			function calculateOrderOfMagnitude(val){
			  return Math.floor(Math.log(val) / Math.LN10);
			}		


	}

    //Populate an array of all the labels by interpolating the string.
    function populateLabels(labelTemplateString, labels, numberOfSteps, graphMin, stepValue) {
        if (labelTemplateString) {
            //Fix floating point errors by setting to fixed the on the same decimal as the stepValue.
            for (var i = 1; i < numberOfSteps + 1; i++) {
                labels.push(tmpl(labelTemplateString, {value: (graphMin + (stepValue * i)).toFixed(getDecimalPlaces(stepValue))}));
            }
        }
    }
	
	//Max value from array
	function Max( array ){
		return Math.max.apply( Math, array );
	};
	//Min value from array
	function Min( array ){
		return Math.min.apply( Math, array );
	};
	//Default if undefined
	function Default(userDeclared,valueIfFalse){
		if(!userDeclared){
			return valueIfFalse;
		} else {
			return userDeclared;
		}
	};
	//Is a number function
	function isNumber(n) {
		return !isNaN(parseFloat(n)) && isFinite(n);
	}
	//Apply cap a value at a high or low number
	function CapValue(valueToCap, maxValue, minValue){
		if(isNumber(maxValue)) {
			if( valueToCap > maxValue ) {
				return maxValue;
			}
		}
		if(isNumber(minValue)){
			if ( valueToCap < minValue ){
				return minValue;
			}
		}
		return valueToCap;
	}
	function getDecimalPlaces (num){
		var numberOfDecimalPlaces;
		if (num%1!=0){
			return num.toString().split(".")[1].length
		}
		else{
			return 0;
		}
		
	} 
	
	function mergeChartConfig(defaults,userDefined){
		var returnObj = {};
	    for (var attrname in defaults) { returnObj[attrname] = defaults[attrname]; }
	    for (var attrname in userDefined) { returnObj[attrname] = userDefined[attrname]; }
	    return returnObj;
	}
	
	//Javascript micro templating by John Resig - source at http://ejohn.org/blog/javascript-micro-templating/
	  var cache = {};
	 
	  function tmpl(str, data){
	    // Figure out if we're getting a template, or if we need to
	    // load the template - and be sure to cache the result.
	    var fn = !/\W/.test(str) ?
	      cache[str] = cache[str] ||
	        tmpl(document.getElementById(str).innerHTML) :
	     
	      // Generate a reusable function that will serve as a template
	      // generator (and which will be cached).
	      new Function("obj",
	        "var p=[],print=function(){p.push.apply(p,arguments);};" +
	       
	        // Introduce the data as local variables using with(){}
	        "with(obj){p.push('" +
	       
	        // Convert the template into pure JavaScript
	        str
	          .replace(/[\r\t\n]/g, " ")
	          .split("<%").join("\t")
	          .replace(/((^|%>)[^\t]*)'/g, "$1\r")
	          .replace(/\t=(.*?)%>/g, "',$1,'")
	          .split("\t").join("');")
	          .split("%>").join("p.push('")
	          .split("\r").join("\\'")
	      + "');}return p.join('');");
	   
	    // Provide some basic currying to the user
	    return data ? fn( data ) : fn;
	  };
}




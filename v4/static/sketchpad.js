// Create variabel for canvas and 2dcanvas context
var canvas,ctx;

// Computer mouse variables for computer mouse
var mouseX,mouseY,mouseDown = 0;

// Touchscreen drawing variables
var touchX, touchY;

let raindow = 0;
let dot_size = 6;
function drawDot(ctx, x, y, size) {
    raindow = raindow + 1
    s=80; l=50; 

    ctx.fillStyle = `hsl(${raindow},${s}%,${l}%)`

    ctx.beginPath();
    ctx.arc(x, y, size, 0, Math.PI*2, true);
    ctx.closePath();
    ctx.fill();
}

function clearCanvas(canvas,ctx) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height)
}

function sketchpad_mouseDown() {
    mouseDown=1;
    drawDot(ctx, mouseX, mouseY, dot_size);
}

function sketchpad_mouseMove(e) {
    getMousePos(e);
    if (mouseDown==1) {
        drawDot(ctx, mouseX, mouseY, dot_size)
    }
}

function sketchpad_mouseUp() {
    mouseDown = 0;
}

function getMousePos(e) {
    if (!e)
        var e = event;
    if (e.offsetX) {
        mouseX = e.offsetX;
        mouseY = e.offsetY;
    }
    else if (e.layerX) {
        mouseX = e.layerX;
        mouseY = e.layerY;
    }}

function sketchpad_touchStart() {
    getTouchPos();
    drawDot(ctx, touchX, touchY, dot_size);
    event.preventDefault();
}

function sketchpad_touchMove(e) { 
    getTouchPos(e);
    drawDot(ctx,touchX,touchY,6); 
    event.preventDefault();
}

function getTouchPos(e) {
    if (!e)
        var e = event;
    if(e.touches) {
        if (e.touches.length == 1) { // Only deal with one finger
            var touch = e.touches[0]; // Get the information for finger #1
            touchX=touch.pageX-touch.target.offsetLeft;
            touchY=touch.pageY-touch.target.offsetTop;
        }
    }
}

// Set-up the canvas and add our event handlers after the page has loaded
function init() {
    
    // Get the specific canvas element from the HTML document
    canvas = document.getElementById('sketchpad');
    // If the browser supports the canvas tag, get the 2d drawing context for this canvas
    if (canvas.getContext)
        ctx = canvas.getContext('2d');
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Check that we have a valid context to draw on/with before adding event handlers
    if (ctx) {
        // React to mouse events on the canvas, and mouseup on the entire document
        canvas.addEventListener('mousedown', sketchpad_mouseDown, false);
        canvas.addEventListener('mousemove', sketchpad_mouseMove, false);
        window.addEventListener('mouseup', sketchpad_mouseUp, false);

        // React to touch events on the canvas
        canvas.addEventListener('touchstart', sketchpad_touchStart, false);
        canvas.addEventListener('touchmove', sketchpad_touchMove, false);
    }
}
//Initializing
var i = 0;
var images = []; //array
var time = 7777; // time in millie seconds

images[0] = "url(../static/uploads/crane.jpg)";
images[1] = "url(../static/uploads/palm.jpg)";
images[2] =  "url(../static/uploads/heron.jpg)";
images[3] = "url(../static/uploads/fog.jpg)";
images[4] =  "url(../static/uploads/water.jpg)";


function changeImage() {
    var el = document.getElementById('splash');
    el.style.backgroundImage = images[i];
    if (i < images.length - 1) {
        i++;
    } else {
        i = 0;
    }
    setTimeout('changeImage()', time);
}

window.onload = changeImage;
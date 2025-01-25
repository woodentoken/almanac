//Initializing
var i = 0;
var images = []; //array
var time = 8000; // time in millie seconds

images[0] =  "url(../static/uploads/20250115_214827_KKB02098.jpg)";
images[1] = "url(../static/uploads/20250115_214906_KKB06201.jpg)";

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
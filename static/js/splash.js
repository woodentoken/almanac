//Initializing
var i = 0;
var images = []; //array
var time = 7777; // time in millie seconds

images[0] = "url(/static/images/crane.jpg)";
images[1] = "url(/static/images/palm.jpg)";
images[2] = "url(/static/images/heron.jpg)";
images[3] = "url(/static/images/fog.jpg)";
images[4] = "url(/static/images/water.jpg)";

// Preload images
function preloadImages() {
    var imageUrls = [
        "/static/images/crane.jpg",
        "/static/images/palm.jpg",
        "/static/images/heron.jpg",
        "/static/images/fog.jpg",
        "/static/images/water.jpg"
    ];
    
    var loadedCount = 0;
    var totalImages = imageUrls.length;
    
    imageUrls.forEach(function(url) {
        var img = new Image();
        img.onload = function() {
            loadedCount++;
            if (loadedCount === totalImages) {
                changeImage(); // Start slideshow after all images are loaded
            }
        };
        img.onerror = function() {
            console.warn('Failed to load image:', url);
            loadedCount++;
            if (loadedCount === totalImages) {
                changeImage(); // Start slideshow even if some images failed
            }
        };
        img.src = url;
    });
}

function changeImage() {
    var el = document.getElementById('splash');
    el.style.backgroundImage = images[i];
    if (i < images.length - 1) {
        i++;
    } else {
        i = 0;
    }
    setTimeout(changeImage, time); // Also fixed the setTimeout syntax
}

window.onload = preloadImages;

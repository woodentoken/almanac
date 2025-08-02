//Initializing
var images = []; //rray
var i = 0; // Index for the current image
var time = 10000;

images[0] = "https://ik.imagekit.io/ry1ze0vkn/splash/crane.jpg?tr=lqip";
images[1] = "https://ik.imagekit.io/ry1ze0vkn/splash/heron.jpg?tr=lqip";
images[2] = "https://ik.imagekit.io/ry1ze0vkn/splash/fog.jpg?tr=lqip";
images[3] = "https://ik.imagekit.io/ry1ze0vkn/splash/palm.jpg?tr=lqip";
images[4] = "https://ik.imagekit.io/ry1ze0vkn/splash/water.jpg?tr=lqip";

document.addEventListener('DOMContentLoaded', function() {
  const el = document.getElementById('splash');
  randomIndex = Math.floor(Math.random() * images.length);
  el.style.backgroundImage = images[randomIndex]; // Initial image
 });


// Preload images
function preloadImages() {
    var imageUrls = [
        "https://ik.imagekit.io/ry1ze0vkn/splash/crane.jpg?tr=lqip",
    ];
    
    var loadedCount = 0;
    var totalImages = imageUrls.length;
    
    imageUrls.forEach(function(url) {
        var img = new Image();
        img.src = url;
    console.log('Preloading image:', url);
        img.onload = function() {
            loadedCount++;
            if (loadedCount === totalImages) {
        console.log('All images preloaded successfully.');
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
  console.log('Changing image to:', images[i]);
    el.style.backgroundImage = images[i];
    if (i < images.length - 1) {
        i++;
    } else {
        i = 0;
    }
    setTimeout(changeImage, time); // Also fixed the setTimeout syntax
}

window.onload = preloadImages;

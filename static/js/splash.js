var images = [];
var i = 0;
var time = 10000;

images[0] = "https://ik.imagekit.io/ry1ze0vkn/splash/crane.jpg?tr=lqip";
images[1] = "https://ik.imagekit.io/ry1ze0vkn/splash/heron.jpg?tr=lqip";
images[2] = "https://ik.imagekit.io/ry1ze0vkn/splash/palm.jpg?tr=lqip";
images[3] = "https://ik.imagekit.io/ry1ze0vkn/splash/water.jpg?tr=rt-180,lqip";

document.addEventListener('DOMContentLoaded', function() {
  const el = document.getElementById('splash');
  const randomIndex = Math.floor(Math.random() * images.length);
  el.style.backgroundImage = `url("${images[randomIndex]}")`;
});

// Preload images
function preloadImages() {
  var loadedCount = 0;
  var totalImages = images.length;

  images.forEach(function(url) {
    var img = new Image();
    img.onload = function() {
      loadedCount++;
      if (loadedCount === totalImages) {
        console.log('All images preloaded successfully.');
        changeImage();
      }
    };
    img.onerror = function() {
      console.warn('Failed to load image:', url);
      loadedCount++;
      if (loadedCount === totalImages) {
        changeImage();
      }
    };
    img.src = url;
  });
}

function changeImage() {
  var el = document.getElementById('splash');
  el.style.backgroundImage = `url("${images[i]}")`;
  console.log('Changing image to:', images[i]);
  i = (i + 1) % images.length;
  setTimeout(changeImage, time);
}

window.onload = preloadImages;


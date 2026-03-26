var images = [];
var i = 0;
var time = 10000;
var activeLayer = 0;
var layers = [];

images[0] = "https://ik.imagekit.io/ry1ze0vkn/splash/crane.jpg?tr=lqip";
images[1] = "https://ik.imagekit.io/ry1ze0vkn/splash/heron.jpg?tr=lqip";
images[2] = "https://ik.imagekit.io/ry1ze0vkn/splash/palm.jpg?tr=lqip";
images[3] = "https://ik.imagekit.io/ry1ze0vkn/splash/water.jpg?tr=rt-180,lqip";

document.addEventListener('DOMContentLoaded', function() {
  const el = document.getElementById('splash');

  // Two stacked layers — crossfade between them since background-image can't be transitioned directly
  for (let n = 0; n < 2; n++) {
    const layer = document.createElement('div');
    layer.className = 'splash-layer';
    layer.style.opacity = '0';
    el.prepend(layer);
    layers.push(layer);
  }

  const randomIndex = Math.floor(Math.random() * images.length);
  i = (randomIndex + 1) % images.length;
  layers[0].style.backgroundImage = `url("${images[randomIndex]}")`;
  layers[0].style.transition = 'none';
  layers[0].style.opacity = '1';
  requestAnimationFrame(() => { layers[0].style.transition = ''; });
});

// Preload images
function preloadImages() {
  var loadedCount = 0;
  var totalImages = images.length;

  images.forEach(function(url) {
    var img = new Image();
    img.onload = function() {
      loadedCount++;
      if (loadedCount === totalImages) setTimeout(changeImage, time);
    };
    img.onerror = function() {
      console.warn('Failed to load image:', url);
      loadedCount++;
      if (loadedCount === totalImages) setTimeout(changeImage, time);
    };
    img.src = url;
  });
}

function changeImage() {
  const next = 1 - activeLayer;
  layers[next].style.backgroundImage = `url("${images[i]}")`;
  layers[next].style.opacity = '1';
  layers[activeLayer].style.opacity = '0';
  activeLayer = next;
  i = (i + 1) % images.length;
  setTimeout(changeImage, time);
}

window.onload = preloadImages;


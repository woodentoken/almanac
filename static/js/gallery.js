document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('imageModal');
  const modalFrame = document.getElementById('modalFrame');
  const modalImg = document.getElementById('fullImage');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const caption = document.getElementById('caption');
  const images = document.querySelectorAll('.grid-item');
  let currentIndex = 0;

  function getFullResUrl(url) {
    return url.replace(/w-\d+,?/g, '');
  }

  function getLowResUrl(url) {
    return url.replace(/w-\d+,?/g, 'bl-6,');
  }

  images.forEach((img, index) => {
    img.onclick = function () {
      openModal(index);
    }
  });

  function openModal(index) {
    currentIndex = index;
    modal.style.display = 'flex';
    modal.classList.add('show');

    console.log('Opening modal for image index:', currentIndex);

    const lowRes = getLowResUrl(images[currentIndex].src);
    modalImg.src = lowRes;

    // Get the full image source by removing 'tr' from the src
    const fullRes = getFullResUrl(images[currentIndex].src);
    const fullImage = new Image();
    fullImage.src = fullRes;
    fullImage.onload = function () {
      console.log('Full image loaded:', fullRes);
      modalImg.src = fullRes;
      modalImg.style.filter = 'none'; // Remove blur after full image loads
    };
    caption.textContent = images[currentIndex].alt;
  }

  prevBtn.onclick = function () {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    modalImg.src = getFullResUrl(images[currentIndex].src)
    caption.textContent = images[currentIndex].alt;

  }

  nextBtn.onclick = function () {
    currentIndex = (currentIndex + 1) % images.length;
    modalImg.src = getFullResUrl(images[currentIndex].src)
    caption.textContent = images[currentIndex].alt;

  }

  // close modal when clicking outside of image
  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = 'none';
      modalImg.src = '';
      modal.classList.remove('show');
    }
    if (event.target == modalImg) {
      modalImg.src = '';
      modal.style.display = 'none';
    }
    if (event.target == modalFrame) {
      modalImg.src = '';
      modal.style.display = 'none';
    }
  }
});

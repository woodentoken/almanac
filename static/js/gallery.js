document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("imageModal");
  const modalFrame = document.getElementById("modalFrame");
  const modalImg = document.getElementById("fullImage");
  const modalSpinner = document.getElementById("modalSpinner");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const caption = document.getElementById("caption");
  const images = document.querySelectorAll(".grid-item");
  const loadedImages = new Set();
  let minIndex = 0;
  let maxIndex = images.length - 1;
  let currentIndex = 0;

  modalImg.addEventListener("contextmenu", function (e) {
    e.preventDefault();
    return false;
  });

  function getFullResUrl(url) {
    return url.replace(/w-\d+,?/g, "");
  }

  function getLowResUrl(url) {
    return url.replace(/w-\d+,?/g, "bl-10,");
  }

  function prefetchImage(index) {
    if (images[index] === undefined) return;

    const fullRes = getFullResUrl(images[index].src);
    if (!loadedImages.has(fullRes)) {
      const img = new Image();
      img.src = fullRes;
      img.onload = () => loadedImages.add(fullRes);
    }
  }

  function openModal(index) {
    modal.style.display = "flex";

    // reveal the image
    modal.classList.add("show");

    loadImage(index);
  }

  function closeModal() {
    modal.style.display = "none";
    modalImg.src = "";
    modal.classList.remove("show");
  }

  function loadImage(index, showCaption=false) {
    currentIndex = index;
    modalImg.classList.remove("loaded");
    if (modalSpinner) modalSpinner.style.display = "block";

    // const lowRes = getLowResUrl(images[currentIndex].src);
    const fullRes = getFullResUrl(images[currentIndex].src);

    // prefetch next and previous images (way smoother)
    prefetchImage((currentIndex + 1) % images.length);
    prefetchImage((currentIndex - 1 + images.length) % images.length);

    if (loadedImages.has(fullRes)) {
      // If the image has been loaded before, skip to full-res loading
      modalImg.src = fullRes;

      if (showCaption) caption.textContent = images[currentIndex].alt;

      requestAnimationFrame(() => {
        if (modalSpinner) modalSpinner.style.display = "none";
        modalImg.classList.add("loaded");
      });
      return; // exit early
    }

    // Get the full image source by removing 'tr' from the src
    const fullImage = new Image();
    fullImage.src = fullRes;

    fullImage.onload = function () {
      modalImg.src = fullRes;
      if (showCaption) caption.textContent = images[currentIndex].alt;

      loadedImages.add(fullRes);

      requestAnimationFrame(() => {
        if (modalSpinner) modalSpinner.style.display = "none";
        modalImg.classList.add("loaded");
      });
    };
  }

  images.forEach((img, index) => {
    img.onclick = function () {
      openModal(index);
    };
  });

  // allow the keyboard arrows to navigate
  document.addEventListener("keydown", function (event) {
    if (modal.style.display === "flex") {
      if (event.key === "ArrowLeft") {
        prevBtn.click();
      } else if (event.key === "ArrowRight") {
        nextBtn.click();
      } else if (event.key === "Escape") {
        closeModal();
      }
    }
  });

  prevBtn.onclick = function () {
    if (currentIndex === minIndex) {
      loadImage(maxIndex);
      currentIndex = maxIndex;
      return;
    }
    loadImage((currentIndex - 1) % images.length);
  };

  nextBtn.onclick = function () {
    loadImage((currentIndex + 1) % images.length);
  };

  // close modal when clicking outside of image
  window.onclick = function (event) {
    if (
      event.target == modal ||
      event.target == modalFrame ||
      event.target == caption
    ) {
      closeModal();
    }
  };
});

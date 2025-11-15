document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("imageModal");
  const modalFrame = document.getElementById("modalFrame");
  const modalImg = document.getElementById("fullImage");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const caption = document.getElementById("caption");
  const images = document.querySelectorAll(".grid-item");
  const loadedImages = new Set();
  let currentIndex = 0;

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

  function loadImage(index) {
    currentIndex = index;
    modalImg.classList.remove("loaded");

    // const lowRes = getLowResUrl(images[currentIndex].src);
    const fullRes = getFullResUrl(images[currentIndex].src);

    if (loadedImages.has(fullRes)) {
      // If the image has been loaded before, skip to full-res loading
      modalImg.src = fullRes;
      modalImg.contextmenu = false;
      modalImg.addEventListener("contextmenu", function (e) {
        e.preventDefault();
        return false;
      });

      caption.textContent = images[currentIndex].alt;
      requestAnimationFrame(() => {
        modalImg.classList.add("loaded");
      });
      return; // exit early
    }

    // Get the full image source by removing 'tr' from the src
    const fullImage = new Image();
    fullImage.src = fullRes;

    fullImage.onload = function () {
      modalImg.src = fullRes;
      modalImg.contextmenu = false;
      modalImg.addEventListener("contextmenu", function (e) {
        e.preventDefault();
        return false;
      });
      caption.textContent = images[currentIndex].alt;

      loadedImages.add(fullRes);

      requestAnimationFrame(() => {
        modalImg.classList.add("loaded");
      });

      // prefetch next and previous images (way smoother)
      prefetchImage((currentIndex + 1) % images.length);
      prefetchImage((currentIndex - 1) % images.length);
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
        modal.style.display = "none";
        modalImg.src = "";
        modal.classList.remove("show");
      }
    }
  });

  prevBtn.onclick = function () {
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

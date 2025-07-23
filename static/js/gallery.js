document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('fullImage');
    const closeBtn = document.getElementsByClassName('close')[0];
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const caption = document.getElementById('caption');
    const images = document.querySelectorAll('.grid-item');
    let currentIndex = 0;

    document.querySelectorAll('.grid-item').forEach((img, index) => {
        img.onclick = function () {
            modal.style.display = 'flex';
            modal.classList.add('show');
            modalImg.src = this.src;
            currentIndex = index;
            caption.textContent = this.alt || 'Image ' + (index + 1);
        }
    });

    closeBtn.onclick = function () {
        modal.style.display = 'none';
        modal.classList.remove('show');
    }

    prevBtn.onclick = function () {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        console.log('Current Index:', currentIndex);
        modalImg.src = images[currentIndex].src;
        caption.textContent = images[currentIndex].alt || 'Image ' + (currentIndex + 1);

    }

    nextBtn.onclick = function () {
        currentIndex = (currentIndex + 1) % images.length;
        modalImg.src = images[currentIndex].src;
        caption.textContent = images[currentIndex].alt || 'Image ' + (currentIndex + 1);

    }

    // close modal when clicking outside of image
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
            modal.classList.remove('show');
        }
        if (event.target == modalImg) {
            modal.style.display = 'none';
        }
    }
});
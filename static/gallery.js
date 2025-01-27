document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('fullImage');
    const closeBtn = document.getElementsByClassName('close')[0];
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const images = document.querySelectorAll('.gallery-image');
    let currentIndex = 0;

    document.querySelectorAll('.gallery-image').forEach((img, index) => {
        img.onclick = function() {
            modal.style.display = 'flex';
            modal.classList.add('show');
            modalImg.src = this.src;
            currentIndex = index;
        }
    });

    closeBtn.onclick = function() {
        modal.style.display = 'none';
        modal.classList.remove('show');
    }

    prevBtn.onclick = function() {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        modalImg.src = images[currentIndex].src;
    }

    nextBtn.onclick = function() {
        currentIndex = (currentIndex + 1) % images.length;
        modalImg.src = images[currentIndex].src;
    }

    // close modal when clicking outside of image
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
            modal.classList.remove('show');
        }
        if (event.target == modalImg) {
            modal.style.display = 'none';
        }
    }
});
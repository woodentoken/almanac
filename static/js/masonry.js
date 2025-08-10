let msnry; // Declare in outer scope

document.addEventListener('DOMContentLoaded', function () {
    const grid = document.querySelector('.masonry');
    const gutterSize = window.innerWidth < 700 ? 16 : 32;

    msnry = new Masonry(grid, {
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        gutter: gutterSize,
        percentPosition: true,
        transitionDuration: '0.1s',
    });

    imagesLoaded(grid, () => {
        msnry.layout();
    });
});

window.addEventListener('resize', () => {

  if (msnry) {
    console.log("masonry layout")
    msnry.layout();
  }
});

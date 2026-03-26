let msnry; // Declare in outer scope

document.addEventListener('DOMContentLoaded', function () {
  const grid = document.querySelector('.masonry');
  const gutterSize = 32;

  grid.style.opacity = '0';

  const spinner = document.createElement('div');
  spinner.className = 'masonry-spinner';
  grid.parentNode.insertBefore(spinner, grid);

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

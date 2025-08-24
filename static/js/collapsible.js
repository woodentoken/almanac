document.addEventListener('DOMContentLoaded', function() {

  let menuButton = document.getElementsByClassName('menu-button')[0];
  let menu = document.getElementsByClassName('collapsible')[0];

  console.log("loaded menuButton")

  menuButton.addEventListener('click', function() {
    menuButton.classList.toggle('open');
    menuButton.style.content = "";
    if (menu.style.maxHeight) {
      menu.style.maxHeight = null;
    } else {
      menu.style.maxHeight = menu.scrollHeight + 'px';
    }
  });
});

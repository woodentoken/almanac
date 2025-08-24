document.addEventListener('DOMContentLoaded', function() {
  const toggle = document.getElementById('toggle');
  const body = document.body;
  const currentTheme = localStorage.getItem('theme');

  // Load preference
  if (localStorage.getItem("theme") === "dark-mode") {
    body.classList.add("dark-mode");
  }
   else {
    body.classList.add("light-mode");
  }

  toggle.addEventListener('click', function() {
    if (body.classList.contains('light-mode')) {
      // toggle.src = "static/logo/almanac_logo_white.svg";
      body.classList.replace('light-mode', 'dark-mode');
      localStorage.setItem('theme', 'dark-mode');
    } else {
      // toggle.src = "static/logo/almanac_logo.svg";
      body.classList.replace('dark-mode', 'light-mode');
      localStorage.setItem('theme', 'light-mode');
    }
  });
});

(function() {
  try {
    // Check saved preference
    const theme = localStorage.getItem('theme');
    if (theme === 'dark-mode' || (!theme && window.matchMedia('(prefers-color-scheme: dark-mode)').matches)) {
      document.documentElement.classList.add('dark-mode');
    } else {
      document.documentElement.classList.replace('dark-mode', 'light-mode');
    }
  } catch (e) {}
})();


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

    // ensures the document follows the color scheme changes
    if (document.documentElement.classList.contains('dark-mode')) {
      document.documentElement.classList.replace('dark-mode', 'light-mode');
      // localStorage.setItem('theme', 'light-mode');
    } else {
      document.documentElement.classList.replace('light-mode', 'dark-mode');
      // localStorage.setItem('theme', 'dark-mode');
    }


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

// Update copyright end year to current year on page load
document.addEventListener('DOMContentLoaded', function () {
  try {
    var currentYear = new Date().getFullYear();
    document.querySelectorAll('p').forEach(function (p) {
      p.innerHTML = p.innerHTML.replace(/((?:©|&copy;)\s*2002-)\d{4}/g, '$1' + currentYear);
    });
  } catch (e) {
    // No-op if anything unexpected happens
  }
});


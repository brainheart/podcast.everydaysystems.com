// Update copyright end year to current year on page load
document.addEventListener('DOMContentLoaded', function () {
  try {
    var currentYear = new Date().getFullYear();
    document.querySelectorAll('p').forEach(function (p) {
      p.innerHTML = p.innerHTML.replace(/((?:©|&copy;)\s*2002-)\d{4}/g, '$1' + currentYear);
    });

    // Episode layout tweaks
    var isEpisode = /\/episode\//.test(location.pathname);
    if (isEpisode) {
      var hasYouTube = !!document.querySelector('iframe.yt-player, iframe[src*="youtube.com/embed/"]');

      // Find the discuss link near the top
      var discussLink = Array.from(document.querySelectorAll('a')).find(function (a) {
        return /everydaysystems\.com\/bb\/viewtopic\.php/.test(a.href);
      });

      // Handle the top listen/discuss container
      if (discussLink) {
        var container = discussLink.closest('div');
        // Try to find the mp3 link within the same container
        var mp3Link = container ? Array.from(container.querySelectorAll('a')).find(function (a) { return /\.mp3($|\?)/i.test(a.href); }) : null;

        if (hasYouTube) {
          // Remove entire container if YouTube player is present
          if (container) container.remove();
        } else if (container) {
          // Keep only the mp3 link, relabel as Download mp3
          if (mp3Link) {
            mp3Link.textContent = 'Download mp3';
            // Rebuild container content to include only the mp3 link
            container.innerHTML = '';
            container.appendChild(mp3Link);
          } else {
            // If no mp3 link found, just remove the discuss link from the container
            discussLink.remove();
          }
        }
      }

      // Move discuss link to bottom (centered)
      if (discussLink) {
        var href = discussLink.href;
        var main = document.getElementById('main') || document.body;
        var copyrightP = Array.from(main.querySelectorAll('p')).find(function (p) {
          return /©|&copy;/.test(p.innerHTML);
        });
        var wrapper = document.createElement('p');
        wrapper.style.textAlign = 'center';
        var a = document.createElement('a');
        a.href = href;
        a.textContent = 'Discuss';
        wrapper.appendChild(a);
        if (copyrightP && copyrightP.parentNode === main) {
          main.insertBefore(wrapper, copyrightP);
        } else {
          main.appendChild(wrapper);
        }
      }
    }
  } catch (e) {
    // No-op if anything unexpected happens
  }
});

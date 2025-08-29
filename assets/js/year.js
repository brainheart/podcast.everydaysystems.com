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
      // YouTube mapping for episode pages (episode number -> videoId)
      var YT_MAP = {
        97: '4q_A1BM5uVQ', 96: 'OviAmhuH5XQ', 95: '2GhvhyBxYzw', 94: 'jlYWnuZKF1o',
        93: '9llV0O3-3a4', 92: '0ky0-OOfwK8', 91: 'u3nG1o_0NJ4', 90: 'na0e_HBs4G4',
        89: 'Vj3iqj7t7hg', 88: 'f0kCUfnFxaA', 87: 'T1yWC786bdI', 86: 'hCDeVAQhR94',
        85: 'Ug9OxZ4ajc4', 84: 'Bogr5W9K8ss', 83: '4lWvwcF5sh0', 82: 'VzCZQ7Aqqvc',
        81: 'zFiXcq7pKuA', 80: '8nkV_5d3MeU', 79: 'E3tE4kJySxA', 78: 'S7edZbzsDVg',
        77: 'ktPW5igIcA0', 76: 'UFPgaf02_S8', 75: 'NX2qs9Gog4U', 74: 'OjjPDIUSb-g',
        73: '4Tj9xRdFn2Q', 72: '9efWaX8I2IQ', 71: '1BWNeGl6z3k', 70: 'amzw6KB8SuI',
        69: 'UIVmdpCrkR4', 68: 'weYYsPfRTXk', 67: '_UTIbzQwsDQ', 66: 'Arfx5mUbl9E',
        65: 'hAGSy2mEGWU', 64: 'RSxTdQIUKrc', 63: 'B9-mClalIrU', 62: 'DjwabKO0oiE',
        61: '9waT5fdKQRA', 60: 'ZnLkwOMtb8U', 59: 'Tu3RFavl1q8', 58: 'LnsFIjF7Zh4',
        57: 'C3ZKYmn_ivw', 56: 'X9-wv8HyQfc', 55: '2QeLHhK0BU8', 54: 'hHNdgaVPFhY',
        52: 'XjkcgxyRALs', 51: '6wcn7NP4zRw', 50: 'Y6M-XtbvEH4', 49: '3dKftMpoemo',
        47: 'Ha1ZXNcAlKQ', 46: 'fxsexDDdi4U', 44: 'BRqTjqXyUuE', 43: 'EVcY51Z1sDM',
        42: 'XJdrF6zDUhQ', 41: 'rhOP08He2jE', 40: 'fOAL1zVvLqU', 39: 'j8jO2RqjSPo',
        38: 'MWHqKG0qef0', 37: '_hTUJ2Cr7Us', 36: 'CR7U9KEgZPU', 35: '4zRsHWBGUkQ',
        34: 'KYYPhPX9BvU', 33: 'jRmq3Cux5BQ', 32: 'G8hf_-6VIeQ', 31: 'KfyUPqLJG-I',
        30: 'jwZBOn-9r88', 29: 'REu0xnuwLi0', 28: 'ogV-8MIpqNw', 27: 'LS_2ysSp0qc',
        26: 'X8vBD_m2KYk', 24: '5CJXX3E-G5Y', 23: 'mvE83iNDO18', 22: 'U6elINxzJmg',
        21: 'ycEMVvJbta8', 20: 'tzeQdXEqfxQ', 19: 'fPvDEGizPQM', 18: 'FyofH6vfO70',
        17: '4P_xaLqYM00', 16: '4kiMYwG0ZMA', 15: 'FKpys7YpfTc', 14: 'YrP4i3sveVw',
        13: '4qLpv1v11RY', 12: 'Ezn28IXkzIs', 11: 'rYiM-ESfBsk', 10: '4QZ3ZvOATo0',
        9: 'xmhYMK409q8', 8: 'k48amXIBeEo', 7: 'MNmPxrgnqx8', 6: 'vVj1rfekLmc',
        5: 'xUPKL5NDpZI', 4: 'uzyTCVEdeAI', 3: 'Fljyi2Uwm9I', 2: '7L_WRUIDBHs', 1: 'hTe7-3Q0Tbw'
      };

      // Inject YouTube iframe if mapping exists and none present
      var epMatch = location.pathname.match(/\/episode\/(\d+)\/?/);
      if (epMatch) {
        var epNum = parseInt(epMatch[1], 10);
        var vid = YT_MAP[epNum];
        if (vid && !document.querySelector('iframe.yt-player, iframe[src*="youtube.com/embed/"]')) {
          var main = document.getElementById('main') || document.body;
          // Prefer to place right after the Listen block; otherwise before the lead image; otherwise after the episode h2; otherwise top of main
          var mp3Container = Array.from(document.querySelectorAll('div')).find(function (d) {
            return !!Array.from(d.querySelectorAll('a')).find(function (a) { return /\.mp3($|\?)/i.test(a.href); });
          });
          var leadImg = main.querySelector('#lead-image, #hamburger_flagellants');
          var h2 = main.querySelector('h2') || document.querySelector('h2');
          var anchor = mp3Container || null;
          var iframe = document.createElement('iframe');
          iframe.className = 'yt-player';
          iframe.width = '100%';
          iframe.height = '200';
          iframe.loading = 'lazy';
          iframe.allowFullscreen = true;
          iframe.referrerPolicy = 'strict-origin-when-cross-origin';
          iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
          iframe.title = 'Everyday Systems Podcast Episode ' + epNum;
          iframe.src = 'https://www.youtube-nocookie.com/embed/' + vid + '?modestbranding=1&rel=0&playsinline=1';
          if (anchor && anchor.parentNode) {
            anchor.insertAdjacentElement('afterend', iframe);
          } else if (leadImg && leadImg.parentNode) {
            leadImg.insertAdjacentElement('beforebegin', iframe);
          } else if (h2 && h2.parentNode) {
            h2.insertAdjacentElement('afterend', iframe);
          } else {
            main.insertAdjacentElement('afterbegin', iframe);
          }
        }
      }

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
        var mp3Href = mp3Link ? mp3Link.href : null;

        if (hasYouTube) {
          // Remove only the top Listen/Discuss block; do NOT remove #main
          if (container && mp3Link && container !== (document.getElementById('main'))) {
            container.remove();
          }

          // If we have an mp3 url, render a centered Download mp3 under the YouTube iframe
          if (mp3Href) {
            var iframe = document.querySelector('iframe.yt-player, iframe[src*="youtube.com/embed/"]');
            if (iframe && iframe.parentNode) {
              var p = document.createElement('p');
              p.style.textAlign = 'center';
              var a = document.createElement('a');
              a.href = mp3Href;
              a.textContent = 'Download mp3';
              p.appendChild(a);
              iframe.insertAdjacentElement('afterend', p);
            }
          }
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

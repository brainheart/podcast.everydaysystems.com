// Replace homepage mp3 links with YouTube links for recent episodes
document.addEventListener('DOMContentLoaded', function () {
  try {
    var map = {
      97: '4q_A1BM5uVQ',
      96: 'OviAmhuH5XQ',
      95: '2GhvhyBxYzw',
      94: 'jlYWnuZKF1o',
      93: '9llV0O3-3a4',
      92: '0ky0-OOfwK8',
      91: 'u3nG1o_0NJ4',
      90: 'na0e_HBs4G4',
      89: 'Vj3iqj7t7hg',
      88: 'f0kCUfnFxaA',
      87: 'T1yWC786bdI',
      86: 'hCDeVAQhR94',
      85: 'Ug9OxZ4ajc4',
      84: 'Bogr5W9K8ss',
      83: '4lWvwcF5sh0'
    };

    // Only modify homepage links
    var path = (location.pathname || '').replace(/\/$/, '/');
    if (path === '/' || /\/index\.html$/.test(path)) {
      document.querySelectorAll('a').forEach(function (a) {
        if (a.textContent.trim().toLowerCase() === 'mp3' && /libsyn\.com\/.+\.mp3/.test(a.href)) {
          var m = a.href.match(/eds-(\d+)-/i);
          if (m) {
            var ep = parseInt(m[1], 10);
            if (map[ep]) {
              a.href = 'https://www.youtube.com/watch?v=' + map[ep];
              a.textContent = 'youtube';
              a.setAttribute('rel', 'noopener');
            }
          }
        }
      });
    }
  } catch (e) {
    // no-op
  }
});


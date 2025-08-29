// Replace homepage mp3 links with YouTube links for recent episodes
document.addEventListener('DOMContentLoaded', function () {
  try {
    var map = {
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

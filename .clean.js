const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf-8');

// Find the 3 Baidu fallback code blocks and replace them
// Pattern 1: rcBid (has days, dc variables)
// Pattern 2: rcPot (has score-badge)
// Pattern 3: rcDone (has cc, pc variables)

// rcBid - Baidu fallback in the company link
const pattern1 = /var nm=r\.website&&r\.website!==\x27—\x27\x3f\x27<a href=\\x22\x27\+r\.website\+\x27\\x22 target=\\x22_blank\\x22 rel=\\x22noopener\\x22 style=\\x22color:inherit;text-decoration:none\\x22>\x27\+r\.company\+\x27 🌐<\/a>\x27:\x27<a href=\\x22https:\/\/www\.baidu\.com\/s\?wd=\x27\+encodeURIComponent\(r\.company\)\+\x27%20%E5%AE%98%E7%BD%91\\x22 target=\\x22_blank\\x22 rel=\\x22noopener\\x22 style=\\x22color:inherit;text-decoration:none\\x22>\x27\+r\.company\+\x27 🔍<\/a>\x27;\n  var h=/g;

const pattern2 = /var nm=r\.website&&r\.website!==\x27—\x27\x3f\x27<a href=\x22\x27\+r\.website\+\x27\x22 target=\x22_blank\x22 rel=\x22noopener\x22 style=\x22color:inherit;text-decoration:none\x22>\x27\+r\.company\+\x27 🌐<\/a>\x27:\x27<a href=\x22https:\/\/www\.baidu\.com\/s\?wd=\x27\+encodeURIComponent\(r\.company\)\+\x27%20%E5%AE%98%E7%BD%91\x22 target=\x22_blank\x22 rel=\x22noopener\x22 style=\x22color:inherit;text-decoration:none\x22>\x27\+r\.company\+\x27 🔍<\/a>\x27;\n  var h=/g;

const replacement = "var nm=r.website&&r.website!=='—'?'<a href=\"" + "+r.website+" + '" target="_blank" rel="noopener" style="color:inherit;text-decoration:none">' + "+r.company+" + ' 🌐</a>\':r.company;\n  var h=';

// Actually, let me just do simple string replace
const searchText = 'https://www.baidu.com/s?wd=\'+encodeURIComponent(r.company)+\'%20%E5%AE%98%E7%BD%91" target="_blank" rel="noopener" style="color:inherit;text-decoration:none">\'+r.company+\' 🔍</a>\'';
const replaceWith = '#" target="_self" style="color:inherit;text-decoration:none;cursor:default">\'+r.company+\'</a>\'';

// First, find all instances of the Baidu pattern
const baiduLines = html.match(/baidu\.com\/s\?wd=.*?🔍/g);
console.log('Baidu references found:', baiduLines ? baiduLines.length : 0);

if (baiduLines && baiduLines.length > 0) {
  // Replace each
  html = html.split(searchText).join(replaceWith);
  console.log('Replaced all Baidu search links');
}

fs.writeFileSync('index.html', html, 'utf-8');
console.log('Done');

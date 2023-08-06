
try {
  new Function("import('/hacsfiles/frontend/c.01a10b33.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/c.01a10b33.js';
  document.body.appendChild(el);
}
  
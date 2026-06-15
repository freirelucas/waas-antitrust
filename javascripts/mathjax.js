// Configuração MathJax 3 para arithmatex (generic) sob Material for MkDocs.
// Sem este arquivo, o math em <span class="arithmatex">\(...\)</span> pode
// não ser renderizado em todos os navegadores (notadamente quando o tema
// Material aplica seu próprio loader de scripts).
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
  },
};

document$.subscribe(() => {
  if (typeof MathJax !== "undefined" && MathJax.startup) {
    MathJax.startup.output.clearCache();
    MathJax.typesetClear();
    MathJax.texReset();
    MathJax.typesetPromise();
  }
});

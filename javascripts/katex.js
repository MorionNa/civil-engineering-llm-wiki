document$.subscribe(function () {
  document.querySelectorAll(".arithmatex").forEach(function (el) {
    var tex = el.textContent;
    var displayMode = false;
    if (tex.startsWith("\\[") && tex.endsWith("\\]")) {
      tex = tex.slice(2, -2);
      displayMode = true;
    } else if (tex.startsWith("\\(") && tex.endsWith("\\)")) {
      tex = tex.slice(2, -2);
    }
    katex.render(tex, el, { throwOnError: false, displayMode: displayMode });
  });
});

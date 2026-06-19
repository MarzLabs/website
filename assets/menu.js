/* Menú móvil — mejora progresiva, sin dependencias.
   Sin JS la navegación permanece visible; con JS se colapsa tras el botón. */
(function () {
  "use strict";

  // Marca que JS está disponible (la hoja de estilos usa .js para colapsar el menú).
  document.documentElement.classList.add("js");

  document.addEventListener("DOMContentLoaded", function () {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("primary-nav");
    if (!toggle || !nav) return;

    function setOpen(open) {
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
    }

    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });

    // Cerrar con Escape para usuarios de teclado.
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        toggle.focus();
      }
    });
  });
})();

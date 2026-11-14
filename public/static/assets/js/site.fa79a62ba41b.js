// Dr. Sepideh Safanavaei: the shell's behaviour. No framework, no build step.
// 1. Phone menu: a disclosure. Escape closes it and returns focus to the button.
// 2. Floating call tab: hidden while any [data-call-anchor] is on screen.
// 3. Credential flip cards: tap (and Enter/Space) toggle aria-pressed; hover
//    and keyboard focus turn them in CSS. Escape turns a card back.
(function () {
  "use strict";

  // ---- 1. phone menu ----------------------------------------------------
  var button = document.querySelector(".site-header__menu");
  var menu = document.querySelector("[data-menu]");
  if (button && menu) {
    button.hidden = false;
    var setOpen = function (open) {
      button.setAttribute("aria-expanded", String(open));
      menu.classList.toggle("is-open", open);
      button.querySelector(".sr-only").textContent = open ? "بستن منو" : "منو";
    };
    button.addEventListener("click", function () {
      setOpen(button.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && button.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        button.focus();
      }
    });
    // Leaving the phone layout (rotation, resize) closes the menu.
    var wide = window.matchMedia("(min-width: 961px)");
    wide.addEventListener("change", function () { if (wide.matches) setOpen(false); });
  }

  // ---- 2. floating call tab --------------------------------------------
  var tab = document.querySelector("[data-calltab]");
  var anchors = document.querySelectorAll("[data-call-anchor]");
  if (tab && !(anchors.length && "IntersectionObserver" in window)) {
    tab.classList.remove("is-hidden");
  } else if (tab) {
    var visible = new Set();
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) visible.add(entry.target);
        else visible.delete(entry.target);
      });
      tab.classList.toggle("is-hidden", visible.size > 0);
    });
    anchors.forEach(function (anchor) { observer.observe(anchor); });
  }

  // ---- 3. credential flip cards ----------------------------------------
  document.querySelectorAll("[data-flip]").forEach(function (card) {
    var pointer = "";
    card.addEventListener("pointerdown", function (event) { pointer = event.pointerType; });
    card.addEventListener("click", function () {
      // A mouse already turns the card on hover; a click must not leave it stuck.
      if (pointer !== "mouse") {
        card.setAttribute("aria-pressed", String(card.getAttribute("aria-pressed") !== "true"));
      }
      pointer = "";
    });
    card.addEventListener("keydown", function (event) {
      if (event.key === "Escape") card.setAttribute("aria-pressed", "false");
    });
  });
})();

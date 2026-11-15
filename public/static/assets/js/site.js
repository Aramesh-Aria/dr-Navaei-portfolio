// Dr. Sepideh Safanavaei: the shell's behaviour. No framework, no build step.
// 1. Phone menu: a disclosure. Escape closes it and returns focus to the button.
// 2. Floating call tab: hidden while any [data-call-anchor] is on screen.
// 3. Credential flip cards: tap (and Enter/Space) toggle aria-pressed; hover
//    and keyboard focus turn them in CSS. Escape turns a card back.
// 4. Copy an address (for a taxi app): the button shows only where the
//    clipboard is available, confirms in place and through a live region.
// 5. Forms: a sent state or an error summary takes focus on load; the send
//    button says it is sending and refuses a second press; the call tab steps
//    aside while a field is being typed in.
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

  // ---- 4. copy an address ---------------------------------------------
  var status = document.querySelector("[data-copy-status]");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (navigator.clipboard && window.isSecureContext) {
    document.querySelectorAll("[data-copy]").forEach(function (copy) {
      var label = copy.querySelector("[data-copy-label]");
      var icon = copy.querySelector("use");
      var idle = label.textContent;
      var timer;
      copy.hidden = false;
      var show = function (text, href) {
        label.textContent = text;
        icon.setAttribute("href", href);
        if (status) status.textContent = text + ".";
        clearTimeout(timer);
        timer = setTimeout(function () {
          label.textContent = idle;
          icon.setAttribute("href", "#i-copy");
          if (status) status.textContent = "";
        }, 2400);
      };
      copy.addEventListener("click", function () {
        navigator.clipboard.writeText(copy.getAttribute("data-copy")).then(function () {
          show("نشانی کپی شد", "#i-check");
          // The check settles in (state change made legible); the way back stays instant.
          var svg = icon.parentNode;
          if (svg.animate) {
            var easeOut = getComputedStyle(svg).getPropertyValue("--ease-out").trim() || "ease-out";
            svg.animate(reduce.matches
              ? [{ opacity: 0.4 }, { opacity: 1 }]
              : [{ opacity: 0.4, transform: "scale(0.8)" }, { opacity: 1, transform: "none" }],
              { duration: 180, easing: easeOut });
          }
        }, function () {
          // Refused (no permission, an embedded view): say so; the address is right above.
          show("کپی نشد", "#i-alert");
        });
      });
    });
  }

  // ---- 5. forms --------------------------------------------------------
  var focusTarget = document.querySelector("[data-focus-on-load]");
  if (focusTarget) focusTarget.focus();
  document.querySelectorAll("[data-form]").forEach(function (form) {
    var send = form.querySelector("[data-send]");
    var sendLabel = send && send.querySelector("[data-send-label]");
    var idleLabel = sendLabel && sendLabel.textContent;
    form.addEventListener("submit", function (event) {
      if (send.getAttribute("aria-disabled") === "true") { event.preventDefault(); return; }
      send.setAttribute("aria-disabled", "true");
      sendLabel.textContent = "در حال فرستادن…";
    });
    // While a field has focus the call tab steps aside (it would float over the
    // field above the phone keyboard).
    form.addEventListener("focusin", function (event) {
      if (event.target.matches("input, textarea")) document.documentElement.classList.add("is-typing");
    });
    form.addEventListener("focusout", function () { document.documentElement.classList.remove("is-typing"); });
    // Coming back with the back button (bfcache) must not leave it stuck.
    window.addEventListener("pageshow", function () {
      send.removeAttribute("aria-disabled");
      sendLabel.textContent = idleLabel;
    });
  });

  // The captcha's "new image" button: a hard-to-read image is swapped for a
  // fresh one in place, without reloading the form. Hidden until this runs.
  document.querySelectorAll("[data-captcha-refresh]").forEach(function (button) {
    var field = button.closest(".field");
    var image = field.querySelector("[data-captcha-image]");
    var key = field.querySelector('input[type="hidden"]');
    var answer = field.querySelector('input:not([type="hidden"])');
    button.hidden = false;
    button.addEventListener("click", function () {
      button.disabled = true;
      fetch(button.dataset.captchaRefresh, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(function (response) { return response.ok ? response.json() : null; })
        .then(function (data) {
          if (!data) return;
          image.src = data.image_url;
          key.value = data.key;
          answer.value = "";
          answer.focus();
        })
        .catch(function () {})
        .finally(function () { button.disabled = false; });
    });
  });
})();

// 共用：密碼小眼睛 + 寄送驗證碼（有 JS 則 AJAX，無 JS 則表單）
(function () {
  // === 這段取代原本的 bindEyeButtons：支援 eye ↔ eye-off、aria-label 切換 ===
  function bindPasswordToggles() {
    document.querySelectorAll(".pw-toggle, .eye-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const target = document.getElementById(btn.dataset.target);
        if (!target) return;

        const showLabel = btn.dataset.labelShow || "Show password";
        const hideLabel = btn.dataset.labelHide || "Hide password";

        const toShow = target.type === "password";
        target.type = toShow ? "text" : "password";
        btn.setAttribute("aria-label", toShow ? hideLabel : showLabel);

        // 切換圖示（需要按鈕裡有 .icon-eye / .icon-eye-off 兩個 SVG）
        const eye = btn.querySelector(".icon-eye");
        const eyeOff = btn.querySelector(".icon-eye-off");
        if (eye && eyeOff) {
          eye.style.display = toShow ? "none" : "inline";
          eyeOff.style.display = toShow ? "inline" : "none";
        }
      });
    });
  }

  // ===== 以下你原本就有：完全保留 =====
  function startCooldown(sec, btn, hint) {
    let t = sec;
    const base = btn.textContent;
    btn.disabled = true;
    const timer = setInterval(() => {
      t -= 1;
      hint.textContent = `再送まで ${t}s`;
      if (t <= 0) {
        clearInterval(timer);
        hint.textContent = "";
        btn.disabled = false;
        btn.textContent = base;
      }
    }, 1000);
  }

  function setupRegisterSendCode() {
    const form = document.getElementById("sendCodeForm");
    if (!form) return; // login 頁沒有這個表單

    const email = document.getElementById("email");
    const email2 = document.getElementById("email_confirm");
    const status = document.getElementById("codeStatus");
    const hint = document.getElementById("sendCodeHint");
    const btn = document.getElementById("sendCodeBtn");

    function syncEmailsToLower() {
      const e3 = document.getElementById("email2");
      const e4 = document.getElementById("email2_confirm");
      if (e3) e3.value = email.value.trim();
      if (e4) e4.value = email2.value.trim();
    }

    form.addEventListener("submit", async (ev) => {
      // Progressive Enhancement：先試 AJAX，不行就讓瀏覽器正常送出
      if (!window.fetch) return;
      ev.preventDefault();

      const v = email.value.trim();
      const v2 = email2.value.trim();
      if (!v || !v2 || v !== v2) {
        status.textContent = form.dataset.errMismatch || "メールアドレスが一致しません";
        status.className = "msg error";
        return;
      }
      const fd = new FormData(form);
      try {
        btn.disabled = true;
        hint.textContent = form.dataset.sending || "送信中…";
        status.textContent = "";
        const res = await fetch("/register/send-code.json", { method: "POST", body: fd });
        const data = await res.json();
        status.textContent = data.message || "";
        status.className = data.ok ? "msg" : "msg error";
        if (data.ok) startCooldown(60, btn, hint);
      } catch (e) {
        form.submit(); // 失敗時退回表單提交（/register/send-code）
      } finally {
        syncEmailsToLower();
      }
    });
  }

  function init() {
    bindPasswordToggles();     // ← 用新的
    setupRegisterSendCode();   // ← 保留原本寄送驗證碼
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

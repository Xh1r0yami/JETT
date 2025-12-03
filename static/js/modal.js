document.addEventListener("DOMContentLoaded", () => {

  // ================= MODALS =================
  const modals = {
    chooseRole: document.getElementById("chooseRoleModal"),
    loginSeeker: document.getElementById("loginSeekerModal"),
    loginCompany: document.getElementById("loginCompanyModal"),
    registerSeeker: document.getElementById("registerSeekerModal"),
    registerCompany: document.getElementById("registerCompanyModal"),
    verifySeeker: document.getElementById("verifySeekerModal"),
    verifyCompany: document.getElementById("verifyCompanyModal"),
    resetRequest: document.getElementById("resetPasswordModal"),
    resetConfirm: document.getElementById("resetPasswordConfirmModal"),
  };

  // ================= OPEN CHOOSE ROLE =================
  const signinBtn = document.getElementById("openLoginModal");
  if (signinBtn) {
    signinBtn.addEventListener("click", e => {
      e.preventDefault();
      modals.chooseRole.style.display = "flex";
    });
  }

  // ================= ROLE BUTTONS =================
  const loginSeekerBtn = document.getElementById("loginSeekerBtn");
  const loginCompanyBtn = document.getElementById("loginCompanyBtn");
  if (loginSeekerBtn) loginSeekerBtn.onclick = () => {
    modals.chooseRole.style.display = "none";
    modals.loginSeeker.style.display = "flex";
  };
  if (loginCompanyBtn) loginCompanyBtn.onclick = () => {
    modals.chooseRole.style.display = "none";
    modals.loginCompany.style.display = "flex";
  };

  // ================= SWITCH MODAL (LOGIN <-> REGISTER) =================
  const switchLinks = [
    { linkId: "openRegisterSeekerLink", closeModal: modals.loginSeeker, openModal: modals.registerSeeker },
    { linkId: "openLoginSeekerLink", closeModal: modals.registerSeeker, openModal: modals.loginSeeker },
    { linkId: "openRegisterCompanyLink", closeModal: modals.loginCompany, openModal: modals.registerCompany },
    { linkId: "openLoginCompanyLink", closeModal: modals.registerCompany, openModal: modals.loginCompany }
  ];
  switchLinks.forEach(item => {
    const link = document.getElementById(item.linkId);
    if (link) {
      link.addEventListener("click", e => {
        e.preventDefault();
        if (item.closeModal) item.closeModal.style.display = "none";
        if (item.openModal) item.openModal.style.display = "flex";
      });
    }
  });

  // ================= FORGOT PASSWORD =================
  const forgotSeeker = document.getElementById("openForgotSeekerLink");
  const forgotCompany = document.getElementById("openForgotCompanyLink");
  if (forgotSeeker)
    forgotSeeker.addEventListener("click", e => {
      e.preventDefault();
      modals.loginSeeker.style.display = "none";
      modals.resetRequest.style.display = "flex";
    });
  if (forgotCompany)
    forgotCompany.addEventListener("click", e => {
      e.preventDefault();
      modals.loginCompany.style.display = "none";
      modals.resetRequest.style.display = "flex";
    });

  // ================= CLOSE MODALS =================
  document.querySelectorAll(".close").forEach(btn => {
    btn.addEventListener("click", () => {
      const target = document.getElementById(btn.dataset.close);
      if (target) target.style.display = "none";
    });
  });

  // Tutup modal verifikasi pakai tombol button
  const closeVerifySeeker = document.getElementById("closeVerifySeeker");
  if (closeVerifySeeker && modals.verifySeeker) {
    closeVerifySeeker.addEventListener("click", () => {
      modals.verifySeeker.style.display = "none";
    });
  }
  const closeVerifyCompany = document.getElementById("closeVerifyCompany");
  if (closeVerifyCompany && modals.verifyCompany) {
    closeVerifyCompany.addEventListener("click", () => {
      modals.verifyCompany.style.display = "none";
    });
  }

  window.addEventListener("click", e => {
    if (e.target.classList.contains("modal")) e.target.style.display = "none";
  });

  // ================= SHOW MESSAGES =================
  function showMessage(id, messages, kind="error") {
    const el = document.getElementById(id);
    if (!el) return alert(messages);

    el.className = "message-box " + kind;
    el.innerHTML = "";

    if (Array.isArray(messages)) {
      messages.forEach(msg => {
        const p = document.createElement("p");
        p.textContent = msg;
        el.appendChild(p);
      });
    } else if (typeof messages === "object") {
      Object.values(messages).forEach(arr => {
        arr.forEach(msg => {
          const p = document.createElement("p");
          p.textContent = msg;
          el.appendChild(p);
        });
      });
    } else {
      el.textContent = messages;
    }

    if (kind === "success") {
      setTimeout(() => {
        el.textContent = "";
        el.className = "message-box";
      }, 3000);
    }
  }

  // ================= CSRF =================
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie("csrftoken");

  // ================= HANDLE FORM SUBMIT =================
  function handleForm(formId, messageId, modalClose=null, modalOpen=null) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener("submit", async e => {
      e.preventDefault();

      const formData = new FormData(form);

      try {
        const res = await fetch(form.action, {
          method: "POST",
          body: formData,
          headers: { "X-CSRFToken": csrftoken }
        });

        const result = await res.json();

        if (result.status === "success") {
          showMessage(messageId, result.message || "Berhasil!", "success");
          form.reset();

          // Login → reload halaman
          if (formId === "loginSeekerForm" || formId === "loginCompanyForm") {
            window.location.reload();
          } 
          // Register → tampil modal verifikasi
          else if (formId === "registerSeekerForm" || formId === "registerCompanyForm") {
            if (modalClose) modalClose.style.display = "none";
            if (modalOpen) modalOpen.style.display = "flex";
          }
        }

      } catch(err) {
        console.error(err);
        showMessage(messageId, ["Kesalahan server"], "error");
      }
    });
  }

  // ================= BIND FORMS =================
  handleForm("registerSeekerForm", "registerSeekerMessage", modals.registerSeeker, modals.verifySeeker);
  handleForm("registerCompanyForm", "registerCompanyMessage", modals.registerCompany, modals.verifyCompany);
  handleForm("loginSeekerForm", "loginSeekerMessage", modals.loginSeeker);
  handleForm("loginCompanyForm", "loginCompanyMessage", modals.loginCompany);
  handleForm("resetPasswordForm", "resetPasswordMessage", modals.resetRequest);
  handleForm("resetPasswordConfirmForm", "resetPasswordConfirmMessage", modals.resetConfirm);

  // ================= AUTO OPEN RESET CONFIRM =================
  if (window.location.href.includes("/accounts/reset/")) {
    if (modals.resetConfirm) modals.resetConfirm.style.display = "flex";
  }

  // ================= DROPDOWN PROFILE =================
  const btn = document.querySelector('.profile-btn');
  const menu = document.querySelector('.profile-menu');
  if (btn && menu) {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      menu.classList.toggle('show');
    });
    document.addEventListener('click', e => {
      if (!menu.contains(e.target) && !btn.contains(e.target)) {
        menu.classList.remove('show');
      }
    });
  }

});

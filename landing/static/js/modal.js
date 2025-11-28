document.addEventListener("DOMContentLoaded", function() {

  const loginModal = document.getElementById("loginModal");
  const registerModal = document.getElementById("registerModal");
  const verifyModal = document.getElementById("verifyModal");

  const btnKerja = document.getElementById("openLoginKerja");
  const btnStaff = document.getElementById("openLoginStaff");
  const btnSignIn = document.getElementById("openLoginModal");

  // Check login state from template
  const isLoggedIn = window.isLoggedIn === true;

  // =============================
  // ====== Redirect logic =======
  // =============================
  function openLoginOrRedirect(type) {
    if (isLoggedIn) {
      window.location.href = type === "kerja" ? "/homepage_kerja/" : "/homepage_staff/";
    } else {
      openLoginModal(type);
    }
  }

  function openLoginModal(type = "kerja") {
    loginModal.dataset.type = type;
    loginModal.style.display = "flex";
  }

  if (btnKerja) {
    btnKerja.addEventListener("click", (e) => {
      e.preventDefault();
      openLoginOrRedirect("kerja");
    });
  }

  if (btnStaff) {
    btnStaff.addEventListener("click", (e) => {
      e.preventDefault();
      openLoginOrRedirect("staff");
    });
  }

  if (btnSignIn) {
    btnSignIn.addEventListener("click", (e) => {
      e.preventDefault();
      openLoginModal("kerja");
    });
  }

  // Switch modal links
  const openLoginLink = document.getElementById("openLoginLink");
  const openRegisterLink = document.getElementById("openRegisterLink");

  if (openLoginLink) {
    openLoginLink.addEventListener("click", (e) => {
      e.preventDefault();
      registerModal.style.display = "none";
      loginModal.style.display = "flex";
    });
  }

  if (openRegisterLink) {
    openRegisterLink.addEventListener("click", (e) => {
      e.preventDefault();
      loginModal.style.display = "none";
      registerModal.style.display = "flex";
    });
  }

  document.querySelectorAll(".close").forEach(btn => {
    btn.addEventListener("click", () => {
      const target = document.getElementById(btn.dataset.close);
      if (target) target.style.display = "none";
    });
  });

  window.addEventListener("click", (e) => {
    if (e.target.classList.contains("modal")) {
      e.target.style.display = "none";
    }
  });

  function showMessage(elementId, text, kind = "error") {
    const el = document.getElementById(elementId);
    if (!el) return alert(text);
    el.className = "message-box " + kind;
    el.textContent = text;

    if (kind === "success") {
      setTimeout(() => { el.textContent = ""; el.className = "message-box"; }, 3000);
    }
  }

  // =======================
  // ===== REGISTER ========
  // =======================
  const registerForm = document.getElementById("registerForm");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const pwd = document.getElementById("password").value;
      const pwd2 = document.getElementById("confirm_password").value;

      if (pwd !== pwd2) {
        return showMessage("registerMessage", "Password tidak sama.", "error");
      }

      const formData = new FormData(registerForm);

      try {
        const response = await fetch(registerForm.action, { method: "POST", body: formData });
        const result = await response.json();

        if (result.status === "success") {
          registerModal.style.display = "none";
          verifyModal.style.display = "flex";
        } else {
          showMessage("registerMessage", result.message, "error");
        }
      } catch {
        showMessage("registerMessage", "Terjadi kesalahan server.", "error");
      }
    });
  }

  // =======================
  // ====== LOGIN ==========
  // =======================
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(loginForm);
      const userType = loginModal.dataset.type;

      formData.append("user_type", userType);

      try {
        const response = await fetch(loginForm.action, { method: "POST", body: formData });
        const result = await response.json();

        if (result.status === "success") {
          window.location.href = userType === "kerja" ? "/homepage_kerja/" : "/homepage_staff/";
        } else {
          showMessage("loginMessage", result.message, "error");
        }
      } catch {
        showMessage("loginMessage", "Kesalahan server saat login.", "error");
      }
    });
  }

  const closeVerifyModal = document.getElementById("closeVerifyModal");
  if (closeVerifyModal) {
    closeVerifyModal.addEventListener("click", () => {
      verifyModal.style.display = "none";
    });
  }
});

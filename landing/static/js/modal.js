document.addEventListener("DOMContentLoaded", function() {
  // ======== Ambil elemen modal ========
  const loginModal = document.getElementById("loginModal");
  const registerModal = document.getElementById("registerModal");
  const verifyModal = document.getElementById("verifyModal");

  // ======== Ambil tombol dari index.html ========
  const btnKerja = document.getElementById("openLoginKerja");
  const btnStaff = document.getElementById("openLoginStaff");
  const btnSignIn = document.getElementById("openLoginModal");

  // ======== Fungsi buka modal login ========
  function openLoginModal(type = "kerja") {
    loginModal.dataset.type = type;
    loginModal.style.display = "flex";
  }

  // ======== Event tombol ========
  if (btnKerja) {
    btnKerja.addEventListener("click", (e) => {
      e.preventDefault();
      openLoginModal("kerja");
    });
  }

  if (btnStaff) {
    btnStaff.addEventListener("click", (e) => {
      e.preventDefault();
      openLoginModal("staff");
    });
  }

  if (btnSignIn) {
    btnSignIn.addEventListener("click", (e) => {
      e.preventDefault();
      openLoginModal("kerja");
    });
  }

  // ======== Link antar modal ========
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

  // ======== Tutup modal ========
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

  // =============================
  // ======== REGISTER FORM ======
  // =============================
  const registerForm = document.getElementById("registerForm");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(registerForm);

      try {
        const response = await fetch(registerForm.action, {
          method: "POST",
          body: formData,
        });
        const result = await response.json();

        if (result.status === "success") {
          // Tutup modal register dan tampilkan verifikasi
          registerModal.style.display = "none";
          verifyModal.style.display = "flex";
        } else {
          alert(result.message || "Gagal mendaftar. Silakan coba lagi.");
        }
      } catch (error) {
        console.error("Error saat register:", error);
        alert("Terjadi kesalahan saat mendaftar.");
      }
    });
  }

  // =============================
  // ========= LOGIN FORM ========
  // =============================
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(loginForm);
      const userType = loginModal.dataset.type || "kerja"; // default kerja
      formData.append("user_type", userType);

      try {
        const response = await fetch(loginForm.action, {
          method: "POST",
          body: formData,
        });
        const result = await response.json();

        if (result.status === "success") {
          // Redirect ke halaman sesuai tipe login
          if (userType === "kerja") {
            window.location.href = "/homepage_kerja/";
          } else if (userType === "staff") {
            window.location.href = "/homepage_staff/";
          } else {
            window.location.href = "/";
          }
        } else {
          alert(result.message || "Login gagal. Periksa email & password.");
        }
      } catch (error) {
        console.error("Error saat login:", error);
        alert("Terjadi kesalahan saat login.");
      }
    });
  }

  // Tutup modal verifikasi
  const closeVerifyModal = document.getElementById("closeVerifyModal");
  if (closeVerifyModal) {
    closeVerifyModal.addEventListener("click", () => {
      verifyModal.style.display = "none";
    });
  }
});

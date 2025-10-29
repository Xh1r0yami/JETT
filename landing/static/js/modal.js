document.addEventListener("DOMContentLoaded", function() {
  const loginModal = document.getElementById("loginModal");
  const registerModal = document.getElementById("registerModal");
  const verifyModal = document.getElementById("verifyModal");

  document.getElementById("openLoginModal").onclick = () => loginModal.style.display = "flex";
  document.getElementById("openLoginLink").onclick = (e) => {
    e.preventDefault();
    registerModal.style.display = "none";
    loginModal.style.display = "flex";
  };
  document.getElementById("openRegisterLink").onclick = (e) => {
    e.preventDefault();
    loginModal.style.display = "none";
    registerModal.style.display = "flex";
  };
  document.querySelectorAll(".close").forEach(btn => {
    btn.onclick = () => document.getElementById(btn.dataset.close).style.display = "none";
  });

  // ===== Register Form =====
  document.getElementById("registerForm").onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch(e.target.action, { method: "POST", body: formData });
    const result = await response.json();

    if (result.status === "success") {
      registerModal.style.display = "none";
      verifyModal.style.display = "flex";
    } else {
      alert(result.message);
    }
  };

  // ===== Login Form =====
  document.getElementById("loginForm").onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch(e.target.action, { method: "POST", body: formData });
    const result = await response.json();

    if (result.status === "success") {
      window.location.href = "/homepage/";
    } else {
      alert(result.message);
    }
  };
});

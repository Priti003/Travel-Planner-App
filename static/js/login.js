const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

// Toggle between sign-in and sign-up forms
sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

// Handle sign-up form submission
const signUpForm = document.querySelector(".sign-up-form");
signUpForm.addEventListener("submit", (e) => {
  // Form will be submitted normally
  // No need to prevent default behavior
  // The server will handle the form submission
});

// Handle sign-in form submission
const signInForm = document.querySelector(".sign-in-form");
signInForm.addEventListener("submit", (e) => {
  e.preventDefault(); // Prevent default form submission

  const email = signInForm.querySelector("input[name='email']").value;
  const password = signInForm.querySelector("input[name='password']").value;

  // Create a FormData object to send data
  const formData = new FormData();
  formData.append("email", email);
  formData.append("password", password);

  fetch("/login", {
    method: "POST",
    body: formData,
    credentials: "same-origin"
  })
  .then(response => {
    if (response.redirected) {
      window.location.href = response.url;
    } else {
      return response.text();
    }
  })
  .then(text => {
    if (text.includes("Invalid email or password")) {
      alert("Invalid email or password. Please try again.");
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
});

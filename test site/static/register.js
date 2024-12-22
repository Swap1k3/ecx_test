document.getElementById("registerForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // Останавливаем отправку формы
  
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const errorMessage = document.getElementById("errorMessage");
    const successMessage = document.getElementById("successMessage");
  
    errorMessage.textContent = "";
    successMessage.textContent = "";
  
    // Валидация пароля
    if (password !== confirmPassword) {
      errorMessage.textContent = "Пароли не совпадают!";
      return;
    }
  
    if (password.length < 8) {
      errorMessage.textContent = "Пароль должен быть не менее 8 символов.";
      return;
    }
  
    // Отправка данных на сервер
    try {
      const response = await fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });
  
      const result = await response.json();
  
      if (response.ok) {
        window.location.href = result.redirect;
      } else {
        errorMessage.textContent = result.message;
      }
    } catch (error) {
      errorMessage.textContent = "Произошла ошибка при отправке данных.";
    }
  });
  
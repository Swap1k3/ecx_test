document.getElementById("fpassForm").addEventListener("submit", async function (event) {
  event.preventDefault(); // Останавливаем отправку формы

  const email = document.getElementById("email").value;
  const errorMessage = document.getElementById("errorMessage");

  errorMessage.textContent = ""; // Сбрасываем сообщение об ошибке

  // Отправка данных на сервер
  try {
      const response = await fetch("/fpass", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email }),
      });

      const result = await response.json();

      if (response.ok) {
          window.location.href = result.redirect; // Перенаправляем на главную страницу
      } else {
          errorMessage.textContent = result.message; // Показываем сообщение об ошибке
      }
  } catch (error) {
      errorMessage.textContent = "Произошла ошибка при отправке данных.";
  }
});

document.getElementById('delete-account-form').addEventListener('submit', function(event) {
    const confirmation = confirm("Вы уверены, что хотите удалить аккаунт? Это действие необратимо!");
    if (!confirmation) {
        event.preventDefault(); // Отменяет отправку формы
    }
    if (response.ok) {
        window.location.href = result.redirect
    }

});




from flask import (
    Flask,
    session,
    redirect,
    url_for,
    request,
    render_template,
    flash,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import re


app = Flask(__name__)

# Конфигурация
app.secret_key = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        # Проверяем, существует ли пользователь
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"] = (
                user.id
            )  # Сохраняем идентификатор пользователя в сессии
            session["username"] = user.username  # Сохраняем имя пользователя
            session["email"] = user.email

            return jsonify(
                {"status": "success", "message": "Вход успешен!", "redirect": "/main"}
            )

        if not user:
            return (
                jsonify({"status": "error", "message": "Пользователь не существует!"}),
                400,
            )

        # Проверяем пароль
        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({"status": "error", "message": "Неверный пароль!"}), 400

    return render_template("login.html")


# Маршрут для регистрации
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        data = request.get_json()  # Получаем JSON-данные
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Серверная валидация
        if not username or not email or not password:
            return jsonify({"status": "error", "message": "Все поля обязательны"}), 400
        if len(password) < 8:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Пароль должен быть не менее 8 символов",
                    }
                ),
                400,
            )
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            return jsonify({"status": "error", "message": "Некорректный email"}), 400

        # Проверка уникальности
        if User.query.filter_by(username=username).first():
            return (
                jsonify({"status": "error", "message": "Имя пользователя уже занято"}),
                400,
            )
        if User.query.filter_by(email=email).first():
            return (
                jsonify({"status": "error", "message": "Email уже зарегистрирован"}),
                400,
            )

        # Хэширование пароля и сохранение в базе данных
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(
            {"status": "success", "message": "Вход успешен!", "redirect": "/main"}
        )
    return render_template("register.html")


@app.route("/fpass", methods=["POST", "GET"])
def fpass():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")

        # Проверяем, существует ли пользователь
        user = User.query.filter_by(email=email).first()
        if not user:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Пользователя с таким email не существует!",
                    }
                ),
                400,
            )

        # Успешный вход
        return jsonify(
            {"status": "success", "message": "отправили код!", "redirect": "/login"}
        )

    return render_template("fpass.html")


@app.route("/main")
def main():
    if "user_id" not in session:  # Проверяем, авторизован ли пользователь
        return redirect(url_for("login_user"))  # Перенаправляем на страницу логина

    return render_template(
        "main.html", username=session["username"]
    )  # Передаём имя пользователя в шаблон


@app.route("/logout")
def logout():
    session.clear()  # Удаляем все данные из сессии
    return redirect(url_for("login_user"))  # Перенаправляем на страницу логина


@app.route("/profile")
def profile():
    if "user_id" not in session:  # Проверяем, авторизован ли пользователь
        return redirect(url_for("login_user"))  # Перенаправляем на страницу логина

    return render_template(
        "profile.html",
        username=session["username"],
        email=session["email"],
    )  # Передаём имя пользователя в шаблон


@app.route("/delete_account", methods=["POST"])
def delete_account():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            session.pop("user_id", None)  # Удаляем пользователя из сессии
            return redirect(url_for("register"))  # Перенаправляем на главную страницу
    return "вы удалили аккакунт!", 404


@app.route("/exc1")
def exc1():
    return render_template("exc1.html")


@app.route("/exc2")
def exc2():
    return render_template("exc2.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Создать таблицу, если она отсутствует
    app.run(debug=True)

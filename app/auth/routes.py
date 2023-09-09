from app.auth import bp
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.models import Usuario
from app.extensions import db


@bp.route("/", methods=["POST", "GET"])
@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    else:
        nome = request.form.get("nome")
        senha = request.form.get("senha")
        usuario = Usuario.query.filter_by(nome=nome).first()
        if not usuario or not check_password_hash(usuario.senha, senha):
            flash('Nome ou senha incorretos!!')
            return redirect(url_for("auth.login"))
        login_user(usuario)
        return redirect(url_for("painel.criar"))


@bp.route("/registro", methods=["POST", "GET"])
def registro():
    if request.method == "GET":
        return render_template("registro.html")
    else:
        nome = request.form.get("nome")
        senha = request.form.get("senha")

        usuario = Usuario.query.filter_by(nome=nome).first()

        if usuario:
            flash('Nome já registrado')
            return redirect(url_for("auth.registro"))

        novo_usuario = Usuario(
            nome=nome, senha=generate_password_hash(senha, method="sha256")
        )

        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for("auth.login"))
    
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


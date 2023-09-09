from flask import request, redirect, render_template, url_for
from app.painel import bp
from app.models import Tarefa
from app.extensions import db
from flask_login import login_required, current_user


@bp.route("/painel", methods=["POST", "GET"])
@login_required
def criar():
    if request.method == "GET":
        tarefas = Tarefa.query.filter_by(usuario_id=current_user.id).all()
        return render_template("painel/painel.html", tarefas=tarefas)
    else:
        conteudo_tarefa = request.form["conteudo"]
        nova_tarefa = Tarefa(conteudo=conteudo_tarefa, usuario_id=current_user.id)
        try:
            db.session.add(nova_tarefa)
            db.session.commit()
            return redirect(url_for("painel.criar"))
        except:
            return "Houve um problema em adicionar tarefa!"


@bp.route("/apagar/<int:id>")
@login_required
def apagar(id):
    tarefa_para_apagar = Tarefa.query.get_or_404(id)
    try:
        db.session.delete(tarefa_para_apagar)
        db.session.commit()
        return redirect(url_for("painel.criar"))
    except:
        return "Houve um problema em apagar a tarefa"


@bp.route("/atualizar/<int:id>", methods=["GET", "POST"])
@login_required
def atualizar(id):
    tarefa_para_atualizar = Tarefa.query.get_or_404(id)
    if request.method == "GET":
        return render_template("painel/atualizar.html", tarefa=tarefa_para_atualizar)
    else:
        tarefa_para_atualizar.conteudo = request.form["conteudo"]

        try:
            db.session.commit()
            return redirect(url_for("painel.criar"))
        except:
            return "Erro ao atualizar a tarefa"

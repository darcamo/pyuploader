# -*- coding: utf-8 -*-

from app import app, db, models
from flask import render_template, flash, redirect, url_for, request, \
    make_response, jsonify, g, abort, send_from_directory, send_file
from app.views.forms import UploadNewFileForm, LoginForm, TrocarSenhaForm
from flask_login import login_user, logout_user, current_user, login_required
from flask.ext.classy import FlaskView, route
from app import lm
from app.models import User
from werkzeug import secure_filename
import os
from datetime import datetime


@app.route('/', methods=['GET'])
@login_required
def index():
    u = current_user
    # trabalhos_entregues = db.session.query(models.Trabalhos, models.TrabalhoEntregue).outerjoin(models.TrabalhoEntregue).all()

    trabalhos_entregues = db.session.query(models.Trabalhos, models.TrabalhoEntregue).join(models.TrabalhoEntregue).filter(models.TrabalhoEntregue.user==u).all()
    ids_dos_trabalhos_entregues = [i[0].id for i in trabalhos_entregues]

    todos_os_trabalhos = db.session.query(models.Trabalhos).all()

    # Lista com todos os trabalhos. Primeiro adicionamos os trabalhos que
    # ainda não foram entregues
    trabalhos = []
    for i in todos_os_trabalhos:
        if i.id not in ids_dos_trabalhos_entregues:
            trabalhos.append((i, None))

    # Agora adicionamos os trabalhos que já foram entregues
    trabalhos.extend(trabalhos_entregues)

    # trabalhos_nao_entregues = db.session.query(models.Trabalhos).\
    # join(models.TrabalhoEntregue).filter(models.TrabalhoEntregue.user!=u)\
    # .all()

    if u.is_admin:
        trabalhos_entregues_dos_alunos \
            = db.session.query(models.TrabalhoEntregue, models.Trabalhos)\
                        .filter(models.TrabalhoEntregue.user_id!=u.id)\
                        .join(models.Trabalhos)\
                        .all()

        return render_template(
            "main.html",
            trabalhos=trabalhos,
            trabalhos_entregues_dos_alunos=trabalhos_entregues_dos_alunos)
    else:
        return render_template("main.html",
                               trabalhos=trabalhos,
                               trabalhos_entregues_dos_alunos=None)


@app.errorhandler(404)
def page_not_found(_):
    # Note the 404 after the render_template() call. This tells Flask that
    # the status code of that page should be 404 which means not found. By
    # default 200 is assumed which translates to: all went well.
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(_):
    # The error might have left the database in an invalid state. Let's
    # rollback everything since the last commit to fix that possibility.
    db.session.rollback()
    return render_template('500.html'), 500


@lm.user_loader
def load_user(user_id):
    """
    Function that loads a user from the database. This function will be used
    by Flask-Login

    Parameters
    ----------
    user_id : str
        A unicode string with the user ID.

    Returns
    -------
    User
        The user object.
    """
    return User.query.get(int(user_id))


# The g global is set up by Flask as a place to store and share data during
# the life of a request. We will store the logged in user in it, as shown
# below. Any functions decorated with before_request will run before the
# view function each time a request is received.
# @app.before_request
# def before_request():
#     g.user = current_user


class UploadDeTrabalhosView(FlaskView):
    @route('/download/<int:trabalho_id>/<path:filename>/<int:user_id>')
    @route('/download/<int:trabalho_id>/<path:filename>')
    @login_required
    def download_uploaded_file(self, filename, trabalho_id, user_id=None):
        if user_id is not None:
            user_obj = db.session.query(models.User).get(user_id)
        else:
            user_obj = current_user
            
        folder = self._get_user_task_folder(trabalho_id, user_obj)
        folder = folder.split("/", maxsplit=1)[1]

        try:
            resp = send_file(os.path.join(folder, filename),
                             as_attachment=True)
        except FileNotFoundError:
            resp = abort(404)
        return resp

    @staticmethod
    @login_required
    def _get_user_task_folder(trabalho_id, user_obj=None):
        if user_obj is None:
            user_obj = current_user

        # xxxxxxxxxx Get full path to save the uploaded file xxxxxxxxxx
        # Folder at the server where the tasks of all users will be
        # uploaded for this course
        course_folder = os.path.expanduser(app.config.get('COURSE_UPLOAD_FOLDER'))
        # User folder inside the course folder
        user_folder = "{0}_({1})".format(secure_filename(user_obj.name),
                                         secure_filename(user_obj.username))

        # Assume a task folder corresponding simple to the trabalho_id,
        # let's get the full server folder to save the file for the
        # current task (with trabalho_id) for the current user.
        full_task_folder_name = os.path.join(course_folder,
                                             user_folder,
                                             str(trabalho_id))
        return full_task_folder_name

    @route("/<int:trabalho_id>/novo_trabalho", methods=['GET', 'POST'])
    @login_required
    def upload_trabalho(self, trabalho_id=None):
        """Função para tratar o POST request para submeter um novo trabalho."""
        form = UploadNewFileForm(trabalho_id=trabalho_id)

        choices = db.session.query(models.Trabalhos.id, models.Trabalhos.name).all()
        form.trabalho.choices = choices

        if form.validate_on_submit():
            # Get the folder where to save the file for the task with
            # trabalho_id for the current user.
            full_task_folder_name = self._get_user_task_folder(trabalho_id)

            # Full name of the file at the server
            full_filename = os.path.join(full_task_folder_name,
                                         form.arquivo.data.filename)
            # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

            # TODO: Veja se o arquivo já existe. Se existir, adicione como
            # nova versão.
            # Save the uploaded file to the destination

            try:
                form.arquivo.data.save(full_filename)
            except OSError:
                # If the parent folders don't exist a FileNotFoundError
                # (inherits from OSError) exception is raised. In that case
                # we create the parent folders and then we try to save the
                # file again
                os.makedirs(full_task_folder_name)
                form.arquivo.data.save(full_filename)


            # xxxxx Check if there is already an entry in database xxxxxxxx
            # Check if there is an entry for this specific user_id and
            # trabalho_oi.
            trabalho_entregue = db.session.query(models.TrabalhoEntregue)\
                                          .filter_by(user_id=current_user.id,
                                                     trabalho_id=trabalho_id)\
                                          .first()

            if trabalho_entregue is None:
                # There is no entry. Let's create a new one
                t = models.TrabalhoEntregue(trabalho_id=trabalho_id,
                                            user_id=current_user.id,
                                            path=full_filename,
                                            entrega=datetime.today())
                db.session.add(t)
                db.session.commit()
            else:
                old_path = trabalho_entregue.path
                # Remove previous file
                try:
                    os.remove(os.path.join(full_task_folder_name, old_path))
                except OSError:
                    pass
                # Change path to point to the new file
                trabalho_entregue.path = form.arquivo.data.filename
                db.session.add(trabalho_entregue)
                db.session.commit()
                # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


            # Código para adicionar um trabalho
            # ... ... ...
            # TODO: Finish implementation

            flash("Trabalho cadastrado com sucesso")

            # Retorna para a função main
            return redirect(
                url_for('index'))
        else:
            return render_template("upload_novo_trabalho.html",
                                   form=form,
                                   trabalho_id=trabalho_id)

UploadDeTrabalhosView.register(app)


class LoginView(FlaskView):
    # @route('/registrar', methods=['GET', 'POST'])
    # def registrar_novo_usuario(self):
    #     form = NovoUsuarioForm()
    #     if form.validate_on_submit():
    #         # Handle POST method

    #         # Let's get the user provided password and hash it first to
    #         # store in the database. Note that the werkzeug.security module
    #         # provide nice functions to generate the hash and to check if
    #         # the password match. See this http://flask.pocoo.org/snippets/54/
    #         hashed_password = generate_password_hash(form.password.data)
    #         email = form.email.data.strip()
    #         if not email:
    #             # If not provided, wtforms will set email to an empty
    #             # string.  In that case lets set it to None so that we
    #             # don't have problems with the unique constraint for the
    #             # email column in the database
    #             email = None

    #         user = User(username=form.user.data, password=hashed_password,
    #                     email=email)
    #         db.session.add(user)
    #         db.session.commit()
    #         flash("Usuário '{0}' cadastrado com sucesso".format(user.username))

    #         return redirect(url_for('LoginView:logar'))

    #     # GET method
    #     return render_template("login/registrar_usuario.html", form=form)

    @route('/', methods=['GET', 'POST'])
    def logar(self):

        if current_user.is_authenticated:
            flash('Você já está logado como "{0}"'.format(current_user.username),
                  category='info')
            return redirect(request.args.get('next') or url_for('index'))

        form = LoginForm()
        if form.validate_on_submit():
            # The form will load the user object from the database (it
            # needs it to validate the password. After that it will save
            # the user in the 'user' attribute that we can get here.
            user = form.user
            # This is the function provided by flask-login to actually
            # login-in the user.
            login_user(user, remember=True)
            if user.is_admin:
                flash('Logado como "{0}" ({1} - ADMIN)'.format(user.username, user.name))
            else:
                flash('Logado como "{0}" ({1})'.format(user.username, user.name))

            # To understand the concept of next page, let's look at a
            # simple example. Suppose you want to create a new "to do" item
            # but the new "to do" view requires authentication. If you are
            # not authenticated, Flask-Login will redirect you to the login
            # page for authentication. Flask-Login will store the original
            # request URL in the next page request attribute, and after a
            # successful login, it will redirect you to the requested page.
            return redirect(request.args.get('next') or url_for('index'))
        return render_template('logar_usuario.html',
                               form=form)

    @route('/trocarsenha', methods=['GET', 'POST'])
    @login_required
    def trocar_senha(self, ):
        # return "Trocar Senha: Falta implementar"
        form = TrocarSenhaForm()
        if form.validate_on_submit():
            current_user.set_password(form.new_password.data)
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template("redefinir_senha.html", form=form)


    @route('/deslogar', methods=['GET', 'POST'])
    # noinspection PyMethodMayBeStatic
    def deslogar(self):
        logout_user()
        # remove the username from the session if it's there
        # username = session['user']
        # session.pop('user', None)

        flash("Deslogado com sucesso")
        return redirect(url_for('index'))


LoginView.register(app)

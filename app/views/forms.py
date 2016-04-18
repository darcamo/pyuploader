

"""
Module defining forms, which will handle validation for us.

Web forms are represented in Flask-WTF as classes, subclassed from base
class Form. A form subclass simply defines the fields of the form as class
variables.
"""

from flask_login import current_user
from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Optional, Length, \
    ValidationError, EqualTo
from wtforms import StringField, IntegerField, RadioField, \
    SelectField, PasswordField, SubmitField, FloatField, TextAreaField
from app.models import User, Trabalhos
from app import db


class UploadNewFileForm(Form):
    """Form para upload de novos trabalhos (listas e trabalhos práticos).
    """
    arquivo = FileField(
        'Nome do arquivo',
        validators=[
            FileRequired(),
            FileAllowed(['cpp', 'h', 'c', 'py', 'zip', 'rar', 'tar', 'tag.gz'],
                        ('Apenas código fonte (.cpp/.c/.h) ou arquivos zip/rar '
                         'contendo código fonte são aceitos'))])

    trabalho = SelectField('Tarefa',
                           choices=[('nada', 'nada')],
                           #choices=db.session.query(Trabalhos.id, Trabalhos.name).all(),
                           # default='A',
                           validators=[Optional()])
    comentarios = TextAreaField("Comentários (até 1000 caracteres)",
                                validators=[Optional(), Length(max=1000)])
    submit = SubmitField("Enviar")

    def __init__(self, trabalho_id, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.trabalho.data = str(trabalho_id)

    def validate_arquivo(self, filefield):
        if not filefield.has_file():
            raise ValidationError('É necessário fornecer um arquivo')

        try:
            # Se for arquivo zip/rar veja se tem apenas código fonte nele
            pass
        except Exception as e:
            raise ValidationError(e.args[0])


class LoginForm(Form):
    username = StringField('Usuário', validators=[DataRequired(),
                           Length(min=4, max=64)])
    password = PasswordField('Senha', validators=[DataRequired(),
                                                  Length(min=6, max=60)],
                             description='Precisa ter ao menos 6 caracteres')
    submit = SubmitField("Logar")

    # remember_me = BooleanField('remember_me', default=False)

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        # Store the User database object
        self.user = None

    # noinspection PyMethodOverriding
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        # Here we pull the user from the database in the general validation
        # step, validate username and password by hand and attach errors to
        # the individual fields if something goes wrong.
        user = User.query.filter_by(
            username=self.username.data).first()
        if user is None:
            self.username.errors.append('Usuário não cadastrado')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Senha inválida')
            return False

        # We also keep the user object around so that we can use it in a view
        self.user = user
        return True


class TrocarSenhaForm(Form):
    old_password = PasswordField(
        'Senha antiga',
        validators=[DataRequired(),
                    Length(min=6, max=60)],
        description='Precisa ter ao menos 6 caracteres')
    new_password = PasswordField(
        "Senha nova",
        validators=[DataRequired(),
                    Length(min=6, max=60),
                    EqualTo('new_password2',
                            message='Senha e confirmação não batem')],
        description='Precisa ter ao menos 6 caracteres')
    new_password2 = PasswordField("Confirmação de Senha",
                                  description='Repita a senha nova')
    submit = SubmitField("Enviar")

    def validate_old_password(self, filefield):
        if not current_user.check_password(filefield.data):
            raise ValidationError('Senha incorreta')

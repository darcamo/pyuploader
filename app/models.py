# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import UniqueConstraint, CheckConstraint
from werkzeug.security import generate_password_hash, check_password_hash

from . import app, db


# noinspection PyMethodMayBeStatic
class User(db.Model):
    """
    User model. Integrates with Flask-Login.

    id: The ID of the user.
    username: The username of the user (can contain any characters)
    name: The full name of the user
    password: Encrypted password
    superuser: Boolean to tell if the user is a superuser
    active: Boolean to tell if the user is active (ability to login and operate on the app)
    register_date: The date the user registered
    last_login: The date the user last logged in the app
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(54))
    superuser = db.Column(db.Boolean())
    active = db.Column(db.Boolean())
    register_date = db.Column(db.DateTime())
    last_login = db.Column(db.DateTime())

    def __init__(self, username, name, password, superuser=False, active=True,
                 register_date=None, last_login=None):
        """
        :param username: The username of the user.
        :param name: The full name of the user
        :param password: The raw password to be encrypted and stored.
        :param active: Set if the user is active or not (restrains from logging for example)
        :param superuser: Set if the user is a superuser
        :param register_date: Set the date of registration (defaults to "now")
        :param last_login:
        """
        now = datetime.utcnow()
        self.username = username
        self.name = name
        self.set_password(password)
        self.superuser = superuser
        self.active = active
        if register_date:
            self.register_date = register_date
        else:
            self.register_date = now
        if last_login:
            self.last_login = last_login
        else:
            self.last_login = now

    def save(self):
        """
        Save method. Allows to easily save a single object.
        Also logs the errors in case of Exception.
        Customise this method to suit your needs.
        :return: True if the operation succeed, False otherwise.
        """
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.exception(
                "Something went wrong while saving a user {}".format(e))
            db.session.rollback()
            return False
        return True

    def delete(self):
        """
        Delete method allows to easily delete a single object.
        Also logs the errors in case of Exception.
        Customise this method to suit your needs.
        :return: True if the operation succeed, False otherwise.
        """
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            app.logger.exception(
                "Something went wrong while deleting a user {}".format(e))
            db.session.rollback()
            return False
        return True

    @property
    def is_admin(self):
        return self.superuser

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return "User(id={0}, username={1}, name={2}, superuser={3})".format(
            self.id, self.username, self.name, self.superuser)

    def __str__(self):
        return self.username


class Trabalhos(db.Model):
    """Modelo para as listas de exercícios, aulas práticas e trabalhos.
    """
    id = db.Column(db.Integer, primary_key=True)
    # Exemplos de nomes: "Prática 3", "Lista 4", etc
    name = db.Column(db.String(100), unique=True)
    startdate = db.Column(db.DateTime(), nullable=False) # Data em que passei a lista/prática
    deadline = db.Column(db.DateTime(), nullable=False)  # Prazo de entrega
    # Pratica (não cobro), Lista (vale nota), Trabalho (vale nota e é mais complexo)
    type = db.Column(db.String(20), nullable=False)

    # Os alunos podem submeter novas versões.
    # Eu vou setar depois como falso para proibir novos uploads
    em_aberto = db.Column(db.Boolean, nullable=False, default=True)

    quem_entregou = db.relationship("User",
                                    secondary="trabalho_entregue",
                                    backref=db.backref("trabalhos")  #, lazy="dynamic"),
                                    )
                                    # lazy="dynamic")

                                    # cascade="all, delete-orphan"
                            # backref=backref(
                           # "user_keywords",
                            # collection_class=attribute_mapped_collection("special_key"),
                            # cascade="all, delete-orphan"
                            # )


    # Extra table arguments
    __table_args__ = (
        # Não permite adicionar mais de um apartamento com mesmo número na
        # mesma torre.
        CheckConstraint('deadline >= startdate', name='deadline_maior_igual_que_startdate'),
    )

    def __repr__(self):
        return "Trabalhos(id={0}, name={1}, type={2})".format(
            self.id, self.name, self.type)

    def __str__(self):
        return self.name


class TrabalhoEntregue(db.Model):
    __tablename__ = 'trabalho_entregue'

    id = db.Column(db.Integer, primary_key=True)
    trabalho_id = db.Column(db.Integer, db.ForeignKey('trabalhos.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Relative Path where the work was saved in the server
    path = db.Column(db.String, unique=True)
    entrega = db.Column(db.DateTime(), nullable=False)  # Prazo de entrega

    trabalho = db.relationship("Trabalhos")
    user = db.relationship("User")

        # Extra table arguments
    __table_args__ = (
        # Não permite adicionar mais de um apartamento com mesmo número na
        # mesma torre.
        UniqueConstraint('user_id', 'trabalho_id', name='user_id_trabalho_id_par_unico'),
    )

    def __repr__(self):
        return "TrabalhoEntregue(id={0}, user_id={1}, trabalho_id={2})".format(
            self.id, self.user_id, self.trabalho_id)

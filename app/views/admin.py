# -*- coding: utf-8 -*-

from flask import redirect, url_for, request
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
from flask_login import logout_user
from .. import models, app, db


class AdminModelView(ModelView):
    form_base_class = SecureForm  # Form with CSRF protection
    can_view_details = True
    create_modal = True
    edit_modal = True
    can_export = True

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        else:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('LoginView:logar', next=request.url))


class ReadOnlyAdminModelView(AdminModelView):
    can_create = False
    can_edit = False
    can_delete = False


class AdminTrabalhosModelView(AdminModelView):
    """
    Subclass of AdminModelView that will be used for the models.Trabalhos
    model. The only change is limiting the values for the 'type' field of
    models.Trabalhos to some specific values.
    """
    form_choices = {
        'type': [
            ('Pratica', 'Pratica'),
            ('Trabalho', 'Trabalho')]
    }


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('LoginView:logar'))
        elif not current_user.is_admin:
            logout_user()
            return redirect(url_for('LoginView:logar'))
        # Default index page. Customize this with the "admin/index.html"
        # template
        return super(MyAdminIndexView, self).index()


# Create the Admin instance
admin = Admin(app, name='Admin', index_view=MyAdminIndexView(),
              template_mode='bootstrap3')

# Register the admin views
admin.add_view(AdminModelView(models.User, db.session))
admin.add_view(AdminTrabalhosModelView(models.Trabalhos, db.session))
admin.add_view(ReadOnlyAdminModelView(models.TrabalhoEntregue, db.session))

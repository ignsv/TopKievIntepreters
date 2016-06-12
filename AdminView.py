from flask_admin.contrib import sqla
from flask_security import current_user, utils
from flask_admin import form
from jinja2 import Markup
from flask import url_for
from wtforms import validators, PasswordField


from model import file_path, User, Translator, Service

class ImageView(sqla.ModelView):

    def is_accessible(self):
        return current_user.has_role('superuser')

    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup('<img src="%s">' % url_for('static',
                                                 filename='img/'+form.thumbgen_filename(model.path)))

    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=file_path,
                                      thumbnail_size=(403, 403, True))
    }

class UserAdmin(sqla.ModelView):

    column_searchable_list = ('email','name')

    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Users unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('superuser')

    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        form_class.password2 = PasswordField('New Password')
        return form_class

    def on_model_change(self, form, model, is_created):

        if len(model.password2):
            model.password = utils.encrypt_password(model.password2)


class RoleAdmin(sqla.ModelView):

    def is_accessible(self):
        return current_user.has_role('superuser')

class TranslatorAdmin(sqla.ModelView):

    column_exclude_list = ('description','slug',)

    form_excluded_columns = ('slug',)

    def is_accessible(self):
        return current_user.has_role('superuser')

class ServiceAdmin(sqla.ModelView):

    column_exclude_list = ('description','slug',)

    form_excluded_columns = ('slug',)

    def is_accessible(self):
        return current_user.has_role('superuser')


class ReviewAdmin(sqla.ModelView):


    column_exclude_list = ('text',)

    column_sortable_list = ( ('user', 'user.email'), 'date', )

    column_searchable_list = ('date', User.email,'text')

    def is_accessible(self):
        return current_user.has_role('superuser')

    column_filters = ('user.email',
                      'user.name',
                      'text',
                      'date')

    form_args = dict(
                    text=dict(label='Rewiev Text', validators=[validators.required()])
                )

class PostTranslatorAdmin(sqla.ModelView):


    column_exclude_list = ('text',)

    column_sortable_list = ( ('user', 'user.email'), 'date', ('translator', 'translator.last_name'))

    column_searchable_list = ('date',Translator.last_name,User.email,'text')

    def is_accessible(self):
        return current_user.has_role('superuser')

    column_filters = ('user.email',
                      'user.name',
                      'translator.last_name',
                      'text',
                      'date')

    form_args = dict(
                    text=dict(label='Post Text', validators=[validators.required()])
                )

class LikeTranslatorAdmin(sqla.ModelView):



    column_sortable_list = ( ('user', 'user.email'), 'date', ('translator', 'translator.last_name'))

    column_searchable_list = ('date',Translator.last_name,User.email)

    def is_accessible(self):
        return current_user.has_role('superuser')

    column_filters = ('user.email',
                      'user.name',
                      'translator.last_name',
                      'date')


class PostServiceAdmin(sqla.ModelView):



    column_exclude_list = ('text',)

    column_sortable_list = ( ('user', 'user.email'), 'date', ('service', 'service.name'))

    column_searchable_list = ('date',Service.name,User.email,'text')

    def is_accessible(self):
        return current_user.has_role('superuser')

    column_filters = ('user.email',
                      'user.name',
                      'service.name',
                      'text',
                      'date')

    form_args = dict(
                    text=dict(label='Post Text', validators=[validators.required()])
                )

class LikeServiceAdmin(sqla.ModelView):


    column_sortable_list = ( ('user', 'user.email'), 'date', ('service', 'service.name'))

    column_searchable_list = ('date',Service.name,User.email)

    def is_accessible(self):
        return current_user.has_role('superuser')

    column_filters = ('user.email',
                      'user.name',
                      'service.name',
                      'date')
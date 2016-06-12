from flask_security.utils import encrypt_password
import flask_admin
from flask_admin import helpers as admin_helpers
from flask_security import SQLAlchemyUserDatastore, Security

from forms import ExtendedConfirmRegisterForm, CustomForgotPasswordForm, CustomSendConfirmationForm
from AdminView import *
from views import *


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, confirm_register_form=ExtendedConfirmRegisterForm, forgot_password_form=CustomForgotPasswordForm
                    ,send_confirmation_form=CustomSendConfirmationForm)
admin = flask_admin.Admin(
    app,
    'Admin Panel',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# Add Admin model views
admin.add_view(UserAdmin(User, db.session))
admin.add_view(TranslatorAdmin(Translator, db.session))
admin.add_view(ServiceAdmin(Service,db.session))
admin.add_view(ImageView(Image, db.session))
admin.add_view(ReviewAdmin(Review, db.session))
admin.add_view(PostTranslatorAdmin(PostTranslator,db.session))
admin.add_view(PostServiceAdmin(PostService,db.session))
admin.add_view(LikeTranslatorAdmin(LikeTranslator,db.session))
admin.add_view(LikeServiceAdmin(LikeService,db.session))


# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
    )


def build_sample_db():

    db.drop_all()
    db.create_all()

    with app.app_context():
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        blocked_user_role= Role(name='blocked')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.add(blocked_user_role)
        db.session.commit()

        test_user = user_datastore.create_user(
            name='Admin',
            email='admin',
            password=encrypt_password('admin'),
            roles=[user_role, super_user_role],
            confirmed_at=datetime.datetime.utcnow()
        )



        user_datastore.create_user(
                name='test_user',
                email='user@example.com',
                password=encrypt_password('123456'),
                roles=[user_role, ],
                confirmed_at=datetime.datetime.utcnow()
            )

        db.session.commit()
    return

if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)

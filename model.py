from flask_security import UserMixin, RoleMixin
import datetime
from sqlalchemy.ext.hybrid import hybrid_property
import re
from unicodedata import normalize
import os
import os.path as op
from flask_admin import form
from sqlalchemy.event import listens_for
from settings import db


# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'static')
file_path = op.join(file_path, 'img')
try:
    os.mkdir(file_path)
except OSError:
    pass


#Generates an slightly worse ASCII-only slug
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))

#define Models
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64), unique=True)
    path = db.Column(db.Unicode(128), unique=True)

    def __str__(self):
        return self.name


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


translator_images_table= db.Table(
    'translator_images',
    db.Column('translator_id', db.Integer(), db.ForeignKey('translator.id')),
    db.Column('image_id', db.Integer(), db.ForeignKey('image.id'))
)

service_image_table= db.Table(
    'service_image',
    db.Column('service_id', db.Integer(), db.ForeignKey('service.id')),
    db.Column('image_id', db.Integer(), db.ForeignKey('image.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email


# Create M2M table
translator_service_table = db.Table('translator_services', db.Model.metadata,
                           db.Column('translator_id', db.Integer, db.ForeignKey('translator.id')),
                           db.Column('service_id', db.Integer, db.ForeignKey('service.id'))
                           )

def slug_service(context):
    if 'name' in context.current_parameters:
        return slugify(context.current_parameters['name'])
    else:
        return ""

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type=db.Column(db.String(255))
    name=db.Column(db.String(255), unique=True, nullable=False)
    slug=db.Column(db.String(255), default=slug_service, onupdate=slug_service)
    description=db.Column(db.Text, nullable=False)
    images=db.relationship('Image', secondary=service_image_table)

    @hybrid_property
    def images_amount(self):
        return len(self.images)

    @hybrid_property
    def likes_amount(self):
        return len(self.likes_service)

    @hybrid_property
    def comments_amount(self):
        return len(self.posts_service)

    def __str__(self):
        return self.name

def slug_translator(context):
    if 'last_name' in context.current_parameters:
        return slugify(context.current_parameters['last_name'])
    else:
        return ""

class Translator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(255))
    price=db.Column(db.String(255))
    last_name=db.Column(db.String(255), unique=True, nullable=False)
    slug=db.Column(db.String(255), default=slug_translator, onupdate=slug_translator)
    age=db.Column(db.Integer)
    description=db.Column(db.Text, nullable=False)
    images=db.relationship('Image', secondary=translator_images_table)
    services = db.relationship('Service',backref='translators',secondary=translator_service_table)

    @hybrid_property
    def likes_amount(self):
        return len(self.likes_translator)

    @hybrid_property
    def comments_amount(self):
        return len(self.posts_translator)

    @hybrid_property
    def images_amount(self):
        return len(self.images)

    def __str__(self):
        return self.last_name


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    user = db.relationship(User, backref='review_user')

    #@hybrid_property
    #def review_amounts(self):


    def __unicode__(self):
        return str(self.id)




class PostTranslator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    translator_id = db.Column(db.Integer(), db.ForeignKey(Translator.id))
    user = db.relationship(User, backref='posts_translator')
    translator = db.relationship(Translator, backref='posts_translator')

    def __unicode__(self):
        return str(self.id)

class LikeTranslator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    translator_id = db.Column(db.Integer(), db.ForeignKey(Translator.id))
    user = db.relationship(User, backref='likes_translator')
    translator = db.relationship(Translator, backref='likes_translator')

    def __str__(self):
        return str(self.id)

class PostService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    service_id = db.Column(db.Integer(), db.ForeignKey(Service.id))
    user = db.relationship(User, backref='posts_service')
    service = db.relationship(Service, backref='posts_service')

    def __unicode__(self):
        return str(self.id)

class LikeService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    service_id = db.Column(db.Integer(), db.ForeignKey(Service.id))
    user = db.relationship(User, backref='likes_service')
    service = db.relationship(Service, backref='likes_service')

    def __str__(self):
        return str(self.id)

# Delete hooks for models, delete files if models are getting deleted
@listens_for(Image, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass




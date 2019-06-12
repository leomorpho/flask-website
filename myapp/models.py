from datetime import datetime
from flask import current_app
from time import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from hashlib import md5
from myapp import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Notice that the following is not declared as a model.
# Since it is an auxiliary table, it holds no data other than
# foreign keys of a many-to-many relationship.
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer,
                               db.ForeignKey('users.id')),
                     db.Column('followed_id', db.Integer,
                               db.ForeignKey('users.id'))
                     )


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic',), lazy='dynamic')

    # Assign default role by default, except if registering user
    # is an administrator
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email in current_app.config['ADMINS']:
                self.role = Role.query.filter_by(
                    permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User: {}>'.format(self.username)

#   #--------------------
#   # User setters
#   #--------------------
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

#   #--------------------
#   # Permissions
#   #--------------------
    def can(self, permissions):
        # Bitwise AND operation checks if the ressource can be
        # accessed by the user
        return self.role is not None and  \
            (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

#   #--------------------
#   # Followers
#   #--------------------
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # Look for items in association table that have the left side foreign
    # key set to the 'self' user, and the right side set to the 'user' argument
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        # Make a temporary joined table that hold all the users that have
        # followers and who have written posts. Then, filter it.
        # The query is issued on the Post class, because a list of posts
        # is returned.
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        # jwt encodes the token as a byte sequence, so convert it into
        # a string for convenience.
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    # Static methods can be invoked directly from the class, and do not
    # receive the class as an argument.
    @staticmethod
    def verify_reset_password_token(token):
        # If token is valid, payload is valid and value of reset_password
        # can be used to load the user.
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class AnonymousUser(AnonymousUserMixin):
    """
    An anonymous user class is added for consistency to check for
    permissions and roles. In this manner, all current_user can call
    current_user.can() and .is_admin() without needing to first check
    if the user is logged in.

    AnonymousUserMixin = Flask-Login class
    """

    def can(self, permissions):
        return False

    def is_admin(self):
        return False


login.anonymous_user = AnonymousUser


class Permission:
    BUY = 0x01
    WRITE_BLOGS = 0x02
    MODERATE_CONTENT = 0x04
    ADMINISTER = 0x80


class Role(db.Model):
    """
    Roles are an aggregate of permissions
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(280))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role: {}> \n'.format(self.name)

    @staticmethod
    def insert_roles():
        roles = {
            'Customer': (Permission.BUY, True),
            'Moderator': (Permission.BUY |
                          Permission.WRITE_BLOGS |
                          Permission.MODERATE_CONTENT, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Post(db.Model):
    """
    Posts table
    """
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post: {}>'.format(self.body)


class Product(db.Model):
    __tablename__ = "products"
    id = db .Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(140))
    image = db.Column(db.String(256))
    thumbnail = db.Column(db.String(256))
    # many-to-one: can be
    # boulangerie, patisserie, viennoiserie, salted, drinks, other
    # If more categories are added, the db products must be updated to
    # reflect the best descripting category
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    weight = db.Column(db.Integer)

    def __repr__(self):
        return '<Product: {} ({})> \n'.format(self.name, self.category)


class ProductCategory(db.Model):
    __tablename__ = "product_categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(140))
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<ProductCategory: {} ({})>'.format(
            self.name, self.description)

#     @staticmethod
#     def insert_product_categories():
#         categories = {
#             'Boulangerie': "Breads and similar",
#             'Patisserie': "Sweets, pastry and similar",
#             'Viennoiserie': "Croissants and similarr",
#             'Salted': "Sandwiches, soups and similar",
#         }
#         for r in categories:
#             cat = ProductCategory.query.filter_by(name=r).first()
#             if cat is None:
#                 cat = ProductCategory(name=r)
#             cat.description = categories[r][0]
#             db.session.add(cat)
#         db.session.commit()



# Implement the following:
# Tags for posts
# Groups for users

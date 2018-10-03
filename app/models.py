from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.exc import NoResultFound

from app import db, login_manager


class Voters(UserMixin, db.Model):
    """
    Create an Voter table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'voters'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)
    votes = db.relationship('Vote', backref='voter',
                            lazy='dynamic')

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Voters.query.get(int(user_id))


class Poll(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'poll'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    voters = db.relationship('Voters', backref='poll',
                             lazy='dynamic')
    votes = db.relationship('Vote', backref='poll',
                             lazy='dynamic')
    _electorate = db.Column('electorate', db.String(1024), nullable=False, default='[]', server_default='[]')

    @hybrid_property
    def electorate(self):
        if self._electorate:
            return json.loads(self._electorate)
        else:
            return []

    @electorate.setter
    def electorate(self, electorate):
        self._electorate = json.dumps(electorate)


    def __repr__(self):
        return '<Poll: {}>'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Voters', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class Vote(UserMixin, db.Model):
    """
    Create an Vote table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'vote'

    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    voter_id = db.Column(db.Integer, db.ForeignKey('voters.id'))
    vaoted_to = db.Column(db.String(255) , default = None)


    def get_or_create(self, model, **kwargs):
        """
        Usage:
        class Employee(Base):
            __tablename__ = 'employee'
            id = Column(Integer, primary_key=True)
            name = Column(String, unique=True)

        get_or_create(Employee, name='bob')
        """
        instance = get_instance(model, **kwargs)
        if instance is None:
            instance = create_instance(model, **kwargs)
        return instance

    def create_instance(model, **kwargs):
        """create instance"""
        try:
            instance = model(**kwargs)
            sess.add(instance)
            sess.flush()
        except Exception as msg:
            mtext = 'model:{}, args:{} => msg:{}'
            log.error(mtext.format(model, kwargs, msg))
            sess.rollback()
            raise (msg)
        return instance

    def get_instance(self, model, **kwargs):
        """Return first instance found."""
        try:
            return sess.query(model).filter_by(**kwargs).first()
        except NoResultFound:
            return

    def __repr__(self):
        return '<Vote: {}>'.format(self.id)
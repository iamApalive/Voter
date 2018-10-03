# app/home/views.py

from flask import abort, render_template , request
from flask_login import current_user, login_required
from ..models import Vote, Poll
from ..models import db
from forms import VoteForm
from . import home


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard/<int:id>')
# @home.route('/dashboard')
@login_required
def dashboard(id):
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html',id=id, title="Dashboard")

@home.route('/voting/<int:id>', methods=['GET', 'POST'])
@login_required
def voting(id):
    """
    Render the dashboard template on the /dashboard route
    """

    if request.method == 'POST':
        vote = Vote.query.get_or_404(id)
        vote.vaoted_to = request.form.get('field')
        db.session.add(vote)
        db.session.commit()
        return render_template('home/ThankYou.html')

    vote = Vote.query.get_or_404(id)
    poll = Poll.query.get_or_404(vote.poll_id)
    e = poll.electorate
    if vote.voter_id == current_user.id:
        if vote.vaoted_to:
            return render_template('home/dashboard.html', id=current_user.id, title="Dashboard")
        form = VoteForm(obj=vote)
        return render_template('home/voting.html', electorate=e, title="Voting")
    else:
        return render_template('home/dashboard.html', id=current_user.id, title="Dashboard")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")
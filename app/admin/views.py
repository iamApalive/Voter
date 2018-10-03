# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import PollForm , RoleForm , VotersAssignForm
from .. import db
from ..models import Poll , Role, Voters , Vote


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# Department Views


@admin.route('/polls', methods=['GET', 'POST'])
@login_required
def list_polls():
    """
    List all polls
    """
    check_admin()

    polls = Poll.query.all()

    return render_template('admin/polls/polls.html',
                           polls=polls, title="Polls")


@admin.route('/polls/add', methods=['GET', 'POST'])
@login_required
def add_poll():
    """
    Add a poll to the database
    """
    check_admin()

    add_poll = True

    form = PollForm()
    if form.validate_on_submit():
        poll = Poll(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(poll)
            db.session.commit()
            flash('You have successfully added a new poll.')
        except:
            # in case poll name already exists
            flash('Error: poll name already exists.')

        # redirect to polls page
        return redirect(url_for('admin.list_polls'))

    # load department template
    return render_template('admin/polls/poll.html', action="Add",
                           add_poll=add_poll, form=form,
                           title="Add Poll")


@admin.route('/polls/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_poll(id):
    """
    Edit a poll
    """
    check_admin()

    add_poll = False

    poll = Poll.query.get_or_404(id)
    form = PollForm(obj=poll)
    if form.validate_on_submit():
        poll.name = form.name.data
        poll.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the poll.')

        # redirect to the departments page
        return redirect(url_for('admin.list_polls'))

    form.description.data = poll.description
    form.name.data = poll.name
    return render_template('admin/polls/poll.html', action="Edit",
                           add_poll=add_poll, form=form,
                           poll=poll, title="Edit Poll")


@admin.route('/polls/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_poll(id):
    """
    Delete a poll from the database
    """
    check_admin()

    poll = Poll.query.get_or_404(id)
    db.session.delete(poll)
    db.session.commit()
    flash('You have successfully deleted the poll.')

    # redirect to the departments page
    return redirect(url_for('admin.list_polls'))

    return render_template(title="Delete Poll")

@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


@admin.route('/voters')
@login_required
def list_voters():
    """
    List all voters
    """
    check_admin()

    voters = Voters.query.all()
    return render_template('admin/voters/voters.html',
                           voters=voters, title='Voters')


@admin.route('/voters/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_voter(id):
    """
    Assign a poll and a role to an voter
    """
    check_admin()
    flag_001 = False
    voter = Voters.query.get_or_404(id)
    poll = Poll.query.get(voter.poll.id)
    # prevent admin from being assigned a department or role
    if voter.is_admin:
        abort(403)

    form = VotersAssignForm(obj=voter)
    if form.validate_on_submit():
        voter.poll = form.poll.data
        voter.role = form.role.data
        db.session.add(voter)
        db.session.commit()

        vote = Vote.query.get(voter.id)
        if not vote:
            vote = Vote()
            vote.id = voter.id
            flag_001 = True
        vote.poll = voter.poll
        vote.voter = voter
        if voter.role.name.lower() == 'electorate':
            electorate = poll.electorate
            if electorate is None:
                electorate = []
            electorate.append(voter.username)
            poll.electorate = electorate
        else:
            if not flag_001:

                electorate = poll.electorate
                if voter.username in electorate:
                    electorate.remove(voter.username)
                    poll.electorate = electorate
        db.session.add(vote)
        db.session.commit()
        db.session.add(poll)
        db.session.commit()
        flash('You have successfully assigned a poll and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_voters'))

    return render_template('admin/voters/voter.html',
                           voter=voter, form=form,
                           title='Assign Voter')

@admin.route('/votes')
@login_required
def list_votes():
    """
    List all votes
    """
    check_admin()

    votes = Vote.query.all()

    return render_template('admin/votes/votes.html',
                           votes=votes, title='Votes')

@admin.route('/votes/<int:id>', methods=['GET','POST'])
@login_required
def vote_details(id):
    """
    Assign a poll and a role to an voter
    """
    vote = Vote.query.get_or_404(id)

    return render_template('admin/votes/vote.html',
                           vote=vote,title='Vote Details')

@admin.route('/results/<int:id>', methods=['GET'])
@login_required
def poll_results(id):
    """
    providing result of the poll
    """
    poll = Poll.query.get_or_404(id)
    electorate = poll.electorate
    result = dict((el,0) for el in electorate)
    votes = Vote.query.all()
    for vote in votes:
        if vote.vaoted_to is not None:
            result[vote.vaoted_to] +=1

    return render_template('admin/polls/result.html',
                           result=result,name=poll.name,title='Poll Results')

# @app.route('/admin/create/user', methods=['GET', 'POST'])
# def admin_create_user():
#     check_admin()
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password.data
#         user_exists = Voters.query().filter_by(email=email).first()
#         if user_exists:
#             form.email.errors.append(email + ' is already associated with another user')
#             form.email.data = email
#             email = ''
#             return render_template('create-user.html', form = form)
#
#         else:
#             register_user(
#                     email=email,
#                     password = password)
#             flash('User added successfully')
#             return render_template('create-user.html', form = form)
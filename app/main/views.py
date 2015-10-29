# _*_ coding:utf-8 _*_

from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, abort, flash
from flask.ext.login import login_required, current_user

from . import main
from ..models import User, Role
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db
from ..decorators import admin_required


@main.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@main.route('/user/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return  render_template('profile.html', user=user)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('个人信息已经更新')
        return redirect(url_for('.profile', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('该用户信息已更改')
        return redirect(url_for('main.profile', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)






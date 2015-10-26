# _*_ coding:utf-8 _*_

from flask import render_template, redirect, url_for, request, flash
from flask.ext.login import login_user, logout_user, login_required, current_user

from . import auth
from .forms import LoginFrom, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from ..models import User
from .. import db
from ..email import send_email


@auth.before_app_request
def before_app_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('邮箱或密码错误，请重新登录')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经注销登录了.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, role_id=3)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '确认用户', 'auth/email/confirm', user=user, token=token)
        flash('注册成功,确认邮件已经发送到您的邮箱')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('用户已经确认')
    else:
        flash('确认链接不可用或已经失效')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认用户', 'auth/email/confirm', user=current_user, token=token)
    flash('一封新的确认邮件已经发送到您的邮箱，请注意查收')
    return redirect(url_for('main.index'))


@auth.route('/changepwd', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash("您的密码已经更改了")
            return redirect(url_for('main.index'))
        else:
            flash("密码输入错误")
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, '重置密码', 'auth/email/reset_password', user=user, token=token)
            flash('已发送重置密码请求邮件到您的邮箱，注意查收')
        return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/pwdreset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect('main.index')
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset(token, form.password.data):
            flash('您的密码已经更新')
            return redirect(url_for('auth.login'))
        else:
            flash('确认链接不可用或已经失效')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/changeemail', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, '确认新邮箱地址', 'auth/email/change_email', user=current_user, token=token)
            flash("确认邮件已发送到您的新邮箱中，注意查收")
            return redirect(url_for('main.index'))
        else:
            flash("密码输入错误")
    return render_template('auth/change_email.html', form=form)


@auth.route('/changeemail/<token>')
@login_required
def change_email(token):
    if current_user.email_change(token):
        flash('您的邮箱地址应改变')
    else:
        flash('确认链接不可用或已经失效')
    return redirect(url_for('main.index'))

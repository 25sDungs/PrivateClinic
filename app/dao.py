import hashlib
from app.models import QuyDinh, User
from app import db
from flask import render_template, redirect


def load_quydinh():
    return QuyDinh.query.all()


def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User.query.filter(User.username.__eq__(username), User.password.__eq__(password))
    if role:
        u = u.filter(User.user_role.__eq__(role))
    return u.first()


def get_user_by_id(id):
    return User.query.get(id)

# def change_quydinh_benhnhan(giatri):
#     item = QuyDinh.query.filter_by(id='1').first()
#     item.GiaTri = giatri
#     db.session.commit()
#     return redirect('admin/quydinhview')
#
#
# def change_quydinh_tienkham(giatri):
#     item = QuyDinh.query.filter_by(id='2').first()
#     item.GiaTri = giatri
#     db.session.commit()
#     return redirect('/admin/quydinhview')

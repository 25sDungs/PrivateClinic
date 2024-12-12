from app.models import QuyDinh
from app import db
from flask import render_template, redirect


def load_quydinh():
    return QuyDinh.query.all()


def change_quydinh_benhnhan(giatri):
    item = QuyDinh.query.filter_by(id='1')
    item.GiaTri = giatri
    db.session.commit()
    return redirect('admin/quydinhview')


def change_quydinh_tienkham(giatri):
    item = QuyDinh.query.filter_by(id='2')
    item.GiaTri = giatri
    db.session.commit()
    return redirect('/admin/quydinhview')

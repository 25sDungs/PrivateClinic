from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Double
from sqlalchemy.orm import relationship
from enum import Enum as RoleEnum
import hashlib
from flask_login import UserMixin
from app import app, db


class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2  # Patient
    DOCTOR = 3
    NURSE = 4


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)


class QuyDinh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    TenQuyDinh = Column(String(50), nullable=False, unique=True)
    GiaTri = Column(Integer)
    MoTa = Column(String(100))


class LoaiThuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    TenLoaiThuoc = Column(String(50), nullable=False, unique=True)
    Thuocs = relationship('Thuoc', backref='loaithuoc', lazy=True)


class DonVi(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    TenDonVi = Column(String(50), unique=True)
    SoLuong = Column(Integer)
    MoTa = Column(String(50))
    Thuocs = relationship('Thuoc', backref='donvi', lazy=True)

    def __str__(self):
        return self.TenDonVi


class Thuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    TenThuoc = Column(String(50), unique=True)
    LoaiThuoc_id = Column(Integer, ForeignKey(LoaiThuoc.id), nullable=False)
    DonVi_id = Column(Integer, ForeignKey(DonVi.id), nullable=False)
    GiaThuoc = Column(Integer)
    SoLuong = Column(Integer)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # l1 = LoaiThuoc(TenLoaiThuoc='Thao Duoc')
        # dv1 = DonVi(TenDonVi='Vi', SoLuong=12, MoTa='1 vi = 12 vien')
        # db.session.add(l1)
        # db.session.add(dv1)

        # t1 = Thuoc(TenThuoc="ThuocDoc", LoaiThuoc_id=1, DonVi_id=1, GiaThuoc=200000, SoLuong=10)
        # t2 = Thuoc(TenThuoc="ThuocGiai", LoaiThuoc_id=1, DonVi_id=1, GiaThuoc=5000000, SoLuong=3)
        # db.session.add_all([t1, t2])
        # q1 = QuyDinh(TenQuyDinh='Số Bệnh Nhân Khám', MoTa='Số Bệnh Nhân Khám Trong Ngày', GiaTri=40)
        # q2 = QuyDinh(TenQuyDinh='Số Tiền Khám', MoTa='Số Tiền Khám', GiaTri=100000)
        # db.session.add_all([q1, q2])

        # u = User(username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRole.ADMIN, gender="Nam",phone='0000000000')
        # db.session.add(u)
        db.session.commit()

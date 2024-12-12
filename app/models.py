from sqlalchemy import Column, Integer, String, Double, ForeignKey
from sqlalchemy.orm import relationship

from app import app, db


class QuyDinh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    TenQuyDinh = Column(String(50), nullable=False, unique=True)
    GiaTri = Column(Integer)
    MoTa = Column(String(100))


class LoaiThuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    TenLoaiThuoc = Column(String(50), nullable=False, unique=True)


class DonVi(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    TenDonVi = Column(String(50), unique=True)
    SoLuong = Column(Integer)
    MoTa = Column(String(50))


class Thuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    TenThuoc = Column(String(50), unique=True)
    LoaiThuoc_id = Column(Integer, ForeignKey(LoaiThuoc.id), nullable=False)
    DonVi = Column(Integer, ForeignKey(DonVi.id), nullable=False)
    GiaThuoc = Column(Integer)
    SoLuong = Column(Integer)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # l1 = LoaiThuoc(TenLoaiThuoc='Thao Duoc')
        # dv1 = DonVi(TenDonVi='Vi', SoLuong=12, MoTa='1 vi = 12 vien')
        # db.session.add(l1)
        # db.session.add(dv1)

        t1 = Thuoc(TenThuoc="ThuocDoc", LoaiThuoc_id=1, DonVi=1, GiaThuoc=200000, SoLuong=10)
        t2= Thuoc(TenThuoc="ThuocGiai", LoaiThuoc_id=1, DonVi=1, GiaThuoc=5000000, SoLuong=3)
        db.session.add_all([t1,t2])
        q1 = QuyDinh(TenQuyDinh='Số Bệnh Nhân Khám', MoTa='Số lượng bệnh nhân tiếp nhận trong 1 ngày', GiaTri=40)
        q2 = QuyDinh(TenQuyDinh='Số Tiền Khám', MoTa='Số tiền khám cơ bản', GiaTri=100000)
        db.session.add_all([q1,q2])

        db.session.commit()

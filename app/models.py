from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Double, Boolean, DateTime
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

    def __str__(self):
        return self.TenLoaiThuoc


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
    ThuocTrongPhieuKhams = relationship('ThuocTrongPhieuKham', backref='thuoc', lazy=True)


class HoaDon(db.Model):
    __tablename__ = 'hoa_don'
    id = Column(Integer, primary_key=True, autoincrement=True)
    TienKham = Column(Double)
    TienThuoc = Column(Double)
    TinhTrangThanhToan = Column(Boolean)
    # mqh 1-1
    phieu_kham = relationship("PhieuKham", back_populates="hoa_don", uselist=False)
    # dung back_populates thay the cho backref


class PhieuKham(db.Model):
    __tablename__ = 'phieu_kham'
    id = Column(Integer, primary_key=True, autoincrement=True)
    NgayLapPhieu = Column(DateTime)
    ThuocTrongPhieuKhams = relationship('ThuocTrongPhieuKham', backref='phieukham', lazy=True)
    # Tạo mối quan hệ 1-1
    HoaDon_id = Column(Integer, ForeignKey('hoa_don.id'), unique=True)
    hoa_don = relationship("HoaDon", back_populates="phieu_kham", uselist=False)
    # dung back_populates thay the cho backref


class ThuocTrongPhieuKham(db.Model):
    PhieuKham_id = Column(Integer, ForeignKey(PhieuKham.id), primary_key=True, nullable=False)
    Thuoc_id = Column(Integer, ForeignKey(Thuoc.id), primary_key=True, nullable=False)
    LieuLuong = Column(String(50))
    CachDung = Column(String(50))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        l1 = LoaiThuoc(TenLoaiThuoc='Thảo Dược')
        dv1 = DonVi(TenDonVi='Vĩ', SoLuong=12, MoTa='1 vi = 12 vien')
        db.session.add(l1)
        db.session.add(dv1)

        t1 = Thuoc(TenThuoc="Thuốc Độc", LoaiThuoc_id=1, DonVi_id=1, GiaThuoc=200000, SoLuong=10)
        t2 = Thuoc(TenThuoc="Thuốc Giải", LoaiThuoc_id=1, DonVi_id=1, GiaThuoc=5000000, SoLuong=3)
        db.session.add_all([t1, t2])
        q1 = QuyDinh(TenQuyDinh='Số Bệnh Nhân Khám', MoTa='Số Bệnh Nhân Khám Trong Ngày', GiaTri=40)
        q2 = QuyDinh(TenQuyDinh='Số Tiền Khám', MoTa='Số Tiền Khám', GiaTri=100000)
        db.session.add_all([q1, q2])

        u = User(username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRole.ADMIN, gender="Nam", phone='0000000000')
        db.session.add(u)

        # Tính tiền thuốc và lấy tiền khám từ db
        hd1 = HoaDon(TienThuoc=300000, TienKham=100000, TinhTrangThanhToan=True)
        hd2 = HoaDon(TienThuoc=299000, TienKham=100000, TinhTrangThanhToan=True)
        hd3 = HoaDon(TienThuoc=594000, TienKham=100000, TinhTrangThanhToan=True)
        hd4 = HoaDon(TienThuoc=388000, TienKham=100000, TinhTrangThanhToan=True)
        hd5 = HoaDon(TienThuoc=186000, TienKham=100000, TinhTrangThanhToan=True)
        hd6 = HoaDon(TienThuoc=789000, TienKham=100000, TinhTrangThanhToan=True)
        db.session.add_all([hd1, hd2, hd3, hd4, hd5, hd6])

        ngaypk1 = datetime(2024, 12, 6)
        pk1 = PhieuKham(NgayLapPhieu=ngaypk1, HoaDon_id=1)
        ngaypk2 = datetime(2024, 11, 14)
        pk2 = PhieuKham(NgayLapPhieu=ngaypk2, HoaDon_id=2)
        ngaypk3 = datetime(2024, 12, 19)
        pk3 = PhieuKham(NgayLapPhieu=ngaypk3, HoaDon_id=3)
        ngaypk4 = datetime(2024, 10, 6)
        pk4 = PhieuKham(NgayLapPhieu=ngaypk1, HoaDon_id=4)
        ngaypk5 = datetime(2024, 9, 14)
        pk5 = PhieuKham(NgayLapPhieu=ngaypk2, HoaDon_id=5)
        ngaypk6 = datetime(2024, 12, 19)
        pk6 = PhieuKham(NgayLapPhieu=ngaypk3, HoaDon_id=6)
        db.session.add_all([pk1, pk2, pk3, pk4, pk5, pk6])

        Drug1InReport1 = ThuocTrongPhieuKham(Thuoc_id='1', PhieuKham_id='1', LieuLuong='10 viên 1 ngày',
                                             CachDung='Dùng Sau Khi Ăn')
        Drug2InReport1 = ThuocTrongPhieuKham(Thuoc_id='2', PhieuKham_id='1', LieuLuong='2 viên 1 ngày',
                                             CachDung='Dùng Sau Khi Ăn')
        Drug1InReport2 = ThuocTrongPhieuKham(Thuoc_id='1', PhieuKham_id='2', LieuLuong='3 viên 1 ngày',
                                             CachDung='Dùng Sau Khi Ăn')
        Drug1InReport3 = ThuocTrongPhieuKham(Thuoc_id='1', PhieuKham_id='3', LieuLuong='5 viên 1 ngày',
                                             CachDung='Dùng Sau Khi Ăn')
        Drug1InReport4 = ThuocTrongPhieuKham(Thuoc_id='1', PhieuKham_id='4', LieuLuong='10 viên 1 ngày',
                                             CachDung='Dùng Sau Khi Ăn')
        Drug2InReport4 = ThuocTrongPhieuKham(Thuoc_id='2', PhieuKham_id='4', LieuLuong='2 viên 1 ngày',
                                             CachDung='Dùng Sau Khi Ăn')
        Drug1InReport5 = ThuocTrongPhieuKham(Thuoc_id='1', PhieuKham_id='5', LieuLuong='3 viên 1 ngày',
                                             CachDung='Dùng Sau Khi Ăn')
        Drug1InReport6 = ThuocTrongPhieuKham(Thuoc_id='1', PhieuKham_id='6', LieuLuong='5 viên 1 ngày',
                                             CachDung='Dùng Sau Khi Ăn')
        db.session.add_all(
            [Drug1InReport1, Drug2InReport1, Drug1InReport2, Drug1InReport3, Drug1InReport4, Drug2InReport4,
             Drug1InReport5, Drug1InReport6])
        db.session.commit()

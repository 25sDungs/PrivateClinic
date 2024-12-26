import hashlib
from app.models import User, HoaDon, Thuoc, QuyDinh, PhieuKham, ThuocTrongPhieuKham
from app import db
from flask import render_template, redirect


# def load_quydinh():
#     return QuyDinh.query.all()

# def load_drugs():
#     d = Thuoc.query.all()
#     return d


def is_pay(hoadon_id=None):
    p = HoaDon.query.get(hoadon_id).TinhTrangThanhToan
    if p:
        return True
    return False


def load_bills(kw=None):
    query = HoaDon.query
    if kw:
        query = query.filter(HoaDon.id.contains(kw))
    return query.all()


def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User.query.filter(User.username.__eq__(username), User.password.__eq__(password))
    if role:
        u = u.filter(User.user_role.__eq__(role))
    return u.first()


def get_user_by_id(id):
    return User.query.get(id)


def load_thuoc():
    return Thuoc.query.all()


# Lap Phieu Kham
def them_phieu_kham(ngay, benh):
    tienKham = QuyDinh.query.get(2).GiaTri
    hd = HoaDon(TienThuoc=0, TienKham=tienKham, TinhTrangThanhToan=False)
    db.session.add(hd)
    db.session.commit()
    pk = PhieuKham(NgayLapPhieu=ngay, LoaiBenh=benh, HoaDon_id=hd.id)
    db.session.add(pk)
    db.session.commit()
    return pk.id


def cap_nhat_tien_thuoc(phieu_id, tien):
    phieu = PhieuKham.query.filter(PhieuKham.id == phieu_id).first()
    hoadon = HoaDon.query.get(phieu.HoaDon_id)
    hoadon.TienThuoc = tien
    db.session.commit()


def tao_thuoc_trong_phieu_kham(ten, SoLuong, CachDung, phieu_id):
    thuoc = Thuoc.query.filter(Thuoc.TenThuoc.contains(ten)).first()
    DrugInReport = ThuocTrongPhieuKham(Thuoc_id=thuoc.id, PhieuKham_id=phieu_id, LieuLuong=SoLuong,
                                       CachDung=CachDung)
    db.session.add(DrugInReport)
    db.session.commit()
    return float(thuoc.GiaThuoc * SoLuong)

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

from sqlalchemy import func

from app import db
from app.models import HoaDon, PhieuKham, ThuocTrongPhieuKham


def sum_revenue(lists):
    s = 0
    for i in lists:
        s += i[-1]
    return s


# lấy các tháng có dl
def get_months_of_data():
    query = db.session.query(func.day(PhieuKham.NgayLapPhieu).label('day')).distinct()
    return query.all()


def revenue_stats(month=None, from_date=None, to_date=None):
    p = (db.session.query(PhieuKham.NgayLapPhieu,func.count(PhieuKham.id) ,func.sum(HoaDon.TienKham + HoaDon.TienThuoc))
         .join(HoaDon, HoaDon.id == PhieuKham.HoaDon_id).group_by(PhieuKham.NgayLapPhieu).order_by(PhieuKham.NgayLapPhieu))
    if month:
        p = p.filter(func.month(PhieuKham.NgayLapPhieu) == month)
    if from_date:
        p = p.filter(PhieuKham.NgayLapPhieu.__ge__(from_date))
    if to_date:
        p = p.filter(PhieuKham.NgayLapPhieu.__le__(to_date))

    return p.all()


def drug_stats(month=None, from_date=None, to_date=None):
    p = (db.session.query(PhieuKham.id, func.max(ThuocTrongPhieuKham.Thuoc_id).label('max_Thuoc_id'))
         .join(ThuocTrongPhieuKham, ThuocTrongPhieuKham.PhieuKham_id == PhieuKham.id).group_by(PhieuKham.id))
    if month:
        p = p.filter(func.month(PhieuKham.NgayLapPhieu) == month)
    if from_date:
        p = p.filter(PhieuKham.NgayLapPhieu.__ge__(from_date))
    if to_date:
        p = p.filter(PhieuKham.NgayLapPhieu.__le__(to_date))

    return p.all()

from flask import render_template, request, redirect
from flask_login import login_user, logout_user
from app.models import UserRole, Thuoc, QuyDinh
from app import app, login, db
import dao, utils


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login-admin', methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password, role=UserRole.ADMIN)
    if u:
        login_user(u)
    return redirect('/admin')


# @app.route('/add-drug', methods=['POST'])
# def add_drug():
#     print(request.form.get('action'))
#     if request.form.get('action') == 'add':
#         tenthuoc = request.form['tenthuoc']
#         loaithuoc = request.form['loaithuoc']
#         soluong = int(request.form['soluong'])
#         donvi = request.form['donvi']
#         giathuoc = float(request.form['giathuoc'])
#
#         new_drug = Thuoc(
#             TenThuoc=tenthuoc,
#             LoaiThuoc_id=loaithuoc,
#             SoLuong=soluong,
#             DonVi_id=donvi,
#             GiaThuoc=giathuoc
#         )
#         db.session.add(new_drug)
#         db.session.commit()
#         drugs = dao.load_drugs()
#         return render_template('admin/quanlythuoc.html', drugs=drugs)
#  return redirect('admin/thuocview/')


# @app.route("/update", methods=['post'])
# def quydinh_process():
#     if 'btnCnBenhNhan' in request.form:
#         giatri = request.form.get('ipBenhNhanMoi')
#         if giatri:
#             return dao.change_quydinh_benhnhan(giatri)
#     elif 'btnCnTienKham' in request.form:
#          giatri = request.form.get('ipTienMoi')
#          if giatri:
#              return dao.change_quydinh_tienkham(giatri)
#     return redirect('/admin/quydinhview')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


# Hoa Don Chuc Nang
@app.route("/bills/<int:bill_id>", methods=['GET', 'POST'])
def bill_detail(bill_id):
    thuocs = utils.load_thuoc_trong_hoa_don(bill_id)
    sum = utils.sum_revenue(thuocs)
    tienkham = QuyDinh.query.get(2).GiaTri
    tinhtrangthanhtoan = dao.is_pay(bill_id)
    return render_template('chitiethoadon.html', tinhtrangthanhtoan=tinhtrangthanhtoan,
                           sum=sum, tienkham=tienkham, thuocs=thuocs, mahoadon=bill_id)


@app.route('/bills', methods=['GET', 'POST'])
def bill_process():
    kw = request.args.get('billID')
    date = request.args.get('billDate')
    bills = utils.load_bills_data(kw=kw, date=date)
    tienkham = QuyDinh.query.get(2).GiaTri

    return render_template('thungan.html', tienkham=tienkham, bills=bills)


@app.route("/phieukham", methods=['GET', 'POST'])
def phieu_kham():
    thuoc = dao.load_thuoc()

    if request.method.__eq__('POST'):
        tong_thuoc = 0
        tien_thuoc = 0
        ngay = request.form.get('dateForm')
        benh = request.form.get('disease-txt')
        data = request.form.copy()
        # grouped_data = [data_list[i:i + 3] for i in range(0, len(data_list), 3)]
        del data['docName']
        del data['sdt']
        del data['dateForm']
        del data['disease-txt']
        data_list = list(data.items())
        grouped_data = [data_list[i:i + 3] for i in range(0, len(data_list), 3)]
        id = int(dao.them_phieu_kham(ngay, benh))
        for group in grouped_data:

            for key, value in group:
                if 'medicine' in key:
                    medicine = value
                if 'med-instruct' in key:
                    instruct = value
                if 'med-number' in key:
                    num = float(value)
                    tien_thuoc = dao.tao_thuoc_trong_phieu_kham(medicine, num, instruct, id)
                    tong_thuoc = tien_thuoc + tong_thuoc

        dao.cap_nhat_tien_thuoc(id, tong_thuoc)
    return render_template('phieukham.html', thuocs=thuoc)


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)

from flask import render_template, request, redirect
from app import app
import dao


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/update", methods=['post'])
def quydinh_process():
    # if 'btnCnBenhNhan' in request.form:
    #     giatri = request.form.get('ipBenhNhanMoi')
    #     return dao.change_quydinh_benhnhan(giatri)
    # elif 'btnCnTienKham' in request.form:
    #     giatri = request.form.get('ipTienMoi')
    #     return dao.change_quydinh_tienkham(giatri)
    return redirect('/admin/quydinh.html')


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)

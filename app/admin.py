from app import app, db
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.models import Thuoc, LoaiThuoc
import dao

admin = Admin(app=app, name='PhongMachTu', template_mode='bootstrap4')


# class QuyDinhView(ModelView):
#     column_list = ['id', 'TenQuyDinh', 'GiaTri', 'MoTa']
#     column_searchable_list = ['TenQuyDinh']
#     # column_editable_list = ['TenQuyDinh']
#     page_size = 6


class ThuocView(ModelView):
    column_list = ['id', 'TenThuoc', 'LoaiThuoc_id', 'DonVi', 'GiaThuoc', 'SoLuong']
    column_searchable_list = ['TenThuoc']
    column_filters = ['TenThuoc', 'GiaThuoc']
    column_editable_list = ['TenThuoc']
    page_size = 6


class LoaiThuocView(ModelView):
    column_list = ['id', 'TenLoaiThuoc']


class StatsView(BaseView):
    @expose("/")
    def index(self):
        # ...
        return self.render('admin/stats.html')


class QuyDinhView(BaseView):
    @expose("/")
    def index(self):
        quydinh = dao.load_quydinh()
        return self.render('admin/quydinh.html', quydinh=quydinh)


admin.add_view(ThuocView(Thuoc, db.session))
admin.add_view(LoaiThuocView(LoaiThuoc, db.session))
admin.add_view(StatsView(name='Thống Kê'))
admin.add_view(QuyDinhView(name='Quy Định'))

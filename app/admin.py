from app import app, db
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.models import QuyDinh, Thuoc, LoaiThuoc

admin = Admin(app=app, name='PhongMachTu')


class QuyDinhView(ModelView):
    column_list = ['id', 'TenQuyDinh', 'GiaTri', 'MoTa']
    column_searchable_list = ['TenQuyDinh']
    # column_editable_list = ['TenQuyDinh']
    page_size = 6


class ThuocView(ModelView):
    column_list = ['id', 'TenThuoc', 'DonVi', 'GiaThuoc', 'SoLuong']
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


admin.add_view(QuyDinhView(QuyDinh, db.session))
admin.add_view(ThuocView(Thuoc, db.session))
admin.add_view(LoaiThuocView(LoaiThuoc, db.session))
admin.add_view(StatsView(name='Thống Kê'))

from app import app, db
from flask import redirect, request
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.models import Thuoc, LoaiThuoc, QuyDinh, UserRole, User
from flask_login import current_user, logout_user
import dao, utils

admin = Admin(app=app, name='PhongMachTu', template_mode='bootstrap4')


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class QuyDinhView(AdminView):
    column_list = ['id', 'TenQuyDinh', 'GiaTri', 'MoTa']
    column_searchable_list = ['TenQuyDinh']
    column_editable_list = ['TenQuyDinh']


class UserView(AdminView):
    column_list = ['id', 'username', 'user_role', 'phone']
    column_searchable_list = ['username', 'phone']
    column_editable_list = ['user_role']


class ThuocView(AdminView):
    column_list = ['id', 'TenThuoc', 'LoaiThuoc_id', 'DonVi', 'GiaThuoc', 'SoLuong']
    column_searchable_list = ['TenThuoc']
    column_filters = ['TenThuoc', 'GiaThuoc']
    column_editable_list = ['TenThuoc']
    page_size = 6


class LoaiThuocView(AdminView):
    column_list = ['id', 'TenLoaiThuoc']


class BaseAdminView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class StatsView(BaseAdminView):
    @expose("/")
    def index(self):
        month = request.args.get('ThangThongKe')
        type_stats = request.args.get('LoaiThongKe')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')

        if type_stats == 'Revenue':
            rstats = utils.revenue_stats(month=month, from_date=from_date, to_date=to_date)
            return self.render('admin/stats.html', sum=utils.sum_revenue(rstats), rstats=rstats)

        if type_stats == 'Drug':
            dstats = utils.drug_stats(month=month, from_date=from_date, to_date=to_date)
            return self.render('admin/stats.html',dstats=dstats)

        return self.render('admin/stats.html')


class LogoutView(BaseAdminView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')


admin.add_view(UserView(User, db.session))
admin.add_view(ThuocView(Thuoc, db.session))
admin.add_view(LoaiThuocView(LoaiThuoc, db.session))
admin.add_view(QuyDinhView(QuyDinh, db.session))
admin.add_view(StatsView(name='Thống Kê'))
admin.add_view(LogoutView(name='Đăng Xuất'))

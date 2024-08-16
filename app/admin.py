from flask import redirect
from flask_admin import Admin, AdminIndexView, expose
from app import db, app
from app.models import Phong, KhachHang, NhanVien, TaiKhoan, DonDatPhong, ChiTietDonDatPhong, PhieuThuePhong, HoaDon, UserRoleEnum
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user


class BaseView(ModelView):
    can_view_details = True
    edit_modal = True
    details_modal = True
    # can_export = True
    # column_searchable_list = ['name', 'mota']

class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.NHANVIEN
class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app=app, name='QUẢN LÝ KHÁCH SẠN', template_mode='bootstrap4')
admin.add_view(AuthenticatedAdmin(Phong, db.session, name='Phòng'))
admin.add_view(AuthenticatedAdmin(KhachHang, db.session, name='Khách hàng'))
admin.add_view(AuthenticatedAdmin(NhanVien, db.session, name='Nhân viên'))
admin.add_view(AuthenticatedAdmin(TaiKhoan, db.session, name='Tài khoản'))
admin.add_view(AuthenticatedAdmin(DonDatPhong, db.session, name='Đơn đặt phòng'))
admin.add_view(AuthenticatedAdmin(ChiTietDonDatPhong, db.session, name='Chi tiết đơn đặt phòng'))
admin.add_view(AuthenticatedAdmin(PhieuThuePhong, db.session, name='Phiếu thuê phòng'))
admin.add_view(AuthenticatedAdmin(HoaDon, db.session, name='Hóa đơn'))

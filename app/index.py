from datetime import datetime

from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user

import dao
from app import login
from app.admin import *
from app.models import LoaiKhachHang



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/room_list')

def room_list():
    kw = request.args.get('keyword')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    rooms = dao.load_phong(kw=kw, from_price=from_price, to_price=to_price)
    return render_template('room_list.html', room_list=rooms)

@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')

@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)

@app.route("/login", methods=['get', 'post'])
def process_user_login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            next = request.args.get('next')
            return redirect('/' if next is None else next)

    return render_template('login.html')




@app.route('/logout')
def process_user_logout():
    logout_user()
    return redirect("/login")


@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = None

    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_user(tenTK=request.form.get('tenTK'), username=request.form.get('username'), password=password, email=request.form.get('email'), phone=request.form.get('phone'))
            except Exception as ex:
                print(str(ex))
                err_msg = 'Hệ thống đang bị lỗi!'
            else:
                return redirect('/login')
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('/register.html', err_msg=err_msg)

@app.route('/danhSachPhongDat')
def danhSachPhongDat():
    return render_template('danhSachPhongDat.html')

@app.route('/dat-phong', methods=['GET', 'POST'])
@login_required
def booking():
    if request.method == 'POST':
        ma_phong = int(request.form['ma_phong'])
        ho_kh = request.form['ho_kh']
        ten_kh = request.form['ten_kh']
        phone = request.form['phone']
        cmnd = request.form['cmnd']
        dia_chi = request.form['dia_chi']
        quoc_tich = request.form['quoc_tich']
        ma_loai_khach_hang = request.form['ma_loai_khach_hang']

        ngay_dat_phong = datetime.now()


        loai_khach_hang = LoaiKhachHang.query.get(ma_loai_khach_hang)
        if not loai_khach_hang:
            loai_khach_hang = LoaiKhachHang.query.filter_by(TenLoaiKH='Khách vãng lai').first()


        khach_hang = KhachHang(HoKH=ho_kh, TenKH=ten_kh, Phone=phone, CMND=cmnd, DiaChi=dia_chi, QuocTich=quoc_tich, LoaiKH=loai_khach_hang.MaLoaiKH)
        db.session.add(khach_hang)
        db.session.commit()


        don_dat_phong = DonDatPhong(MaPhong=ma_phong, NgayDatPhong=ngay_dat_phong)
        db.session.add(don_dat_phong)
        db.session.commit()

        return redirect(url_for('index'))

    danh_sach_phong = Phong.query.all()
    danh_sach_loai_khach_hang = LoaiKhachHang.query.all()
    return render_template('booking.html', danh_sach_phong=danh_sach_phong, danh_sach_loai_khach_hang=danh_sach_loai_khach_hang)

if __name__ == "__main__":
    app.run(debug=True)

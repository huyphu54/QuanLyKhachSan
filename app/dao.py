import hashlib
from flask_login import current_user
from app import db, app
from app.models import Phong, LoaiPhong, TaiKhoan as TK, DonDatPhong, ChiTietDonDatPhong


def load_phong(kw=None,from_price=None, to_price=None):

    phong = Phong.query.join(LoaiPhong, Phong.MaLoaiPhong == LoaiPhong.MaLoaiPhong).add_columns(LoaiPhong.DonGia,
                                                                                               LoaiPhong.TenLoaiPhong,
                                                                                               LoaiPhong.Image).all()
    if kw:
        phong = [p for p in phong if (p.TenLoaiPhong.lower().find(kw.lower()) >= 0) ]

    if from_price:
        phong = [p for p in phong if p.DonGia >= float(from_price)]

    if to_price:
        phong = [p for p in phong if p.DonGia <= float(to_price)]

    return phong



def get_user_by_id(user_id):
    return TK.query.get(user_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return TK.query.filter(TK.Username.__eq__(username.strip()),
                             TK.Password.__eq__(password)).first()



def add_user(tenTK, username, password, email, phone):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    tk = TK(TenTK=tenTK, Username=username, Password=password, Email=email, Phone=phone)

    # if avatar:
    #     res = cloudinary.uploader.upload(avatar)
    #     print(res)
    #     u.avatar = res['secure_url']

    db.session.add(tk)
    db.session.commit()

def get_taikhoan():
    return TK.query.all()
# def get_phong_by_id(id):
#     return Phong.query.get(id)
def get_loaiphong():
    return LoaiPhong.query.all()

def add_dondatphong(danhSachPhongDat, ngayNhanPhong,ngayTraPhong):
    if danhSachPhongDat:
        donDatPhong = DonDatPhong(taiKhoan=current_user)
        db.session.add(donDatPhong)
        for c in danhSachPhongDat.values():
            d = ChiTietDonDatPhong(MaPhong=c['MaPhong'],MaDonDatPhong=donDatPhong,NgayNhanPhong=ngayNhanPhong, NgayTraPhong=ngayTraPhong)

            db.session.add(d)

        db.session.commit()



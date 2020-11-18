from flask import render_template, request, redirect
from saleapp import app, utils, models, login
from saleapp.admin import *
from flask_login import login_user
import hashlib
import os


@app.route("/")
def index():
    categories = utils.read_data()
    return render_template('index.html',
                          categories=categories)


@app.route("/register", methods=['GET', 'POST'])
def register():
    err_msg = ''
    if request.method == 'POST':
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password", '').strip()
        confirm_password = request.form.get("confirm_password", '').strip()
        email = request.form.get("email")

        if password == confirm_password:
            # import pdb
            # pdb.set_trace() -> Debug

            avatar = request.files['avatar']
            avatar_path = 'images/upload/%s' % avatar.filename
            path = os.path.join(app.root_path, 'static/', avatar_path)
            avatar.save(path)

            password = str(hashlib.md5(password.encode("utf8")).hexdigest())
            u = models.User(name=name, username=username, password=password, email=email, avatar=avatar_path)
            db.session.add(u)
            db.session.commit()

            return redirect('/')
        else:
            err_msg = "Mat khau khong khop"

    return render_template('register.html', err_msg=err_msg)


@app.route("/products")
def product_list():
    kw = request.args.get("kw")
    cate_id = request.args.get("category_id")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")

    products = utils.read_products(cate_id=cate_id,
                                   kw=kw,
                                   from_price=from_price,
                                   to_price=to_price)

    return render_template('products.html',
                           products=products)


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = utils.get_product_by_id(product_id=product_id)

    return render_template('product-detail.html',
                           product=product)


@login.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)


@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf8")).hexdigest())
        user = models.User.query.filter(models.User.username == username, models.User.password == password).first()

        if user:
            login_user(user=user)

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)

from saleapp import admin, db, models
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from saleapp.models import Category, Product
from flask_login import logout_user, current_user
from flask import redirect


class AccessibleView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class ContactView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/contact.html')


class HomeView(BaseView):
    @expose('/')
    def index(self):
        return redirect('/')


class CategoryModelView(ModelView, AccessibleView):
    form_columns = ('name',)


class ProductModelView(ModelView, AccessibleView):
    pass


class LogOutView(AccessibleView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(CategoryModelView(Category, db.session))
admin.add_view(ProductModelView(Product, db.session))
admin.add_view(ContactView(name='Liên hệ', endpoint='contact'))
admin.add_view(HomeView(name='Trang chu'))
admin.add_view(LogOutView(name='Dang xuat'))
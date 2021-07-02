from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render

from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from mainapp.models import Product, ProductCategory

from authapp.forms import ShopUserRegisterForm

from adminapp.forms import ShopUserAdminEditForm

from adminapp.forms import ProductCategoryAdminEditForm, ProductAdminEditForm
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView, UpdateView


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     context = {
#         'title': title,
#         'objects': users_list
#     }
#
#     return render(request, 'adminapp/users.html', context=context)


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserRegisterForm
    success_url = 'adminapp/users.html'


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserRegisterForm
    success_url = 'adminapp/users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователь/редактирование'

        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'пользователи/создание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('adminapp:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     context = {'title': title, 'update_form': user_form}
#
#     return render(request, 'adminapp/user_update.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'пользователи/редактирование'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, \
#                                           instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin:user_update', \
#                                                 args=[edit_user.pk]))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     context = {'title': title, 'update_form': edit_form}
#
#     return render(request, 'adminapp/user_update.html', context=context)


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    context_object_name = 'user_to_delete'
    success_url = reverse_lazy('admin_staff:users')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        # self.object.is_active=False
        # self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = 'пользователи/удаление'
#
#     user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         # user.delete()
#         # вместо удаления лучше сделаем неактивным
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('adminapp:users'))
#
#     context = {'title': title, 'user_to_delete': user}
#
#     return render(request, 'adminapp/user_delete.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка/категории'
#
#     categories_list = ProductCategory.objects.all()
#
#     context = {
#         'title': title,
#         'objects': categories_list
#     }
#
#     return render(request, 'adminapp/categories.html', context=context)

class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    form_class = ProductCategoryAdminEditForm
    success_url = reverse_lazy('admin_staff:categories')


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    form_class = ProductCategoryAdminEditForm
    success_url = 'adminapp/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'

        return context


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'категории/создание'
#
#     if request.method == 'POST':
#         category_form = ProductCategoryAdminEditForm(request.POST, request.FILES)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         category_form =ProductCategoryAdminEditForm()
#
#     context = {'title': title, 'update_form': category_form}
#
#     return render(request, 'adminapp/category_create.html', context=context)


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категории/редактирование'
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         category_form = ProductCategoryAdminEditForm(request.POST, request.FILES, instance=edit_category)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('adminapp:category_update', args=[edit_category.pk]))
#     else:
#         category_form = ProductCategoryAdminEditForm(instance=edit_category)
#
#     context = {'title': title, 'update_form': category_form}
#
#     return render(request, 'adminapp/category_update.html', context=context)


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    context_object_name = 'category_to_delete'
    success_url = reverse_lazy('admin_staff:categories')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        # self.object.is_active=False
        # self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'категории/удаление'
#     delete_category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         delete_category.delete()
#
#         return HttpResponseRedirect(reverse('adminapp:categories'))
#
#     context = {'title': title, 'category_to_delete': delete_category}
#
#     return render(request, 'adminapp/category_delete.html', context=context)


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    # context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/продукт'
        context['category'] = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context['objects'] = Product.objects.filter(category__pk=self.kwargs['pk'])

        return context

        @method_decorator(user_passes_test(lambda u: u.is_superuser))
        def dispatch(self, *args, **kwargs):
            return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     title = 'админка/продукт'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category__pk=pk).order_by('name')
#
#     context = {
#         'title': title,
#         'category': category,
#         'objects': products_list,
#     }
#
#     return render(request, 'adminapp/products.html', context=context)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_create.html',
    form_class = ProductAdminEditForm


    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={'category': get_object_or_404(ProductCategory, id=self.kwargs['pk'])})
        return render(request, self.template_name, {'form': form, 'title': 'продукт/создание'})

    def get_success_url(self):

        return reverse('admin_staff:products', kwargs={'pk': self.object.category.pk})



# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     title = 'продукты/создание'
#
#     product_category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         product_form = ProductAdminEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[product_category.pk]))
#     else:
#         product_form = ProductAdminEditForm(initial= {'category':  product_category.id})
#
#     context = {'title': title,  'update_form': product_form}
#
#     return render(request, 'adminapp/product_create.html', context=context)



class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'
    form_class = ProductAdminEditForm

    def get(self, request, *args, **kwargs):
        read_product = get_object_or_404(Product, id=self.kwargs['pk'])
        read_form = ProductAdminEditForm(instance=read_product)
        return render(request, self.template_name, {'form': read_form, 'title': 'продукт/подробнее', 'read_product': read_product})


    # def get_success_url(self):
    #     return reverse('admin_staff:product_read', kwargs={'pk': self.object.category.pk})

    # def get(self, request, *args, **kwargs):
    #     read_product = get_object_or_404(Product, id=self.kwargs['pk'])
    #     read_form = ProductAdminEditForm(instance=read_product)
    # #     return render(request, self.template_name, {'form': read_form, 'title': 'продукт/редактирование'})
    #
    # def get_success_url(self):
    #     return reverse('admin_staff:products', kwargs={'pk': self.object.category.pk})

#
# def product_read(request, pk):
#     title = 'продукты/подробнее'
#
#     read_product = get_object_or_404(Product, pk=pk)
#     # du spes eir gre
#     # read_category = get_object_or_404(Category, pk=pk)
#
#     # kstananq categoryn @st id-i
#     # read_category = get_object_or_404(Product, pk=read_product.category_id)
#     # kogtagorcenq arden isk kopit sac load exac categoryn
#     read_category = read_product.category
#
#     if request.method == 'POST':
#         product_form = ProductAdminEditForm(request.POST, request.FILES, instance=read_product)
#         if product_form.is_valid():
#             return HttpResponseRedirect(reverse('adminapp:products'))
#     else:
#         product_form = ProductAdminEditForm(instance=read_product)
#
#     context = {'title': title, 'category': read_category, 'update_form': product_form, }
#
#     return render(request, 'adminapp/product_read.html', context=context)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html',
    form_class = ProductAdminEditForm

    def get(self, request, *args, **kwargs):

        edit_product = get_object_or_404(Product, id=self.kwargs['pk'])
        edit_form = ProductAdminEditForm(instance=edit_product)
        return render(request, self.template_name, {'form': edit_form, 'title': 'продукт/редактирование'})

    def get_success_url(self):

        return reverse('admin_staff:products', kwargs={'pk': self.object.category.pk})


# def product_update(request, pk):
#     title = 'продукты/редактирование'
#
#     edit_product = get_object_or_404(Product, pk=pk)
#     edit_category = edit_product.category
#
#     if request.method == 'POST':
#         edit_form = ProductAdminEditForm(request.POST, request.FILES, instance=edit_product)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('adminapp:product_update', args=[edit_product.pk]))
#     else:
#         edit_form = ProductAdminEditForm(instance=edit_product)
#
#     context = {'title': title, 'category': edit_category, 'update_form': edit_form}
#
#     return render(request, 'adminapp/product_update.html', context=context)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    context_object_name = 'product_to_delete'

    def delete(self, request, *args, **kwargs):
        self.object=self.get_object()
        success_url=self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


    def get_success_url(self):
        return reverse('admin_staff:products', kwargs={'pk': self.object.category.pk})




# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     title = 'категории/удаление'
#     delete_product = get_object_or_404(Product, pk=pk)
#     delete_category = delete_product.category
#
#     if request.method == 'POST':
#         delete_product.delete()
#
#         return HttpResponseRedirect(reverse('adminapp:products', args=[delete_category.pk]))
#
#     context = {'title': title, 'category': delete_category, 'product_to_delete': delete_product}
#
#     return render(request, 'adminapp/product_delete.html', context=context)

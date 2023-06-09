from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User, auth
from django.shortcuts import get_object_or_404, redirect, render

from bill_coll import forms
from bill_coll.decorators import *

from .ExtraneousFolder import ExtraFunctions
from .models import *

# Create your views here.

# @login_required(login_url='/signin')


def index(request):
    isAdmin = False
    user = request.user
    print("userrrid", user.id)
    print(request.user.pk)
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if (group == "consumer"):
        return redirect("/consumer_Dashboard")
    if (group == "admin"):
        # isAdmin = True
        return redirect("/admin_Dashboard")
    else:
        print("home sweet home")
        return redirect("/Home")
    # user = Profile.objects.get(id_user=request.user.id)
    collection_list = Collection.objects.order_by('package')
    print(collection_list)
    package_list = Package.objects.order_by('name')
    dict = {'title': "homepage", 'collection_list': collection_list,
            'package_list': package_list, 'user': user}
    # return render(request, 'bill_coll/index.html', context=dict)


@login_required(login_url='/signin')
def Dashboard(request):
    user = request.user
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if (group == "consumer"):
        return redirect("/consumer_Dashboard")
    if (group == "admin"):
        return redirect("/admin_Dashboard")
    return redirect("/")


@allowed_user(allowed_roles=['admin'])
@login_required(login_url='/signin')
def admin_Dashboard(request):
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    isAdmin = ExtraFunctions.isAdmin(group)
    # return redirect("/admin_Dashboard")
    user = request.user
    print("hello", user)
    # print("pk is", pk)
    # user = get_object_or_404(User,username=pk)
    print("user is", request.user.pk)
    collection_list = Collection.objects.order_by('package')
    package_list = Package.objects.order_by('name')
    dict = {'title': "Dashboard", 'collection_list': collection_list,
            'user': user, 'user_id': request.user.pk, 'isAdmin': isAdmin}
    return render(request, 'bill_coll/admin_Dashboard.html', context=dict)


@allowed_user(allowed_roles=['consumer'])
@login_required(login_url='/signin')
def consumer_Dashboard(request):
    user = request.user
    user_profile = Profile.objects.get(id_user=user.pk)
    print(user_profile.photo.url)
    print(user.id)
    dict = {
        'title': "Dashboard",
        'user': user,
        'profile': user_profile
    }
    return render(request, 'bill_coll/consumer_Dashboard.html', context=dict)


def Home(request):
    user = Profile.objects.filter(id_user=request.user.pk).first()
    print("user in home page", user)
    package_list = Package.objects.order_by('name')
    dict = {'title': "Homepage", 'package_list': package_list, 'user': user}
    return render(request, 'bill_coll/Home.html', context=dict)


@allowed_user(allowed_roles=['admin'])
@login_required(login_url='/signin')
def Collections(request):
    # isAdmin = False
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if (group == "admin"):
        isAdmin = request.user.groups.exists()
        # return redirect("/admin_Dashboard")
    user = request.user
    print("hello", user)
    # print("pk is", pk)
    # user = get_object_or_404(User,username=pk)
    print("user is", request.user.pk)
    collection_list = Collection.objects.order_by('package')
    package_list = Package.objects.order_by('name')
    dict = {'title': "Dashboard", 'collection_list': collection_list,
            'user': user, 'user_id': request.user.pk, 'isAdmin': isAdmin}
    return render(request, 'bill_coll/Collection.html', context=dict)


@allowed_user(allowed_roles=['admin'])
@login_required(login_url='/signin')
def Packages(request):  # , package_id):
    user = User.objects.filter(pk=request.user.pk).first()
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    isAdmin = ExtraFunctions.isAdmin(group)
    # package_list = Package.objects.filter(pk=package_id)
    package_list = Package.objects.order_by('name')
    dict = {'title': "homepage", 'package_list': package_list,
            'user': user, 'isAdmin': isAdmin}
    return render(request, 'bill_coll/Packages.html', context=dict)


@allowed_user(allowed_roles=['admin'])
@login_required(login_url='/signin')
def Users(request):
    dict = {'title': "Users"}
    return render(request, 'bill_coll/Users.html', context=dict)

# @unauthenticated_user


def signup(request):
    user = Profile.objects.filter(
        id_user=request.user.id).first()  # prevents anonymous user
    dict = {'user': user}
    # if request.user.is_authenticated: #is_authenticated will return true/false
    # return redirect('/')
    # else:
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists.')
                return redirect('/signup')
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken.')
                return redirect('/signup')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                # create a profile for new user
                user_model = User.objects.get(username=username)
                group = Group.objects.get(name='consumer')
                user_model.groups.add(group)
                new_profile = Profile.objects.create(
                    user=user_model, id_user=user_model.id)
                print(user_model)
                print("id_user exists?", new_profile.id_user)
                new_profile.save()
                messages.success(request, 'Signup Successful')
                return redirect('/signup')

        else:
            messages.info(request, 'Password didn\'t match.')
            return redirect('/signup')

    return render(request, 'bill_coll/signup.html', context=dict)

# @unauthenticated_user


def signin(request):
    # user = request.user #this will work after sign in
    user = Profile.objects.filter(id_user=request.user.pk).first()
    dict = {'user': user}
    # print("username", user.user.username)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # null if it can't find
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('/signin')

    else:
        return render(request, 'bill_coll/signin.html', context=dict)


def logout(request):
    auth.logout(request)
    return redirect('/signin')


def addpackage(request):
    form = forms.PackageForm
    if request.method == "POST":  # if user typed something, Post == data hidden
        form = forms.PackageForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)

    dict = {'title': "addpackage", 'package_form': form}
    return render(request, 'bill_coll/addpackage.html', context=dict)


def viewpackage(request, package_id):
    user = request.user
    package_info = Package.objects.get(pk=package_id)  # pk is primary key
    dict = {'title': "viewpackage", 'package_info': package_info, 'user': user}
    return render(request, 'bill_coll/viewpackage.html', context=dict)


def editpackage(request, package_id):
    edit_package = Package.objects.get(pk=package_id)
    form = forms.PackageForm(instance=edit_package)
    user = Profile.objects.filter(id_user=request.user.pk)
    if request.method == "POST":  # if user typed something, Post == data hidden
        form = forms.PackageForm(request.POST, instance=edit_package)

        if form.is_valid():
            form.save(commit=True)
            # return index(request)
            return redirect('/Packages')

    dict = {'title': "editpackage", 'edit_package_form': form, 'user': user}
    return render(request, 'bill_coll/editpackage.html', context=dict)


def deletepackage(request, package_id):
    package_info = Package.objects.get(pk=package_id)
    package_info.delete()
    dict = {'title': "deletepackage"}
    return render(request, 'bill_coll/deletepackage.html', context=dict)


def addcity(request):
    form = forms.CityForm
    if request.method == "POST":  # if user typed something, Post == data hidden
        form = forms.CityForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)

    dict = {'title': "addcity", 'city_form': form}
    return render(request, 'bill_coll/addcity.html', context=dict)


def viewcity(request, city_id):
    user = request.user
    city_info = City.objects.get(pk=city_id)  # pk is primary key
    dict = {'title': "viewcity", 'city_info': city_info, 'user': user}
    return render(request, 'bill_coll/viewcity.html', context=dict)


def editcity(request, city_id):
    edit_city = City.objects.get(pk=city_id)
    form = forms.CityForm(instance=edit_city)
    user = Profile.objects.filter(id_user=request.user.pk)
    if request.method == "POST":  # if user typed something, Post == data hidden
        form = forms.CityForm(request.POST, instance=edit_city)

        if form.is_valid():
            form.save(commit=True)
            return index(request)

    dict = {'title': "editcity", 'edit_city_form': form, 'user': user}
    return render(request, 'bill_coll/editcity.html', context=dict)


def deletecity(request, city_id):
    city_info = City.objects.get(pk=city_id)
    city_info.delete()
    dict = {'title': "deletecity"}
    return render(request, 'bill_coll/deletecity.html', context=dict)


def addarea(request):
    form = forms.AreaForm
    if request.method == "POST":  # if user typed something, Post == data hidden
        form = forms.AreaForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)

    dict = {'title': "addarea", 'area_form': form}
    return render(request, 'bill_coll/addarea.html', context=dict)


def viewarea(request, area_id):
    user = request.user
    area_info = Area.objects.get(pk=area_id)  # pk is primary key
    dict = {'title': "viewarea", 'area_info': area_info, 'user': user}
    return render(request, 'bill_coll/viewarea.html', context=dict)


def editarea(request, area_id):
    edit_area = Area.objects.get(pk=area_id)
    form = forms.AreaForm(instance=edit_area)
    user = Profile.objects.filter(id_user=request.user.pk)
    if request.method == "POST":  # if user typed something, Post == data hidden
        form = forms.AreaForm(request.POST, instance=edit_area)

        if form.is_valid():
            form.save(commit=True)
            return index(request)

    dict = {'title': "editarea", 'edit_area_form': form, 'user': user}
    return render(request, 'bill_coll/editarea.html', context=dict)


def deletearea(request, area_id):
    area_info = Area.objects.get(pk=area_id)
    area_info.delete()
    dict = {'title': "deletearea"}
    return render(request, 'bill_coll/deletearea.html', context=dict)


def addcollection(request):
    form = forms.CollectionForm
    if request.method == "POST":  # if user typed something, Post == data hidden
        form = forms.CollectionForm(request.POST)

        user_id = request.POST['user_id']
        profile = Profile.objects.filter(id_user=user_id).first()

        package_id = request.POST['package']
        package = Package.objects.get(pk=package_id)
        print(package)

        month_id = request.POST['billMonth']
        month = Month.objects.get(pk=month_id)
        profile.paidThruMonth = month.name
        profile.package = package
        # return render(request, 'bill_coll/addcollection.html')

        if form.is_valid():
            form.save(commit=True)
            profile.save()
            return index(request)

    dict = {'title': "addcollection", 'collection_form': form}
    return render(request, 'bill_coll/addcollection.html', context=dict)


def viewcollection(request, collection_id):
    user = request.user
    collection_info = Collection.objects.get(
        pk=collection_id)  # pk is primary key
    dict = {'title': "viewcollection",
            'collection_info': collection_info, 'user': user}
    return render(request, 'bill_coll/viewcollection.html', context=dict)


def editcollection(request, collection_id):
    edit_collection = Collection.objects.get(pk=collection_id)
    form = forms.CollectionForm(instance=edit_collection)
    user = Profile.objects.filter(id_user=request.user.pk)

    if request.method == "POST":  # if user typed something, Post == data hidden
        form = forms.CollectionForm(request.POST, instance=edit_collection)

        user_id = request.POST['user_id']
        profile = Profile.objects.filter(id_user=user_id).first()

        package_id = request.POST['package']
        package = Package.objects.get(pk=package_id)

        month_id = request.POST['billMonth']
        month = Month.objects.get(pk=month_id)
        profile.paidThruMonth = month.name
        profile.package = package

        if form.is_valid():
            form.save(commit=True)
            profile.save()
            return index(request)

    dict = {'title': "editcollection",
            'edit_collection_form': form, 'user': user}
    return render(request, 'bill_coll/editcollection.html', context=dict)


def deletecollection(request, collection_id):
    collection_info = Collection.objects.get(pk=collection_id)
    collection_info.delete()
    dict = {'title': "deletecollection"}
    return render(request, 'bill_coll/deletecollection.html', context=dict)


@login_required(login_url='/signin')
def update_profile(request, pk):
    user = get_object_or_404(Profile, id_user=pk)
    form = forms.UpdateProfile(instance=user)

    if request.method == 'POST':
        form = forms.UpdateProfile(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            messages.info(request, 'Profile updated successfully')
            return redirect('/user/' + str(pk))

    dict = {'user': user, 'form': form}
    return render(request, 'bill_coll/update_profile.html', context=dict)


# AJAX
def load_areas(request):
    city_id = request.GET.get('city_id')
    areas = Area.objects.filter(city_id=city_id).all()
    dict = {'areas': areas}
    return render(request, 'bill_coll/city_dropdown_list_options.html', context=dict)

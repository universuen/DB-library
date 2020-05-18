from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages
from django import forms
from .models import *
import django.utils.timezone as timezone


# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')

def sign_up(request):
    if request.method == 'POST':
        form = forms.Form(request.POST)
        username = form.data['username']
        password = form.data['password']
        identity = form.data['identity']
        if len(identity) * len(password) * len(username) == 0:
            messages.error(request, '填写信息不能为空')
            return render(request, 'sign_up.html')
        if User.objects.filter(username=username).count() != 0:
            messages.error(request, username + '已被注册, 请更换其他用户名')
            return render(request, 'sign_up.html')
        obj = User.objects.create(username=username, password=password, identity=identity)
        obj.save()
        messages.success(request, '注册成功!')
        return redirect(reverse('library:sign_in'))
    else:
        return render(request, 'sign_up.html')


def sign_in(request):
    if request.method == 'POST':
        form = forms.Form(request.POST)
        username = form.data['username']
        if User.objects.filter(username=username).count() == 0:
            messages.error(request, '无法在数据库中找到' + username + '的信息')
            return render(request, 'sign_in.html')
        request.session['username'] = username
        return render(request, 'function.html')
    else:
        return render(request, 'sign_in.html')


def search(request):
    if request.method == 'POST':
        form = forms.Form(request.POST)
        result = Book.objects.all()
        if form.data['name']:
            result = Book.objects.filter(name=form.data['name'])
        if form.data['id']:
            result = result.filter(id=form.data['id'])
        if form.data['publish_house']:
            result = result.filter(publish_house=form.data['publish_house'])
        if form.data['release_date']:
            result = result.filter(release_date=form.data['release_date'])
        if form.data['author']:
            result = result.filter(author=form.data['author'])
        if form.data['category']:
            result = result.filter(category=form.data['category'])
        if len(result) == 0:
            messages.error(request, '未查询到符合条件的图书！')
            return render(request, 'search.html')
        else:
            data = [[] for _ in range(len(result))]
            for i in range(len(result)):
                item = result[i]
                data[i].append(str(item.name))
                data[i].append(str(item.id))
                data[i].append(str(item.publish_house))
                data[i].append(str(item.release_date))
                data[i].append(str(item.author))
                data[i].append(item.category)
                data[i].append(item.status)
                data[i].append(str(item.return_date))
            request.session['data'] = data
            return redirect(reverse('library:borrow'))
    else:
        return render(request, 'search.html')

def function(request):
    return render(request, 'function.html')

def borrow(request):
    if request.method == 'POST':
        form = forms.Form(request.POST)
        id = form.data['id']
        if not id:
            messages.error(request,'图书ID不可为空！')
            return redirect(reverse('library:borrow'))
        if Book.objects.filter(id=id).count() == 0:
            messages.error(request, '无法在数据库中找到ID为' + str(id) + '的图书')
            return redirect(reverse('library:borrow'))
        if Book.objects.get(id=id).status == '未借出':
            book = Book.objects.get(id=id)
            book.status = '正常借出'
            borrower = User.objects.get(username=request.session['username'])
            book.borrower = borrower
            return_date = timezone.datetime.now() + timezone.timedelta(days=7)
            book.return_date = return_date.strftime("%Y-%m-%d")
            book.save()
            messages.error(request, '已成功借阅《'+book.name+'》请在' +book.return_date+'之前归还图书')
            return redirect(reverse('library:function'))
        else:
            messages.error(request, '抱歉，该图书已借出')
            return redirect(reverse('library:borrow'))
    else:
        data = request.session['data']
        return render(request, 'borrow.html', {'data':data})

def renew(request):
    user = User.objects.get(username=request.session['username'])
    books = user.books.all()
    if request.method == 'POST':
        form = forms.Form(request.POST)
        id = form.data['id']
        if not id:
            messages.error(request,'图书ID不可为空！')
            return redirect(reverse('library:renew'))
        if books.filter(id=id).count() == 0:
            messages.error(request, '您未借阅ID为' + str(id) + '的图书')
            return redirect(reverse('library:renew'))
        book = Book.objects.get(id=id)
        return_date = book.return_date
        today = timezone.localdate()
        if book.status == '续借':
            messages.error(request, '您已续借过该图书，无法连续续借')
            return redirect(reverse('library:renew'))
        if return_date > today:
            book.status = '续借'
            borrower = User.objects.get(username=request.session['username'])
            book.borrower = borrower
            return_date = timezone.datetime.now() + timezone.timedelta(days=7)
            book.return_date = return_date.strftime("%Y-%m-%d")
            book.save()
            messages.error(request, '已成功续借《'+book.name+'》请在' +book.return_date+'之前归还图书')
            return redirect(reverse('library:function'))
        else:
            messages.error(request, '抱歉，您未在规定时间内归还该图书，已失去该图书的续借资格')
            return redirect(reverse('library:renew'))
    else:
        data = [[] for _ in range(len(books))]
        for i in range(len(books)):
            item = books[i]
            data[i].append(str(item.name))
            data[i].append(str(item.id))
            data[i].append(str(item.publish_house))
            data[i].append(str(item.release_date))
            data[i].append(str(item.author))
            data[i].append(item.category)
            data[i].append(item.status)
            data[i].append(str(item.return_date))
        return render(request, 'renew.html', {'data':data})

def return_book(request):
    user = User.objects.get(username=request.session['username'])
    books = user.books.all()
    if request.method == 'POST':
        form = forms.Form(request.POST)
        id = form.data['id']
        if not id:
            messages.error(request,'图书ID不可为空！')
            return redirect(reverse('library:return_book'))
        if books.filter(id=id).count() == 0:
            messages.error(request, '您未借阅ID为' + str(id) + '的图书')
            return redirect(reverse('library:return_book'))
        book = Book.objects.get(id=id)
        messages.error(request, '已成功归还《' + book.name + '》')
        return_date = book.return_date
        today = timezone.localdate()
        book.status = '未借出'
        book.borrower = None
        book.return_date = None
        book.save()
        if return_date <= today:
            messages.error(request, '您未在规定时间内归还该图书，下不为例')
        return redirect(reverse('library:function'))
    else:
        data = [[] for _ in range(len(books))]
        for i in range(len(books)):
            item = books[i]
            data[i].append(str(item.name))
            data[i].append(str(item.id))
            data[i].append(str(item.publish_house))
            data[i].append(str(item.release_date))
            data[i].append(str(item.author))
            data[i].append(item.category)
            data[i].append(item.status)
            data[i].append(str(item.return_date))
        return render(request, 'return_book.html', {'data':data})
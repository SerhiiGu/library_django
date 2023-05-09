# from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.http import HttpResponse

from libUser.models import *
from libUser.utils.user_utils import *


@login_required(login_url='/login/')
def books_on_read(request):
    reading_books = Books.objects.filter(userbooks__user_id=request.user.id, userbooks__status=1).all()
    return render(request, "books_on_read.html", {"books": reading_books})


@login_required(login_url='/login/')
def books_unreaded(request):
    # unread_books = Books.objects.exclude(userbooks__user_id=request.user.id).exclude(userbooks__status=0).all()
    unread_books = Books.objects.exclude(userbooks__user_id=request.user.id, userbooks__status__in=[0, 1]).all()
    books = []
    for book in unread_books:
        if book.free_count > 0:
            can_booking = "yes"
        else:
            can_booking = "no"
        books.append((book.pk, request.user.id, book.author, book.title, can_booking))
    return render(request, "books_unreaded.html", {"books": books})


@login_required(login_url='/login/')
def books_readed(request):
    readed_books = Books.objects.filter(userbooks__user_id=request.user.id, userbooks__status=0).all()
    return render(request, "books_readed.html", {"books": readed_books})


@login_required(login_url='/login/')
def books_to_read(request):
    books = UserBooks.objects.filter(user_id=request.user.id, status=2).all()
    return render(request, "books_to_read.html", {"books": books})


@login_required(login_url='/login/')
def books_booking_to_read(request, pk):
    if request.method == 'POST':
        book = Books.objects.filter(pk=pk).first()
        book_add = UserBooks(status=2, book_id=pk, user_id=request.user.id)
        book_add.save()
        messages.success(request, "Книга зарезервована")
        return redirect('books_unreaded')
    messages.error(request, "Неможливий запит на цю адресу!")
    return redirect('books_unreaded')


@login_required(login_url='/login/')
def books_ask_for_new(request):
    return None


def login_handler(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, "login.html", {"error": "Помилка в логіні/паролі, або ж неіснуючий користувач!"})
    return render(request, "login.html")


def logout_handler(request):
    logout(request)
    return redirect('login')


def register_handler(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username, email, password)
        user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, "register.html", {"error": "Щось пішло не так, спробуйте знову"})
    return render(request, "register.html")

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import datetime

from libUser.models import *
from libUser.utils.user_utils import *


def panel_books_in_users(request):
    if not request.user.has_perm('libUser.add_books'):
        messages.error(request, "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки")
        return redirect('panel_login')
    books = []
    books_used = Books.objects.filter(users_use__gt=1).all()
    for book in books_used:
        for user_id in book.users_use.strip().split(","):
            if user_id:
                books.append((book.pk, user_id, book.author, book.title, id_to_name(user_id)))
    return render(request, "panel_books_in_users.html", {"books": books})


def panel_book_from_user(request, pk, user_id):
    if not request.user.has_perm('libUser.add_books'):
        messages.error(request, "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки")
        return redirect('panel_login')
    if request.method == 'POST':
        book = Books.objects.filter(pk=pk).first()
        book.free_count += 1
        book.users_use = remove_user_from_book_usage(book.users_use, user_id)
        book.save()
        history = UserBooks.objects.filter(book_id=book.id, user_id=user_id).first()
        history.status = 0
        history.save()
        book_history = BooksHistory.objects.filter(book_id=book.id, user_id=user_id).first()
        book_history.dt_end = datetime.datetime.now(datetime.timezone.utc)
        book_history.save()
        messages.success(request, "Книга прийнята")
        return redirect('panel_books_in_users')
    messages.error(request, "Неможливий запит на цю адресу!")
    return redirect('panel_books_in_users')


def panel_books_all(request):
    if not request.user.has_perm('libUser.add_books'):
        messages.error(request, "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки")
        return redirect('panel_login')
    all_books = Books.objects.all()
    books = query_to_list(all_books)
    return render(request, "panel_books_all.html", {"books": books})


def panel_book_edit(request, book_id):
    if not request.user.has_perm('libUser.add_books'):
        messages.error(request, "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки")
        return redirect('panel_login')
    if request.method == 'POST':
        book = Books.objects.filter(id=book_id).first()
        book.author = request.POST['author']
        book.title = request.POST['title']
        book.description = request.POST['description']
        new_all = int(request.POST['all_count'])
        if new_all > book.all_count:
            diff = new_all - book.all_count
            book.free_count = diff + book.free_count
        else:
            diff = book.all_count - new_all
            book.free_count = book.free_count - diff
        book.all_count = int(request.POST['all_count'])
        book.save()
        messages.success(request, "Книгу відредаговано")
        return redirect('panel_books_all')
    book = Books.objects.filter(id=book_id).first()
    min = book.all_count - book.free_count
    return render(request, 'panel_book_edit.html', {"book": book, "min": min})


def panel_books_free(request):
    if not request.user.has_perm('libUser.add_books'):
        messages.error(request, "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки")
        return redirect('panel_login')
    free_books = Books.objects.filter(free_count__gt=0).all()
    books = query_to_list(free_books)
    return render(request, "panel_books_free.html", {"books": books})


def panel_requests_for_books(request):
    if not request.user.has_perm('libUser.add_books'):
        messages.error(request, "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки")
        return redirect('panel_login')
    books = UserBooks.objects.filter(status=2).all()
    return render(request, "panel_requests_for_books.html", {"books": books})


def panel_book_give_to_user(request, book_id, user_id):
    if not request.user.has_perm('libUser.add_books'):
        messages.error(request, "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки")
        return redirect('panel_login')
    if request.method == 'POST':
        user_book = UserBooks.objects.filter(user_id=user_id, book_id=book_id).first()
        user_book.status = 1
        user_book.save()
        book = Books.objects.filter(pk=book_id).first()
        book.free_count -= 1
        book.users_use = book.users_use + str(user_book.user_id) + ','
        book.save()
        book_history = BooksHistory(book_id=book_id, user_id=user_book.user_id, dt_end=datetime.datetime.utcfromtimestamp(0))
        book_history.save()
        messages.success(request, "Книга видана")
        return redirect('panel_requests_for_books')
    messages.error(request, "Неможливий запит на цю адресу!")
    return redirect('panel_requests_for_books')


def panel_book_give_reject_to_user(request, book_id, user_id):
    if not request.user.has_perm('libUser.add_books'):
        messages.error(request, "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки")
        return redirect('panel_login')
    if request.method == 'POST':
        user_book = UserBooks.objects.filter(user_id=user_id, book_id=book_id).first()
        user_book.delete()
        messages.success(request, "Бронювання скасовано")
        return redirect('panel_requests_for_books')
    messages.error(request, "Неможливий запит на цю адресу!")
    return redirect('panel_requests_for_books')


def panel_books_wait_list(request, page):
    if not request.user.has_perm('libUser.add_books'):
        messages.error(request, "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки")
        return redirect('panel_login')
    if request.method == 'POST':
        book_id = request.POST['book_id']
        status = request.POST['status']
        book = NewBooks.objects.filter(id=book_id).first()
        book.status = status
        book.save()
    match page:
        case "rejected":
            books = NewBooks.objects.filter(status='rejected').all()
            return render(request, "panel_books_wait_list.html", {"books": books})
        case "approved":
            books = NewBooks.objects.filter(status='approved').all()
            return render(request, "panel_books_wait_list.html", {"books": books})
        case "all":
            books = NewBooks.objects.all()
            return render(request, "panel_books_wait_list.html", {"books": books})
        case _:
            books = NewBooks.objects.filter(status='waiting').all()
            return render(request, "panel_books_wait_list.html", {"books": books})


def panel_book_add(request):
    if not request.user.has_perm('libUser.add_books'):
        messages.error(request, "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки")
        return redirect('panel_login')
    if request.method == 'POST':
        book = Books(
            author=request.POST['author'],
            title=request.POST['title'],
            description=request.POST['description'],
            all_count=request.POST['all_count'],
            free_count=request.POST['all_count']
        )
        book.save()
        return render(request, "panel_add_book.html", {"message": "Книгу додано в бібліотеку"})
    return render(request, "panel_add_book.html")


def panel_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/panel/')
        else:
            return render(request, "panel_login.html", {"error": "Помилка в логіні/паролі, або ж неіснуючий користувач!"})
    return render(request, "panel_login.html")


def panel_logout(request):
    logout(request)
    return redirect('panel_login')

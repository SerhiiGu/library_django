from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from libUser.models import *
from libUser.utils.user_utils import *


def panel_books_in_users(request):
    if not request.user.has_perm('libUser.add_books'):
        return render(request, "panel_books_in_users.html",
                      {"error": "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки"})
    books = []
    books_used = Books.objects.filter(users_use__gt=1).all()
    for book in books_used:
        for user_id in book.users_use.strip().split(","):
            if user_id:
                books.append((book.pk, user_id, book.author, book.title, id_to_name(user_id)))
    return render(request, "panel_books_in_users.html", {"books": books})


def panel_book_from_user(request, pk, user_id):
    if request.method == 'POST':
        book = Books.objects.filter(pk=pk).first()
        book.free_count += 1
        book.users_use = remove_user_from_book_usage(book.users_use, user_id)
        book.save()
        history = UserBooks.objects.filter(book_id=book.id, user_id=user_id).first()
        history.status = 0
        history.save()
        messages.success(request, "Книга прийнята")
        return redirect('panel_books_in_users')
    messages.error(request, "Неможливий запит на цю адресу!")
    return redirect('panel_books_in_users')


def panel_books_all(request):
    if not request.user.has_perm('libUser.add_books'):
        return render(request, "panel_books_all.html",
                      {"error": "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки"})
    all_books = Books.objects.all()
    books = query_to_list(all_books)
    return render(request, "panel_books_all.html", {"books": books})


def panel_books_free(request):
    if not request.user.has_perm('libUser.add_books'):
        return render(request, "panel_books_free.html",
                      {"error": "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки"})
    free_books = Books.objects.filter(free_count__gt=0).all()
    books = query_to_list(free_books)
    return render(request, "panel_books_free.html", {"books": books})


def panel_requests_for_books(request):
    if not request.user.has_perm('libUser.add_books'):
        return render(request, "panel_requests_for_books.html",
                      {"error": "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки"})
    books = UserBooks.objects.filter(status=2).all()
    return render(request, "panel_requests_for_books.html", {"books": books})


def panel_book_give_to_user(request, book_id, user_id):
    if request.method == 'POST':
        user_book = UserBooks.objects.filter(user_id=user_id, book_id=book_id).first()
        user_book.status = 1
        user_book.save()
        book = Books.objects.filter(pk=book_id).first()
        book.free_count -= 1
        book.users_use = book.users_use + str(user_book.user_id) + ','
        book.save()
        messages.success(request, "Книга видана")
        return redirect('panel_requests_for_books')
    messages.error(request, "Неможливий запит на цю адресу!")
    return redirect('panel_requests_for_books')
    pass


def panel_books_wait_list(request):
    return None


def panel_book_add(request):
    if not request.user.has_perm('libUser.add_books'):
        return render(request, "panel_add_book.html",
                      {"error": "Ви не увійшли, або ж не маєте прав для доступу до цієї сторінки"})
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

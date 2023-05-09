from django.contrib.auth.models import User


def ids_to_names(users_ids):
    names = []
    for lst in users_ids.strip().split(","):
        if lst:
            us = User.objects.filter(pk=int(lst)).first().username
            names.append(us)
    str_names = ', '.join(names)
    return str_names


def id_to_name(user_id):
    str_name = User.objects.filter(pk=int(user_id)).first().username
    return str_name


def remove_user_from_book_usage(users_use, to_del):
    new_users_use = ''
    for lst in users_use.strip().split(","):
        if lst and int(lst) != int(to_del):
            new_users_use = new_users_use + lst + ','
    return new_users_use


def query_to_list(query):
    books = []
    for book in query:
        if book.users_use:
            users_use_str = ids_to_names(book.users_use)
        else:
            users_use_str = ''
        books.append((book.pk, book.author, book.title, book.all_count, book.free_count, users_use_str))
    return books

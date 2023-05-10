from django.urls import path
import libAdmin.views

urlpatterns = [
    path('', libAdmin.views.panel_books_in_users, name='panel_books_in_users'),
    path('books/get/<int:pk>/<int:user_id>/', libAdmin.views.panel_book_from_user, name='panel_book_from_user'),
    path('books/all/', libAdmin.views.panel_books_all, name='panel_books_all'),
    path('books/edit/<int:book_id>/', libAdmin.views.panel_book_edit, name='panel_book_edit'),
    path('books/free/', libAdmin.views.panel_books_free, name='panel_books_free'),
    path('books/requests_for_books/', libAdmin.views.panel_requests_for_books, name='panel_requests_for_books'),
    path('books/give/<int:book_id>/<int:user_id>/', libAdmin.views.panel_book_give_to_user, name='panel_book_give_to_user'),
    path('books/give_reject/<int:book_id>/<int:user_id>/', libAdmin.views.panel_book_give_reject_to_user, name='panel_book_give_reject_to_user'),
    path('books/wait_list/', libAdmin.views.panel_books_wait_list, name='panel_books_wait_list'),
    path('books/add/', libAdmin.views.panel_book_add, name='panel_book_add'),
    path('login/', libAdmin.views.panel_login, name='panel_login'),
    path('logout/', libAdmin.views.panel_logout, name='panel_logout'),
]

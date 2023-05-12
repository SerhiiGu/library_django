from django.urls import path
import libUser.views

urlpatterns = [
    path('', libUser.views.books_on_read, name='books_on_read'),
    path('books/unreaded/', libUser.views.books_unreaded, name='books_unreaded'),
    path('books/readed/', libUser.views.books_readed, name='books_readed'),
    path('books/to_read/', libUser.views.books_to_read, name='books_to_read'),
    path('books/booking_reject/<int:book_id>/', libUser.views.books_booking_reject, name='books_booking_reject'),
    path('books/<int:pk>/', libUser.views.books_booking_to_read, name='books_booking_to_read'),
    path('books/ask_for_new/', libUser.views.books_ask_for_new, name='books_ask_for_new'),
    path('login/', libUser.views.login_handler, name='login'),
    path('logout/', libUser.views.logout_handler, name='logout'),
    path('register/', libUser.views.register_handler, name='register'),
]

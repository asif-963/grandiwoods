from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # User Side
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('near-by-places/', views.near_by_places, name='near_by_places'),
    path('near-by-places/<int:pk>/', views.nearby_place_detail, name='nearby_place_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('booking/', views.booking, name='booking'),
    path('room/', views.room, name='room'),
   
    # Admin Login
    path('login/', views.user_login, name='user_login'),
    path('logout-user/', views.logout_user, name='logout_user'),

    # Admin Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Contact Us
    path('contact-view/', views.contact_view, name='contact_view'),
    path('delete-contact/<int:id>/', views.delete_contact, name='delete_contact'),

    # Booking
    path('booking-view/', views.booking_view, name='booking_view'),
    path('delete-booking/<int:id>/', views.delete_booking, name='delete_booking'),

    # Nearby Places
    path('add-near-by-place/', views.add_near_by_place, name='add_near_by_place'),
    path('view-near-by-place/', views.view_near_by_place, name='view_near_by_place'),
    path('update-near-by-place/<int:id>/', views.update_near_by_place, name='update_near_by_place'),
    path('delete-near-by-place/<int:id>/', views.delete_near_by_place, name='delete_near_by_place'),

    # CKEditor Upload
    path('ckeditor-upload/', views.ckeditor_upload, name='ckeditor_upload'),

    # Client Reviews
    path('add-client-review/', views.add_client_review, name='add_client_review'),
    path('view-client-reviews/', views.view_client_reviews, name='view_client_reviews'),
    path('update-client-review/<int:id>/', views.update_client_review, name='update_client_review'),
    path('delete-client-review/<int:id>/', views.delete_client_review, name='delete_client_review'),

    # Folders
    path('add-folders/', views.add_folders, name='add_folders'),
    path('view-folders/', views.view_folders, name='view_folders'),
    path('update-folder/<int:id>/', views.update_folder, name='update_folder'),
    path('delete-folder/<int:id>/', views.delete_folder, name='delete_folder'),

    # Images
    path('add-images/', views.add_images, name='add_images'),
    path('view-images/', views.view_images, name='view_images'),
    path('update-image/<int:id>/', views.update_image, name='update_image'),
    path('delete-image/<int:id>/', views.delete_image, name='delete_image'),

    # Pricing
    path('add-price/', views.add_price, name='add_price'),

    # Chatbot
    path('view-chatbot-messages/', views.view_chatbot_messages, name='view_chatbot_messages'),
    path('delete-chatbot-message/<int:message_id>/', views.delete_chatbot_message, name='delete_chatbot_message'),


    # Guests
    path('guests/add/', views.add_guest, name='add_guest'),
    path('guests/', views.view_guests, name='view_guests'),
    path('guests/update/<int:pk>/', views.update_guest, name='update_guest'),
    path('guests/delete/<int:pk>/', views.delete_guest, name='delete_guest'),


    #robots.txt



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom 404 Error Handler
handler404 = 'grandywoods_app.views.page_404'
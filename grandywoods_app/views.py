from django.shortcuts import  render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import random

from .models import ContactModel, NearByPlace, ClientReview, Gallery, Folder, GalleryImage, Booking, RoomPrice, Guest
from .forms import ContactModelForm, NearByPlaceForm, ClientReviewForm, GalleryForm, FolderForm, BookingForm, GuestForm


def index(request):
    places = NearByPlace.objects.order_by('?')[:3]
    reviews = ClientReview.objects.all()
    guests = Guest.objects.all().order_by('-created_date')
    return render(request, 'index.html', {'places': places, 'reviews':reviews, 'guests':guests})

def about(request):
    reviews = ClientReview.objects.all()
    return render(request, 'about.html', {'reviews':reviews})

def room(request):
    guests = Guest.objects.all().order_by('-created_date')
    return render(request, 'room.html', {'guests':guests})

def near_by_places(request):
    reviews = NearByPlace.objects.all().order_by('-created_date')
    return render(request, 'near_by_places.html', {'reviews': reviews})

def nearby_place_detail(request, pk):
    place = get_object_or_404(NearByPlace, pk=pk)
    other_places = NearByPlace.objects.exclude(pk=pk).order_by('-created_date')[:5]
    return render(request, 'near_by_place_details.html', {'place': place, 'other_places': other_places})

def gallery(request):
    folders = Folder.objects.all().order_by('-id')  # Latest folders first
    images = GalleryImage.objects.select_related('gallery__folder').all().order_by('-id')  # Latest images first

    return render(request, 'gallery.html', {'folders': folders,'images': images})
    


def contact(request):
    if request.method == 'POST':
        form = ContactModelForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact.html')
    else:
        form = ContactModelForm()

    return render(request, 'contact.html', {'form': form})

def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking successful!")  # Show a success message
            return redirect('booking')  # Reload the same page
        else:
            messages.error(request, "There was an error in your booking.")
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form})



# Admin Side
@csrf_protect
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, Admin!")
            return redirect('dashboard')
        else:   
            messages.error(request, "There was an error logging in, try again.")
            return redirect('user_login')
    return render(request, 'authenticate/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out"))
    return redirect('user_login')


#  dashboard
@login_required(login_url='user_login')
def dashboard(request):
    return render(request,'admin_pages/dashboard.html')


# Contact 
@login_required(login_url='user_login')
def contact_view(request):
    contacts = ContactModel.objects.all().order_by('-id')
    return render(request,'admin_pages/contact_view.html',{'contacts':contacts})


@login_required(login_url='user_login')
def delete_contact(request,id):
    contact = ContactModel.objects.get(id=id)
    contact.delete()
    return redirect('contact_view')


# Bookings 
@login_required(login_url='user_login')
def booking_view(request):
    bookings = Booking.objects.all().order_by('-id')
    return render(request,'admin_pages/booking_view.html',{'bookings':bookings})


@login_required(login_url='user_login')
def delete_booking(request,id):
    booking = Booking.objects.get(id=id)
    booking.delete()
    return redirect('booking_view')



# Near by place
@login_required(login_url='user_login')
def add_near_by_place(request):
    if request.method == 'POST':
        form = NearByPlaceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_near_by_place') 
    else:
        form = NearByPlaceForm()

    return render(request, 'admin_pages/add_near_by_place.html', {'form': form})


@login_required(login_url='user_login')
def view_near_by_place(request):
    places = NearByPlace.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_near_by_place.html', {'places': places})


@login_required(login_url='user_login')
def update_near_by_place(request, id):
    place = get_object_or_404(NearByPlace, id=id)
    if request.method == 'POST':
        form = NearByPlaceForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            return redirect('view_near_by_place')
    else:
        form = NearByPlaceForm(instance=place)
    return render(request, 'admin_pages/update_near_by_place.html', {'form': form, 'place': place})

@login_required(login_url='user_login')
def delete_near_by_place(request,id):
    places = NearByPlace.objects.get(id=id)
    places.delete()
    return redirect('view_near_by_place')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

@csrf_exempt
def ckeditor_upload(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']
        file_extension = os.path.splitext(upload.name)[1].lower()
        
        # Check if the uploaded file is an image or a PDF
        if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            folder = 'images'
        elif file_extension == '.pdf':
            folder = 'pdfs'
        else:
            return JsonResponse({'uploaded': False, 'error': 'Unsupported file type.'})

        # Save the file in the appropriate folder
        file_name = default_storage.save(f'{folder}/{upload.name}', ContentFile(upload.read()))
        file_url = default_storage.url(file_name)
        return JsonResponse({
            'uploaded': True,
            'url': file_url
        })
    
    return JsonResponse({'uploaded': False, 'error': 'No file was uploaded.'})





# Client Reviews
@login_required(login_url='user_login')
def add_client_review(request):
    if request.method == 'POST':
        form = ClientReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_client_reviews') 
    else:
        form = ClientReviewForm()

    return render(request, 'admin_pages/add_client_review.html', {'form': form})


@login_required(login_url='user_login')
def view_client_reviews(request):
    client_reviews = ClientReview.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_client_reviews.html', {'client_reviews': client_reviews})


@login_required(login_url='user_login')
def update_client_review(request, id):
    client_reviews = get_object_or_404(ClientReview, id=id)
    if request.method == 'POST':
        form = ClientReviewForm(request.POST, request.FILES, instance=client_reviews)
        if form.is_valid():
            form.save()
            return redirect('view_client_reviews')
    else:
        form = ClientReviewForm(instance=client_reviews)
    return render(request, 'admin_pages/update_client_review.html', {'form': form, 'client_reviews': client_reviews})

    

@login_required(login_url='user_login')
def delete_client_review(request,id):
    client_reviews = ClientReview.objects.get(id=id)
    client_reviews.delete()
    return redirect('view_client_reviews')



# add folders
@login_required(login_url='user_login')
def add_folders(request):
    if request.method == 'POST':
        form = FolderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_images') 
    else:
        form = FolderForm()

    return render(request, 'admin_pages/add_folders.html', {'form': form})

@login_required(login_url='user_login')
def view_folders(request):
    folders = Folder.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_folders.html', {'folders': folders})

@login_required(login_url='user_login')
def update_folder(request, id):
    folder = get_object_or_404(Folder, id=id)
    if request.method == 'POST':
        form = FolderForm(request.POST, request.FILES, instance=folder)
        if form.is_valid():
            form.save()
            return redirect('add_images')
    else:
        form = FolderForm(instance=folder)
    return render(request, 'admin_pages/update_folder.html', {'form': form, 'folder': folder})

@login_required(login_url='user_login')
def delete_folder(request,id):
    folder = Folder.objects.get(id=id)
    folder.delete()
    return redirect('view_folders')


# Add Images
@login_required(login_url='user_login')
def add_images(request):
    folders = Folder.objects.all()
    if request.method == 'POST':
        form = GalleryForm(request.POST)
        if form.is_valid():
            gallery = form.save()
            images = request.FILES.getlist('image')
            for image in images:
                GalleryImage.objects.create(gallery=gallery, image=image)
            return redirect('view_images')  # Redirect to wherever you want after successful upload
    else:
        form = GalleryForm()

    return render(request, 'admin_pages/add_images.html', {'form': form, 'folders': folders})

@login_required(login_url='user_login')
def view_images(request):
    galleries = Gallery.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_images.html', {'galleries': galleries})


@login_required(login_url='user_login')
def update_image(request, id):
    image = get_object_or_404(Gallery, id=id)
    folders = Folder.objects.all()
    
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            updated_image = form.save()

            # Handle image removal
            if 'remove_image' in request.POST:
                remove_image_ids = request.POST.getlist('remove_image')
                for image_id in remove_image_ids:
                    try:
                        image_to_remove = GalleryImage.objects.get(id=image_id)
                        image_to_remove.delete()
                    except GalleryImage.DoesNotExist:
                        pass

            # Save new images
            images = request.FILES.getlist('image')
            for img in images:
                GalleryImage.objects.create(gallery=updated_image, image=img)

            return redirect('view_images')
    else:
        form = GalleryForm(instance=image)

    return render(request, 'admin_pages/update_image.html', {'form': form, 'image': image, 'folders': folders})



@login_required(login_url='user_login')
def delete_image(request,id):
    image = Gallery.objects.get(id=id)
    image.delete()
    return redirect('view_images')


def add_price(request):
    current_price = RoomPrice.objects.first()  # Fetch the first (or only) price record

    if request.method == "POST":
        price_per_night = request.POST.get("price_per_night")
        offer_price = request.POST.get("offer_price")

        # Ensure only one price record exists
        RoomPrice.objects.all().delete()  # Clear previous records
        RoomPrice.objects.create(
            price_per_night=price_per_night,
            offer_price=offer_price or None
        )

        return redirect('add_price')  # Redirect to the same page

    return render(request, 'admin_pages/add_price.html', {'current_price': current_price})


    #  404 view\
def page_404(request, exception):
    return render(request, '404.html', status=404)

from django.http import JsonResponse
from .models import ChatMessage
import json


@csrf_exempt
def save_chat_message(request):
    print("✅ save_chat_message view called")  # DEBUG LINE

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("📦 Received data:", data)  # DEBUG LINE

            name = data.get('name')
            phone = data.get('phone')
            email = data.get('email')
            message = data.get('message')

            if not all([name, phone, email, message]):
                print("❌ Missing field(s)")  # DEBUG LINE
                return JsonResponse({'status': 'error', 'message': 'All fields are required'}, status=400)

            chat = ChatMessage.objects.create(
                name=name,
                phone=phone,
                email=email,
                message=message
            )

            print("✅ Saved to DB:", chat)  # DEBUG LINE
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print("🔥 Error occurred:", e)  # DEBUG LINE
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required(login_url='user_login')
def view_chatbot_messages(request):
    chats = ChatMessage.objects.all().order_by('-created_at')
    return render(request, 'admin_pages/view_chatbot_messages.html', {'chats': chats})
@login_required(login_url='user_login')
def delete_chatbot_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id)
    message.delete()
    return redirect('view_chatbot_messages')


# Add guest
@login_required(login_url='user_login')
def add_guest(request):
    if request.method == "POST":
        form = GuestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # messages.success(request, "Guest added successfully.")
            return redirect('view_guests')
    else:
        form = GuestForm()
    return render(request, "admin_pages/add_guests.html", {"form": form})

# View guests
@login_required(login_url='user_login')
def view_guests(request):
    guests = Guest.objects.all().order_by('-created_date')
    return render(request, "admin_pages/view_guests.html", {"guests": guests})

# Update guest
@login_required(login_url='user_login')
def update_guest(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    if request.method == "POST":
        form = GuestForm(request.POST, request.FILES, instance=guest)
        if form.is_valid():
            form.save()
            # messages.success(request, "Guest updated successfully.")
            return redirect('view_guests')
    else:
        form = GuestForm(instance=guest)
    return render(request, "admin_pages/update_guests.html", {"form": form, "guest": guest})

# Delete guest
@login_required(login_url='user_login')
def delete_guest(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    guest.delete()
    messages.success(request, "Guest deleted successfully.")
    return redirect('view_guests')

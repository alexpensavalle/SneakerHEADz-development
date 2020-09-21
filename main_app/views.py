from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Sneaker, Photo
import uuid
import boto3
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'catcollector-sei-9-cl'

# Create your views here.
def home(request):
  return render(request, 'base.html')

def about(request):
  return render(request, 'about.html')

# This ListView is for later implementation of seeing an all users sneakers index **
class SneakerList(ListView):
  model = Sneaker

class SneakerCreate(LoginRequiredMixin, CreateView):
  model = Sneaker
  fields = ['name', 'style', 'colorway', 'price', 'release', 'condition', 'brand']
  def form_valid(self, form):
    form.instance.user = self.request.user  
    return super().form_valid(form)

class SneakerUpdate(LoginRequiredMixin, UpdateView):
  model = Sneaker
  fields = ['name', 'style', 'colorway', 'price', 'release', 'condition', 'brand']

class SneakerDelete(LoginRequiredMixin, DeleteView):
  model = Sneaker
  success_url = '/sneakers/'

@login_required
def sneakers_index(request): ########################################
  sneakers = Sneaker.objects.filter(user=request.user)
  return render(request, 'sneakers/index.html', { 'sneakers': sneakers })

@login_required
def sneakers_detail(request, sneaker_id):
  sneaker = Sneaker.objects.get(id=sneaker_id)
  return render(request, 'sneakers/detail.html', { 'sneaker': sneaker })

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def add_photo(request, sneaker_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            Photo.objects.create(url=url, sneaker_id=sneaker_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', sneaker_id=sneaker_id)
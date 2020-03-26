
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Game, Collection, Photo
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = '8bitarchive'

class CollectionCreate(LoginRequiredMixin, CreateView):
    model = Collection
    fields = ['title']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CollectionUpdate(LoginRequiredMixin, UpdateView):
  model = Collection
  fields = ['title']

class CollectionDelete(LoginRequiredMixin, DeleteView):
  model = Collection
  success_url = '/collections/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def collections_index(request):
    collections = Collection.objects.filter(user=request.user)
    return render(request, 'collections/index.html', {'collections': collections})

@login_required
def collections_detail(request, collection_id):
  collection = Collection.objects.get(id = collection_id)
  games_collection_doesnt_have = Game.objects.exclude(id__in= collection.games.all().values_list('id'))
  return render(request, 'collections/detail.html', {
    'collection': collection, 
    'games': games_collection_doesnt_have
    })

@login_required
def add_photo(request, game_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, game_id=game_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('games_detail', pk=game_id)

@login_required
def assoc_game(request,collection_id, game_id):
  Collection.objects.get(id=collection_id).games.add(game_id)
  return redirect('detail', collection_id=collection_id)

@login_required
def unassoc_game(request, collection_id, game_id):
  Collection.objects.get(id=collection_id).games.remove(game_id)
  return redirect('detail',collection_id=collection_id)

class GameList(LoginRequiredMixin, ListView):
  model = Game

class GameDetail(LoginRequiredMixin, DetailView):
  model = Game

class GameCreate(LoginRequiredMixin, CreateView):
  model = Game
  fields = ['title', 'platform', 'year', 'genre', 'esrb', 'publisher']

  def form_valid(self,form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class GameUpdate(LoginRequiredMixin, UpdateView):
  model = Game
  fields = ['title', 'platform', 'year', 'genre', 'esrb', 'publisher']

class GameDelete(LoginRequiredMixin, DeleteView):
  model = Game
  success_url = '/games/'

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

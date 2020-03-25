
# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Game, Collection
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
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
def assoc_game(request,collection_id, game_id):
  Collection.objects.get(id=collection_id).games.add(game_id)
  return redirect('detail', collection_id=collection_id)

@login_required
def unassoc_game(request, collection_id, game_id):
  Collection.objects.get(id=collection_id).games.remove(game_id)
  return redirect('detail',collection_id=collection_id)

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

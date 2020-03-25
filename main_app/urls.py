from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('collections/', views.collections_index, name='index'),
    path('accounts/signup', views.signup, name='signup'),
    path('collections/create/', views.CollectionCreate.as_view(), name='collections_create'),
    path('collections/<int:pk>/update', views.CollectionUpdate.as_view(), name="collections_update"),
    path('collections/<int:pk>/delete', views.CollectionDelete.as_view(), name="collections_delete"),
    path('collections/<int:collection_id>/', views.collections_detail, name='detail'),
    # path(' collections/<int:collection_id>/assoc_game/<int:game_id>/', views.assoc_game, name='assoc_game'),
    # path(' collections/<int:collection_id>/unassoc_game/<int:game_id>/', views.unassoc_game, name='unassoc_game'),
]

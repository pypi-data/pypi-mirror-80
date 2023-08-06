from django.views import generic

from .models import PicturePost
# Create your views here.

class PhotoIndexView(generic.ListView):
    model = PicturePost
    template_name = 'photogallery/index.html'
    context_object_name = 'pictures_list'
    ordering = ['-pub_date']
    paginate_by = 8

class PhotoDetailView(generic.DetailView):
    model = PicturePost
    template_name = 'photogallery/detail.html'
    context_object_name = 'picture'

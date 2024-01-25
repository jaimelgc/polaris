from django.shortcuts import render
from pydub import AudioSegment
from pydub.playback import play

from .models import Product


def home(request):
    products = Product.objects.all()
    return render(request, 'guest/home.html', {'products': products})

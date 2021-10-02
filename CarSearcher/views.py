from django.shortcuts import render, HttpResponse, redirect
from . import scrape
from .models import Car


# Create your views here.
def index(request):
    return render(request,'main_page.html')

def search(request):
    carNameSearched = request.POST.get('carName')
    scrape.main(carNameSearched)
    car = Car.objects.all()
    response = {'cars':car}
    return render(request,'car_show.html',response)

def delete(request):
    cars = Car.objects.all()
    for car in cars:
        car.delete()
    return HttpResponse(f'<h1>All cars were deleted</h1>')
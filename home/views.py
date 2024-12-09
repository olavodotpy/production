from django.shortcuts import render

# Create your views here.

def home_view(request):
    context = {'message': 'teste blablabla'}
    return render(request, "home.html", context)

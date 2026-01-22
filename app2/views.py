from django.shortcuts import render

def bloch_sphere(request):
    return render(request, 'bloch_sphere.html')
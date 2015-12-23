from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
def SiteContent(request):
	return render(request, 'SiteContent/index.html')

def Workshops(request):
	return render(request, 'SiteContent/Workshops.html')

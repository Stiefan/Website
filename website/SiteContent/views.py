from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
def SiteContent(request):
	return render(request, 'SiteContent/index.html')

def About(request):
	return render(request, 'SiteContent/About.html')

def Contact(request):
	return render(request, 'SiteContent/contact.html')
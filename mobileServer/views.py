from django.shortcuts import render, render_to_response

# Create your views here.
def index(request):
    page = render(request, "index.html", {})
    return page
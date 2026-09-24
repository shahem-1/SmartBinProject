from django.shortcuts import render

def main_page(request):
    return render(request, 'bins/MainPage.html')

def dashboard_view(request):
    return render(request, 'bins/dashboard.html')

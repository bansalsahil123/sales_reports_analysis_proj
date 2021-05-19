from django.shortcuts import render
from .models import Profile


from django.contrib.auth.decorators import login_required

@login_required
def my_profile_view(request):
    
    return render(request, 'profiles/main.html', context)
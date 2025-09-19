from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Petition
from .forms import PetitionForm

def petition_list(request):
    petitions = Petition.objects.all().order_by('-created_at')
    return render(request, 'petitions/petition_list.html', {'petitions': petitions})

@login_required
def create_petition(request):
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            return redirect('petitions:petition_list')
    else:
        form = PetitionForm()
    return render(request, 'petitions/create_petition.html', {'form': form})

@login_required
def vote(request, petition_id):
    petition = Petition.objects.get(pk=petition_id)
    if request.user in petition.votes.all():
        petition.votes.remove(request.user)
    else:
        petition.votes.add(request.user)
    return redirect('petitions:petition_list')

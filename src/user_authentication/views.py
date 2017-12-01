from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .models import (UserContact, UserEducation,
					 UserEducationTypes, Colleges,
					 Faculties, Departments, Cities )
from .forms import SignUpForm
# Create your views here.
User = get_user_model()


class UserListView(LoginRequiredMixin, ListView):
	queryset 	  = User.objects.all()
	template_name = 'userlist.html'

class UserDetailView(LoginRequiredMixin, DetailView):
	
	def get_queryset(self):
		slug = self.kwargs.get('slug')
		if slug:
			queryset = User.objects.filter(slug=slug)
		else:
			queryset = None
		print("QuerySet: ", queryset)
		return queryset

class AuthorDetailView(DetailView):
	template_name = 'author_detail.html'

	def get_object(self):
		username = self.kwargs.get("username")
		if username is None or username == '':
			raise Http404
		return get_object_or_404(User, username__iexact=username, is_active=True)


def delete_user(request, id):
    user = get_object_or_404(User, pk=id)
    user.delete()  ##Ultimately vulnarable to CSRF
    print('Deleted!')
    return HttpResponseRedirect('/userlist/')


def signup(request):
	if not request.user.is_authenticated:
		
	    if request.method == 'POST':
	        form = SignUpForm(request.POST, request.FILES)
	        if form.is_valid():
	            form.save()
	            username = form.cleaned_data.get('username')
	            raw_password = form.cleaned_data.get('password1')
	            user = authenticate(username=username, password=raw_password)
	            login(request, user)
	            return HttpResponseRedirect('/')
	    else:
	        form = SignUpForm()
	    return render(request, 'registration/signup.html', {'form': form})
	else:
		return render(request, 'registration/dont_signup.html', {})
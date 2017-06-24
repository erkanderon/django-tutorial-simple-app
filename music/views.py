from django.views import generic
from .models import Album
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import View
from .models import Album
from .forms import UserForm 




class IndexView(generic.ListView):
	template_name = "music/index2.html"
	context_object_name = 'all_albums'

	def get_queryset(self):
		return Album.objects.all()



class DetailView(generic.DetailView):
	model = Album
	template_name = "music/detail2.html"


class AlbumCreate(CreateView):
	model = Album
	fields = ['artist','album_title','genre','album_logo']


class AlbumUpdate(UpdateView):
	model = Album
	fields = ['artist','album_title','genre','album_logo']

class AlbumDelete(DeleteView):
	model = Album
	success_url = reverse_lazy('music:index')


class UserFormView(View):
	form_class = UserForm
	template_name = "music/registration_form.html"


	# display blank form
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	# process form data
	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():

			user = form.save(commit = False)

			# cleaned normalized data (Date field ex)

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user.set_password(password)
			user.save()

			# returns User object if the credentials are true

			user = authenticate(username=username, password = password)

			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('music:index')

		return render(request, self.template_name, {'form': form})

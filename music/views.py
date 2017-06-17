from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404

from .models import Album, Song

# Create your views here.

def index(request):
	all_albums = Album.objects.all()

	return render(request, 'music/index.html', {'all_albums': all_albums,})



def detail(request, album_id):
	album = get_object_or_404(Album, pk=album_id)

	return render(request, 'music/details.html', {'album': album})


def favorite(request, album_id):
	album = get_object_or_404(Album, pk=album_id)

	try:
		selected_song = album.song_set.get(pk = request.POST['song'])

	except(KeyError, Song.DoesNotExist):
		return render(request, 'music/details.html', { 'album': album, 'error_message': "You didnt select any song"})

	else:
		if selected_song.is_favourite:
			selected_song.is_favourite = False
		else:
			selected_song.is_favourite = True
		selected_song.save()
		return render(request, 'music/details.html', {'album': album})

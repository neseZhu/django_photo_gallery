from django.http import HttpResponse

def main(request):
	return HttpResponse('<h1>Gallery</h1>')
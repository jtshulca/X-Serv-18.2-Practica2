from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from acorta.models import Urls
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def show(request):
    lista_urls = Urls.objects.all();
    if request.method == 'GET':
        if Urls.objects.all().exists():
            respuesta = "<h3>Aplicación web simple para acortar URLs</h3>"
            for URL in lista_urls:
                respuesta += "<li>/" + str(URL.id) + " --> " + URL.URL_larga
        else:	
            respuesta = "<h3>No hay URLs acortadas</h3></br>"
            
        respuesta += "<form action='' method='POST'>"
        respuesta += "URL a acortar <input type='text' name='url_larga'>"
        respuesta += "<input type='submit' value='Acortar'></form>"

    elif request.method == 'POST':
        URL_larga = request.POST['url_larga']
        if URL_larga == "":
            respuesta = "<p><h4>¡No has introducido ninguna página!<h4></p>"
            respuesta += "<a href='http://localhost:1234'>Pulse aqui para volver la aplicación</a>"
            return HttpResponseBadRequest(respuesta)
            
        elif not URL_larga.startswith("http://") and not URL_larga.startswith("https://"):
            URL_larga = "http://" + URL_larga
        try:
            nueva_url = Urls.objects.get(URL_larga = URL_larga)
            respuesta = "Ya has añadido esa URL anteriormente"
            respuesta += "<p>URL acortada: <a href='" + nueva_url.URL_larga + "'>" + str(nueva_url.id) + "</a>"
            respuesta += " --> " + "<a href='" + nueva_url.URL_larga + "'>" + nueva_url.URL_larga + "</a></p>"
            respuesta += "<a href=''>Pulse aqui para volver a la aplicación</a>"
            return HttpResponse(respuesta)
            
        except Urls.DoesNotExist:
            nueva_url = Urls(URL_larga = URL_larga)
            nueva_url.save()
        respuesta = ("<p>URL acortada: <a href='" + nueva_url.URL_larga + "'>" + str(nueva_url.id) + "</a>" +
                     " --> " + "<a href='" + nueva_url.URL_larga + "'>" + nueva_url.URL_larga + "</a></p>")
        respuesta += "<a href=''>Pulse aqui para volver a la aplicación</a>"
		
    return HttpResponse(respuesta)

def redireccion(request, URL_corta):
    try:
        URL_larga = Urls.objects.get(id = URL_corta).URL_larga
        return HttpResponseRedirect(URL_larga)
        
    except Urls.DoesNotExist:
        respuesta = "<p>Esa URL no esta disponible</p>"
        respuesta += "<a href='http://localhost:1234'>Pulse aqui para volver la aplicación</a>"
        return HttpResponse(respuesta)
        
def NotFoundErr(request):
    return HttpResponse('<h1>!Algo has hecho mal¡<h1>')

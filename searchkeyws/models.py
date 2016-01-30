from django.db import models


class WSRequest(models.Model):
    id_proyecto = models.IntegerField()
    nombre_directorio = models.CharField(max_length=50)


class WSResponse(models.Model):
    id_proyecto = models.IntegerField()


class WSFilteredUrlsRequest(models.Model):
    id_proyecto = models.IntegerField()
    nombre_directorio = models.CharField(max_length=50)


class SearchKey(models.Model):
    clave = models.CharField(max_length=512)
    request = models.ForeignKey(WSRequest, on_delete=models.CASCADE, related_name='claves')


class SearchResult(models.Model):
    buscador = models.CharField(max_length=30)
    response = models.ForeignKey(WSResponse, on_delete=models.CASCADE, related_name='buscadores')


class SearchUrl(models.Model):
    url = models.CharField(max_length=255)
    searchresult = models.ForeignKey(SearchResult, on_delete=models.CASCADE, related_name='urls')


class FilteredUrl(models.Model):
    orden = models.IntegerField()
    url = models.CharField(max_length=255)
    request = models.ForeignKey(WSFilteredUrlsRequest, on_delete=models.CASCADE, related_name='urls')

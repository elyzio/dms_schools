from django.http import JsonResponse

from .models import Subdistrito, Suco, Aldeia


def ajax_load_subdistritos(request):
    distrito_id = request.GET.get('distrito_id')
    subdistritos = Subdistrito.objects.filter(distrito_id=distrito_id) if distrito_id else Subdistrito.objects.none()
    return JsonResponse(list(subdistritos.order_by('subdistrito').values('id', 'subdistrito')), safe=False)


def ajax_load_sucos(request):
    subdistrito_id = request.GET.get('subdistrito_id')
    sucos = Suco.objects.filter(subdistrito_id=subdistrito_id) if subdistrito_id else Suco.objects.none()
    return JsonResponse(list(sucos.order_by('suco').values('id', 'suco')), safe=False)


def ajax_load_aldeias(request):
    suco_id = request.GET.get('suco_id')
    aldeias = Aldeia.objects.filter(suco_id=suco_id) if suco_id else Aldeia.objects.none()
    return JsonResponse(list(aldeias.order_by('aldeia').values('id', 'aldeia')), safe=False)

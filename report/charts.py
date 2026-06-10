from django.db.models import Count
from estudante.models import Estudante
from funcionario.models import Professor


def get_students_by_sex():
    qs = Estudante.objects.filter(is_active=True, is_delete=False)
    mane = qs.filter(sexu='M').count()
    feto = qs.filter(sexu='F').count()
    return {
        'labels': ['Mane', 'Feto'],
        'data': [mane, feto],
        'colors': ['#36A2EB', '#FF6384'],
    }


def get_teachers_by_sex():
    qs = Professor.objects.filter(is_active=True, is_delete=False)
    mane = qs.filter(sexu='M').count()
    feto = qs.filter(sexu='F').count()
    return {
        'labels': ['Mane', 'Feto'],
        'data': [mane, feto],
        'colors': ['#36A2EB', '#FF6384'],
    }


def get_students_by_status():
    qs = Estudante.objects.filter(is_delete=False)
    aktivo = qs.filter(is_active=True).count()
    transfer = qs.filter(is_transfer=True).count()
    alumni = qs.filter(is_alumni=True).count()
    inativo = qs.filter(is_active=False, is_transfer=False, is_alumni=False).count()
    return {
        'labels': ['Ativo', 'Transfer', 'Alumni', 'Inativo'],
        'data': [aktivo, transfer, alumni, inativo],
        'colors': ['#4CAF50', '#FFC107', '#9C27B0', '#F44336'],
    }


def get_teachers_by_estadu():
    _labels = {
        'KONTRATADU': 'Kontratadu',
        'PERMANENTE': 'Permanente',
        'VOLUNTARIU': 'Voluntariu',
        'PARCIAL': 'Parcial',
    }
    _colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
    qs = Professor.objects.filter(is_active=True, is_delete=False)
    data = qs.values('estadu').annotate(total=Count('id')).order_by('estadu')
    labels = [_labels.get(d['estadu'], d['estadu']) for d in data]
    counts = [d['total'] for d in data]
    return {
        'labels': labels,
        'data': counts,
        'colors': _colors[: len(labels)],
    }


def get_teachers_by_nivel():
    _labels = {
        'D1': 'D1', 'D2': 'D2', 'D3': 'D3',
        'S1': 'S1/Lisensiadur',
        'S2': 'S2/Masteradu',
        'S3': 'S3/Doutoramentu',
        'Outru': 'Outru',
    }
    _colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF']
    qs = Professor.objects.filter(is_active=True, is_delete=False)
    data = qs.values('nivel_akademiku').annotate(total=Count('id')).order_by('-total')
    labels = [_labels.get(d['nivel_akademiku'], d['nivel_akademiku']) for d in data]
    counts = [d['total'] for d in data]
    return {
        'labels': labels,
        'data': counts,
        'colors': _colors[: len(labels)],
    }


def get_students_by_district_chart():
    qs = Estudante.objects.filter(is_active=True, is_delete=False)
    data = qs.values('distrito__distrito').annotate(total=Count('id')).order_by('-total')
    labels = [d['distrito__distrito'] or 'N/A' for d in data]
    counts = [d['total'] for d in data]
    return {'labels': labels, 'data': counts}

from django.db.models import Count
from estudante.models import Estudante, EstudanteClasse
from funcionario.models import Professor
from custom.models import Ano


def get_students_by_district_table():
    qs = Estudante.objects.filter(is_active=True, is_delete=False)
    data = (
        qs.values('distrito__id', 'distrito__distrito')
        .annotate(total=Count('id'))
        .order_by('distrito__distrito')
    )
    return list(data)


def get_students_by_classe_turma_table():
    try:
        ano_aktivo = Ano.objects.get(is_active=True)
    except Ano.DoesNotExist:
        return []

    rows = (
        EstudanteClasse.objects
        .filter(ano=ano_aktivo, estudante__is_delete=False, estudante__is_active=True)
        .values('classe__id', 'classe__classe', 'turma__id', 'turma__turma', 'departamentu__departamento')
        .annotate(total=Count('id'))
        .order_by('classe__classe', 'turma__turma')
    )

    classes = {}
    for row in rows:
        cid = row['classe__id']
        if cid not in classes:
            classes[cid] = {
                'classe': row['classe__classe'],
                'classe_id': cid,
                'departamentu': row['departamentu__departamento'],
                'turmas': [],
                'class_total': 0,
            }
        classes[cid]['turmas'].append({
            'turma': row['turma__turma'],
            'turma_id': row['turma__id'],
            'classe_id': cid,
            'total': row['total'],
        })
        classes[cid]['class_total'] += row['total']

    return list(classes.values())


def get_teachers_by_posisaun_table():
    _labels = {
        'DIRETOR': 'Diretor/a',
        'DIRETOR_ADJUNTO': 'Diretor Adjunto',
        'GAT': 'GAT',
        'PROFESSOR': 'Professor/a',
        'TECNICO_ADMINISTRAÇÃO': 'Tecnico Administrasaun',
        'APOIA_ADMINISTRAÇÃO': 'Apoia Administrasaun',
        'GURDA_ESCOLA': 'Guarda Eskola',
        'TECNICO_AGUA_SANEAMENTO': 'Tecnico Bee no Saneamentu',
        'JARDINHEIRA': 'Jardinheira',
    }
    qs = Professor.objects.filter(is_active=True, is_delete=False)
    data = qs.values('posisaun_prof').annotate(total=Count('id')).order_by('-total')
    return [
        {
            'posisaun': _labels.get(d['posisaun_prof'], d['posisaun_prof'] or 'N/A'),
            'posisaun_val': d['posisaun_prof'] or '',
            'total': d['total'],
        }
        for d in data
    ]


def get_teachers_by_estadu_table():
    _labels = {
        'KONTRATADU': 'Kontratadu',
        'PERMANENTE': 'Permanente',
        'VOLUNTARIU': 'Voluntariu',
        'PARCIAL': 'Parcial',
    }
    qs = Professor.objects.filter(is_active=True, is_delete=False)
    data = qs.values('estadu').annotate(total=Count('id')).order_by('estadu')
    rows = [
        {
            'estadu': _labels.get(d['estadu'], d['estadu']),
            'estadu_val': d['estadu'],
            'total': d['total'],
        }
        for d in data
    ]
    grand_total = sum(r['total'] for r in rows)
    return rows, grand_total

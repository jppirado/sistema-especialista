import json
import random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *

# Create your views here.

# https://www.kaggle.com/datasets/jatinthakur706/most-watched-netflix-original-shows-tv-time?resource=download


class DeterminaValoresSistemaEspecialista:

    def __init__(self, longos, classificacao, genero):
        self.longos = longos
        self.classificacao = classificacao
        self.genero = genero
        self.films = Film.objects.all()

    def filtra_por_tamanho(self):
        sets = []
        for item in self.films:
            if self.longos == 'nao':
                if int(item.duration) < 30:
                    sets.append(item)
            else:
                if int(item.duration) > 30:
                    sets.append(item)
        self.films = sets

    def filtra_por_idade(self):
        qr = []
        for item in self.films:

            if int(item.classification) == int(self.classificacao):
                qr.append(item)

        self.films = qr

    def filtra_por_genero(self):

        qrr = []

        for item in self.films:
            if self.genero.id in [genre.id for genre in item.genre.all()]:
                qrr.append(item)

        self.films = qrr

    def call(self):
        self.filtra_por_tamanho()
        self.filtra_por_idade()

        return self.films


class DeviceViewResults(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):

        return self.render_to_response(kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        data = json.loads(request.body.decode('utf-8'))
        tamanho = data.get('tamnho')
        idade = data.get('classificacao')
        genero = data.get('genero')

        resultado  = DeterminaValoresSistemaEspecialista(
            classificacao=idade,
            genero=genero,
            longos=tamanho,
        ).call()
        filmes_serializados = []
        filmes_sorteados = random.sample(resultado, min(3, len(resultado)))
        for filme in filmes_sorteados:  # Apenas os três primeiros filmes
            filme_serializado = {
                'name': filme.name,
                'classification': filme.classification,
                'duration': filme.duration,
                # Adicione outros atributos do modelo Filme, se necessário
            }
            filmes_serializados.append(filme_serializado)

        # Retornar os filmes serializados como uma resposta JSON
        return JsonResponse(filmes_serializados, safe=False)
        

    def serialize_questions(self):

        return 'dasdsad'


# Desabilita a proteção CSRF para esta view (somente para fins de demonstração)
@csrf_exempt
def seleciona_genero(request):
    if request.method == 'POST':

        data = json.loads(request.body.decode('utf-8'))

        # Acesse os dados específicos (tamanho e classificação)

        tamanho = data.get('tamnho')  # se for false ele é epsódio curto
        classificacao = data.get('classificacao')

    # Filtro de duração
        if tamanho == 'false':
            filmes = Film.objects.filter(duration__gt=30)
        else:
            filmes = Film.objects.filter(duration__lte=30)
        
        # Filtro de classificação
        
        if classificacao != 'false':
            filmes = filmes.filter(classification=classificacao)

        # Extrair valores de gênero dos filmes
            
        print( filmes )
        generos = []
        for filme in filmes:
            for genero in filme.genre.all():
                generos.append(genero.name)

        # Remover duplicatas (opcional)
        generos = list(set(generos))

    # Retorne uma resposta JSON com os gêneros filtrados
        return JsonResponse(generos, safe=False)

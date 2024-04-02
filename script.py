 # Importe o modelo Film do seu aplicativo Django
import os
import django

# Configure as configurações do Django antes de importar os modelos
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()


import csv
from app.models import * 

from app.models import Film, Genre

def create_films_from_csv(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['lister-item-header']
            classification = row['certificate']
            duration = float(row['runtime'].split()[0].replace(',', '.'))  # Extrair apenas o número de minutos
            genre_names = [genre.strip() for genre in row['genre'].split(',')]
            
            # Criar uma instância do modelo Film e salvar no banco de dados
            film = Film.objects.create(name=name, classification=classification, duration=duration)
            
            # Adicionar os gêneros ao filme
            for genre_name in genre_names:
                genre_instance, _ = Genre.objects.get_or_create(name=genre_name)
                film.genre.add(genre_instance)

# Substitua 'imdb.csv' pelo caminho real do seu arquivo CSV
create_films_from_csv('imdb.csv')

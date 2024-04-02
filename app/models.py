from django.db import models

# Create your models here.


class FilmCase( models.Model ):


    book_name = models.CharField(max_length=10)


    def __str__(self):
        return self.book_name 
    

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Film(models.Model):
    
    name = models.CharField(max_length=255)
    classification = models.CharField(max_length=10)
    duration = models.IntegerField()
    genre = models.ManyToManyField('Genre', related_name='films')

    def __str__(self):
        return self.name
    

    def get_all_generos( self ):

        for i in self.genre.all():
            print(i)

        return self.genre.all()

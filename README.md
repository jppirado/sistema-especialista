requisitos  python 3.12 


1-criar uma maquina virtual 

python -m venv venv

2-ativar o ambiente virtual 

python venv/Scripts\Activate.ps1

3-instalar os pacotes

pip install -r requirements.txt


4- ajustar arquivos do banco de dados em:

main.settings.DATABASES 

5-migrar 
python manage.py migrate 

6-popula base de dados

python script.py 

Requisitos del sistema:
Windows 10 64bits
Python 3.11.5 o superior

# 1 Instalar Python

# 2 Instalar virtualenv desde un cmd
pip install virtualenv

# 3 Crear un entorno virtual para intalar las librerias necesarias
virtualenv env_dispositivos

# 4 Activar el entorno virtual
.\env_dispositivos\Scripts\activate

# 5 Instalar los paquetes dentro del entorno virtual
pip install -r requirements.txt

# 6 Crear Base de datos
python manage.py migrate

# 7 Correr sistema
python manage.py runserver

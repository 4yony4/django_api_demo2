# Usa una imagen base de Python (por ejemplo, Python 3.9 slim)
FROM python:3.9-slim

# Evita que Python genere archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Evita que Python realice buffering en la salida
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /code

# Copia el archivo de requerimientos y actualiza pip
COPY requirements.txt /code/
RUN pip install --upgrade pip

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el resto de la aplicación al directorio de trabajo
COPY . /code/

# Expone el puerto 8000 (puedes cambiarlo si usas otro)
EXPOSE 8000

# Comando para ejecutar el servidor usando Gunicorn
CMD ["gunicorn", "apiserver.wsgi:application", "--bind", "0.0.0.0:8000"]
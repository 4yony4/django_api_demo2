
# Guía para Dockerizar tu Servidor Django

Aquí tienes una guía paso a paso para dockerizar tu servidor Django. Vamos a crear un Dockerfile, un archivo de docker-compose (opcional pero recomendado) y explicar los pasos para construir y ejecutar el contenedor.

## 1. Crear el archivo requirements.txt

En la raíz de tu proyecto, crea un archivo llamado `requirements.txt` que contenga todas las dependencias necesarias. Por ejemplo:

```
Django>=3.2
djangorestframework
gunicorn
openai
python-dotenv
```

Asegúrate de que estos paquetes sean los que usas en tu proyecto.

## 2. Crear el archivo Dockerfile

En la raíz del proyecto, crea un archivo llamado `Dockerfile` (sin extensión) con el siguiente contenido:

```dockerfile
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
```

**Notas:**
- Se asume que tu archivo WSGI se encuentra en `apiserver/wsgi.py`. Si tu proyecto tiene otro nombre o estructura, ajústalo en consecuencia.
- Usamos Gunicorn como servidor de producción dentro del contenedor.

## 3. (Opcional) Crear el archivo docker-compose.yml

Si deseas facilitar la gestión (por ejemplo, para levantar otros servicios o montar volúmenes) puedes crear un archivo `docker-compose.yml` en la raíz:

```yaml
version: "3.9"

services:
  web:
    build: .
    command: gunicorn apiserver.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    env_file:
      - .env
```

**Detalles:**
- La opción `volumes` monta el directorio actual en el contenedor para facilitar el desarrollo. En producción, puedes omitirlo.
- La opción `env_file` carga variables de entorno desde el archivo `.env`, donde puedes incluir la variable `OPENAI_API_KEY` y otras configuraciones.

## 4. Construir la imagen Docker

Desde la raíz del proyecto, ejecuta el siguiente comando para construir la imagen:

```bash
docker build -t my-django-app .
```

Donde `my-django-app` es el nombre que le darás a la imagen.

## 5. Ejecutar el contenedor

### Opción 1: Usando Docker

Una vez construida la imagen, ejecuta el contenedor:

```bash
docker run -d -p 8000:8000 --name django_app my-django-app
```

- `-d` ejecuta el contenedor en segundo plano.
- `-p 8000:8000` mapea el puerto 8000 del contenedor al puerto 8000 de tu máquina.
- `--name django_app` asigna un nombre al contenedor.

### Opción 2: Usando Docker Compose

Si creaste el archivo `docker-compose.yml`, simplemente ejecuta:

```bash
docker-compose up -d
```

Este comando construirá la imagen (si es necesario) y levantará el contenedor.

## 6. Verificar que el servidor esté funcionando

Abre tu navegador o utiliza `curl` para acceder a:

```
http://localhost:8000/
```

Deberías ver tu aplicación Django corriendo en el contenedor.

## 7. Consideraciones adicionales

- **Migraciones:**
  Cuando levantes el contenedor, es posible que necesites ejecutar las migraciones de Django. Puedes hacerlo ejecutando un comando dentro del contenedor:

  ```bash
  docker exec -it django_app python manage.py migrate
  ```

  (Si usas Docker Compose, el nombre del servicio es `web` y podrías ejecutar: `docker-compose exec web python manage.py migrate`).

- **Archivos estáticos:**
  Si usas archivos estáticos en producción, asegúrate de configurarlos adecuadamente (por ejemplo, usando `collectstatic` y sirviéndolos con NGINX u otro servidor).

- **Variables de entorno:**
  Puedes crear un archivo `.env` en la raíz del proyecto con las variables que necesites (por ejemplo, `OPENAI_API_KEY` y cualquier otra configuración).

Con estos pasos tendrás tu servidor Django dockerizado y listo para correr en cualquier entorno que soporte Docker. ¡Éxito en tu despliegue!

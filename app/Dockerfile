# Usamos la imagen oficial de Python 3.9 como base
FROM python:3.9

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos los archivos de la aplicación al contenedor
COPY . /app

# Instalamos las dependencias del proyecto
RUN pip install -r requirements.txt

EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
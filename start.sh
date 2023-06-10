#!/bin/bash

# Activa el entorno virtual si lo estás utilizando
# source path/to/virtualenv/bin/activate

# Establece el valor de $PORT si no está configurado
if [[ -z "$PORT" ]]; then
  export PORT=8000
fi

# Inicia la aplicación con Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker your_app_module:app -b 0.0.0.0:$PORT


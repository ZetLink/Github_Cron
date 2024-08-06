# Github Cron

Este programa esta pensado para automatizar la monitorización y gestión de commits en repositorios de GitHub a través de un contenedor Docker.


## Instalacion

Instala un contenedor Docker con el script:

```bash
  ./setup.sh
```

Tambien puede usarlo sin Docker, modificando el archivo de configuracion de cron:

```bash
  crontab -e
```

Luego, añade la siguiente linea

```bash
  0 23 * * * /usr/bin/python3 /ruta/al/script.py
```

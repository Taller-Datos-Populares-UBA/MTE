# MTE
Colaboración con la cooperativa Amanecer de los Cartoneros.  
<img src="assets/logo_negro.png" alt="alt text" width="300">

# Instalación
Los pasos principales son:
1. Instalar Python >= 3.9
2. Bajar el proyecto desde este repositorio de GitHub.
3. Instalar las librerías necesarias (recomendamos usar un entorno virtual)
4. Correr con python el archivo `index.py`, eso te va a hostear la página en tu compu y te va a dar una ip para acceder desde el navegador.

En más detalle sobre cada uno:
1. Podés instalarlo desde [la página oficial](https://www.python.org/downloads/), o si usás algún gestor de paquetes seguro lo tengan. Tildar la opción de agregarlo al PATH si usás la instalación oficial en Windows.
2. Podés bajarte el zip o mejor clonarlo/forkearlo si tenés [git](https://git-scm.com/downloads) instalado.  
Ejemplo:  
    `git clone https://github.com/Taller-Datos-Populares-UBA/MTE`
3. Acá tenés que usar `pip` (el package manager de python) para instalar las librerías en sus correspondientes versiones indicadas en el archivo `requirements.txt`. Idealmente sugiero armarse un entorno virtual: usando la librería que trae python venv se hace fácil yendo por consola a donde querés tener el proyecto y correr `python venv venv` (el segundo "venv" es el nombre que le quieras dar al entorno) y después activarlo (en Windows es con el `activate` haciendo `.\venv\Scripts\activate` y en Mac/Linux `source ./venv/bin/activate`. Después ya sea con el entorno o no, hacés `python -m pip install -r requirements.txt` estando en el directorio del proyecto y te levanta e instala las librerías y dependencias.
4. Desde la consola:  
    `python ./index.py`.  
Si quisieras usar una ip en particular se puede especificar:  
    `python ./index.py --host X.X.X.X`  

Aclaración: dependiendo del sistema operativo y cómo hayas instalado Python, la palabra para llamarlo desde consola puede ser `py` (Windows) o `python3`, `python3.9` o algo similar en Mac/Linux.
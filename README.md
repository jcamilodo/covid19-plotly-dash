# Análisis de Mortalidad por COVID-19 en Colombia (2020 - 2021)

Este proyecto consiste en el análisis de los datos de mortalidad por COVID-19 en Colombia durante los años 2020 y 2021, desarrollado en Python con visualizaciones interactivas utilizando las librerías Plotly y Dash. La aplicación web permite explorar distintos aspectos de los datos de mortalidad mediante gráficos y mapas interactivos.

## Tabla de Contenidos
- [Descripción de la Aplicación](#descripción-de-la-aplicación)
- [Instalación](#instalación)
- [Archivos Principales](#archivos-principales)
- [Instrucciones de Uso](#instrucciones-de-uso)
- [Despliegue en la Web](#despliegue-en-la-web)
- [Créditos](#créditos)

## Descripción de la Aplicación

La aplicación proporciona una interfaz interactiva para visualizar el análisis de mortalidad por COVID-19 en Colombia a través de los siguientes componentes:

   - Mapa: Muestra el número total de muertes confirmadas por COVID-19 en cada departamento durante el año 2021.
   - Gráfico de Barras Horizontal: Indica las cinco ciudades con mayor índice de muertes confirmadas por COVID-19 en el año 2021.
   - Gráfico Circular: Representa los casos de COVID-19 reportados como confirmados, sospechosos y descartados en 2021.
   - Gráfico de Línea: Visualiza el total de muertes confirmadas por COVID-19 por mes durante los años 2020 y 2021.
   - Histograma de Frecuencias: Muestra la distribución de las muertes confirmadas por COVID-19 por edades quinquenales en el año 2020.


## Objetivos Principales
* Analizar y visualizar la mortalidad por COVID-19 en Colombia para los años 2020 y 2021: Generar gráficos y mapas interactivos que permitan comprender la distribución y tendencias de las muertes causadas por COVID-19 en Colombia a nivel departamental y por ciudad, destacando los patrones temporales y demográficos.
* Desarrollar una aplicación web interactiva para la exploración de datos: Crear una interfaz de usuario intuitiva mediante Dash y Plotly que permita a los usuarios navegar y visualizar los datos de mortalidad por COVID-19, con diferentes tipos de gráficos y filtros de tiempo, edad y geografía para una experiencia de análisis enriquecida.
* Implementar y desplegar la aplicación en un servidor web accesible: Asegurar que la aplicación esté disponible en línea para que usuarios y analistas puedan accederla desde cualquier dispositivo, permitiendo un acceso fácil y directo a los datos y visualizaciones sobre el impacto de la pandemia en Colombia.

## Instalación

Para instalar las dependencias necesarias, es importante tener Python 3.7 o superior. Puedes instalar `plotly` y `dash` ejecutando:

```bash
python -m venv .venv #crear ambiente virtual
pip install -r requirements.txt #instalar librerias
```

## Archivos Principales

   - `dashboard_app.py:` Archivo principal que contiene el código de la aplicación Dash y las visualizaciones.
   - `utils.py:` Funciones auxiliares para la limpieza, procesamiento y manipulación de los datos.
   - `Carpeta assets:` Contiene imágenes y recursos utilizados en la interfaz de la aplicación, como el logotipo y otros elementos visuales.

## Instrucciones de Uso

- Clona el repositorio del proyecto o descarga los archivos necesarios.
- Instala las dependencias especificadas en la sección de instalación.
- Ejecuta la aplicación con el siguiente comando en el terminal:

```bash
python dashboard_app.py
```

Abre un navegador web y ve a la dirección http://127.0.0.1:8050 o http://localhost:8050 para acceder a la aplicación interactiva.   

Nota

Para personalizar o modificar las visualizaciones, puedes editar el archivo `dashboard_app.py` y ajustar las configuraciones en `utils.py` si es necesario

## Despliegue en la Web

La aplicación está desplegada en un servidor web y accesible a través del siguiente enlace: URL de la aplicación.

## Créditos

Este proyecto fue desarrollado con fines académicos para la materia de APLICACIONES I, de la Maestria en Inteligencia Artificial de la Universidad de La Salle, para el análisis de datos de mortalidad por COVID-19 en Colombia. Utiliza las librerías Plotly y Dash para visualización interactiva.



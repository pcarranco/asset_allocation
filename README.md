# Asset allocation Toolkit
---

## Objetivo

El objetivo de este proyecto es proveer con las herramientas necasarias para poder realizar diferentes
análisis de *"asset classes"* utilizando series de datos históricos que las representen para posteriomente
crear un asset allocation objetivo para una estrategia de inversión.

## ¿Cómo utilizar este proyecto?

El usuario puede crear tareas de optimización utilizando este proyecto, para poder ejecutar la tarea es necesario crear diccionario en python o bien
crear un archivo json con la siguiente estructura:

````python

    tarea = {
        'tipos': {
            # Se pasa como un arreglo de numpy
            'rendimiento': 'rend Esp',
            # Se pasa como un arreglo de numpy
            'riesgo': 'covar',
        },
        'data': {
            'rendimiento': [],
            'volatilidad': [],
            'activos': []
        }
            
    }

````
Una vez generada la tarea se puede utilizar alguna de la funciones de 
generación de curva para poder llevar acabo la tarea.

### Funciones para generar curvas
- generar_curva_portafolio_2_activos()
- generar_curva_portafolio_3_activos()
- generar_curva_montecarlo()

Para poder ocupar cualquiera de estas solo se deben seguir los siguientes pasos:

**generar_curva_portafolio_3_activos**
````python

    import optimport

    tarea = {
        'tipos': {
            # Se pasa como un arreglo de numpy
            'rendimiento': 'rend Esp',
            # Se pasa como un arreglo de numpy
            'riesgo': 'covar',
        },
        'data': {
            'rendimiento': [],
            'volatilidad': [],
            'activos': []
        }
            
    }

    result = optimport.generar_curva_portafolio_3_activos(
        datos=tarea)

````

**generar_curva_montecarlo**
````python

    import optimport

    tarea = {
        'tipos': {
            # Se pasa como un arreglo de numpy
            'rendimiento': 'rend Esp',
            # Se pasa como un arreglo de numpy
            'riesgo': 'covar',
        },
        'data': {
            'rendimiento': [],
            'volatilidad': [],
            'activos': []
        }
            
    }

    result = optimport.generar_curva_montecarlo(
        datos=tarea)

````

### Requisitos
**Crear entorno virtual con anaconda**
````
conda create -n asset_alloc
````



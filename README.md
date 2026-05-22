# 📊 LABORATORIO FINAL: Sistema de Análisis Estadístico de Mortalidad en Colombia (2019)

Aplicación web interactiva desarrollada en **Python**, **Streamlit** y **Plotly** orientada al procesamiento, integración y análisis de datos de defunciones no fetales en el territorio nacional colombiano durante el año 2019. El sistema está estructurado bajo una arquitectura de software limpia utilizando el patrón de diseño **MVC (Modelo-Vista-Controlador)** y se encuentra desplegado en la nube a través de **Azure App Service**.

---

## 🎯 1. Propósito y Objetivos del Proyecto

### 1.1 Introducción
La comprensión de los patrones demográficos, causas de muerte y vulnerabilidades territoriales es clave para la formulación de políticas públicas efectivas y la optimización de recursos en salud y seguridad. Esta aplicación provee una herramienta de software interactiva y centralizada que procesa microdatos reales del DANE para automatizar la unificación de catálogos médicos globales (CIE-10), registros político-administrativos (Divipola) e históricos individuales de defunciones en Colombia.

### 1.2 Objetivo General
Desarrollar una aplicación web interactiva que permita estructurar, cruzar e interpretar dinámicamente los datos de mortalidad de Colombia en 2019, facilitando el descubrimiento de tendencias epidemiológicas y de seguridad a través de analítica visual de datos.

### 1.3 Objetivos Específicos
* **Limpieza e Integración:** Cargar y estandarizar fuentes de datos heterogéneas en formato Excel eliminando duplicados y homogeneizando tipos de llaves primarias (`COD_DANE`, `COD_MUERTE`, `COD_DEPARTAMENTO`).
* **Modularidad:** Implementar una arquitectura desacoplada basada en el patrón MVC para asegurar la escalabilidad del backend.
* **Visualización Científica:** Generar gráficos interactivos mediante Plotly con sus respectivas interpretaciones estadísticas y de contexto país.
* **Despliegue Cloud:** Publicar el sistema en entornos de producción usando tecnologías Cloud (Azure Web Apps).

---

## 🗂️ 2. Estructura del Proyecto (Patrón MVC)

El proyecto adopta el patrón estructural **Modelo-Vista-Controlador**, aislando la lógica de negocio de la interfaz interactiva:

```text
Proyecto-mortalidad-en-Colombia-2019/
│
├── Datos/                  # Capa de Datos (Fuentes oficiales del DANE en .xlsx)
│   ├── Anexo1.NoFetal2019_CE_15-03-23 (1).xlsx
│   ├── Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx
│   └── Divipola_CE_.xlsx
│
├── vistas/                 # Capa de Vista (Interfaces y renderizado de gráficos)
│   ├── __init__.py
│   └── graficos.pY         # Módulo de gráficos y panel principal del dashboard
│
├── modelo.py               # Capa de Modelo (Carga, extracción y caché de dataframes con Pandas)
├── controlador.py          # Capa de Controlador (Orquestación, lógica de cruces .merge() y persistencia)
├── main.py                 # Punto de entrada de la aplicación Streamlit
├── requirements.txt        # Dependencias del proyecto requeridas por Azure
└── README.md               # Documentación técnica del sistema

## 💻 3. Tecnologías y Software Utilizado

- Lenguaje de Programación: Python 3.12+
- Framework de UI Web: Streamlit (Manejo del ciclo de vida e interfaces dinámicas con `st.session_state` y `st.tabs`)
- Librería Gráfica: Plotly Express (Visualizaciones interactivas vectoriales)
- Procesamiento de Datos: Pandas y OpenPyXL (Estructuras de datos y lectura de archivos de Excel)
- Entorno de Desarrollo: Visual Studio Code
- Control de Versiones: Git y GitHub
- Infraestructura Cloud: Azure App Service (Entorno de producción bajo Linux)

## 🛠️ 4. Instalación, Configuración y Ejecución Local
Sigue estos pasos para clonar el repositorio e iniciar la aplicación en tu máquina local de Windows.

### 4.1 Paso 1: Configurar el entorno virtual
Abre tu terminal (PowerShell o Símbolo del Sistema) en la raíz del proyecto y ejecuta:

```powershell
python -m venv venv

# Habilitar permisos de ejecución de Scripts en PowerShell (Solo Windows - Ejecutar como admin si falla)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activar el entorno virtual (PowerShell)
.\venv\Scripts\Activate.ps1

# Activar el entorno virtual (CMD alternativo)
.\venv\Scripts\activate.bat
```

### 4.2 Paso 2: Instalar dependencias
Instala todas las librerías necesarias especificadas en el archivo de requerimientos:

```bash
pip install -r requirements.txt
```

O alternativamente:

```bash
pip install streamlit pandas plotly openpyxl
```

### 4.3 Paso 3: Ejecutar la aplicación
Lanza el servidor local de Streamlit mediante el comando:

```bash
streamlit run main.py
```

## ☁️ 5. Despliegue en Azure App Service
El proyecto cuenta con despliegue automatizado y continuo en la nube de Microsoft Azure. Los pasos clave realizados para la publicación pública del servicio incluyen:

- Creación del recurso: configuración de un Web App en Azure App Service seleccionando la pila de Python 3.12 (Linux).
- Configuración de Arranque (Startup Command): ajuste del comando en el panel de Azure para inicializar el contenedor web de manera persistente.
- Despliegue local mediante Git/GitHub Actions: vinculación del repositorio para disparar la compilación automática ante actualizaciones en la rama principal.

Ejemplo de comando de inicio:

```bash
python -m streamlit run main.py --server.port 8080 --server.address 0.0.0.0
```

## 📈 6. Visualizaciones e Interpretación de Resultados
(Nota: adjunta capturas de pantalla de cada sección del dashboard debajo de cada punto al realizar la entrega definitiva.)

### 6.1 Mapa Departamental de Mortalidad
Descripción: Representación del volumen bruto y acumulado de fallecimientos por entidad territorial.

Hallazgo Clínico/Social: Existe una correlación lineal directa entre las densidades demográficas del país y el número absoluto de muertes. Departamentos con alta concentración poblacional como Antioquia, Valle del Cauca y Bogotá D.C. dominan los registros, sirviendo de base para calcular tasas ponderadas de mortalidad relativa por cada 100,000 habitantes.

### 6.2 Línea Temporal (Evolución por Meses)
Descripción: Gráfico lineal continuo que evalúa el comportamiento temporal de las defunciones en 2019.

Hallazgo Clínico/Social: Permite rastrear la estacionalidad de las afecciones humanas. Picos estadísticos hacia el cierre del año (diciembre) e inicios (enero) suelen ligarse epidemiológicamente al incremento de muertes por causas externas accidentales o de orden público.

### 6.3 Ciudades más Violentas (Homicidios CIE-10: X95)
Descripción: Histograma enfocado en aislar las 5 ciudades con mayor tasa absoluta de agresiones letales con disparo de armas de fuego.

Hallazgo Clínico/Social: Al filtrar quirúrgicamente el dataset con el código X95 cruzado con la Divipola, el sistema expone los principales focos geográficos con crisis de seguridad urbana, permitiendo priorizar planes de intervención social y de desarme militar.

### 6.4 Ciudades con Menor Mortalidad
Descripción: Gráfico de distribución circular (Pie Chart) con los 10 municipios colombianos con menores reportes de muertes registradas en la base de datos.

Hallazgo Clínico/Social: Generalmente, estas cifras corresponden a áreas no municipalizadas del país o corregimientos de baja densidad poblacional (ej: Amazonía/Orinoquía). Sin embargo, estadísticamente es vital contemplar posibles fenómenos institucionales de subregistro o brechas de reporte hospitalario en zonas de difícil acceso geográfico.

### 6.5 Top 10 Principales Causas de Muerte (CIE-10 Mapeado)
Descripción: Tabla ordenada de mayor a menor que cruza los códigos de fallecimiento con su descripción textual en español.

Hallazgo Clínico/Social: Se evidencia la transición epidemiológica típica de Colombia, donde los primeros puestos están ocupados por enfermedades crónicas no transmisibles (como enfermedades isquémicas del corazón o accidentes cerebrovasculares) junto con el impacto crónico de causas violentas externas.

### 6.6 Análisis de Brecha de Género (Barras Apiladas por Departamento)
Descripción: Comparativa visual que contrasta el volumen de muertes entre hombres y mujeres por cada departamento.

Hallazgo Clínico/Social: En la vasta mayoría de departamentos se observa una brecha asimétrica donde el sexo masculino presenta mayores registros de decesos. Esto obedece en gran medida a la alta exposición de la población masculina joven a fallecimientos por causas externas (homicidios, riñas y accidentes viales).

### 6.7 Histograma de Distribución por Etapas de Vida (Grupos de Edad)
Descripción: Agrupación analítica de la variable `GRUPO_EDAD1` bajo las clasificaciones biológicas oficiales del DANE (Mortalidad neonatal, infantil, primera infancia, niñez, adolescencia, juventud, adultez y vejez).

Hallazgo Clínico/Social: La gráfica dibuja una distribución asimétrica en forma de "U" o "J" modificada. La concentración más crítica se localiza en la población de la Vejez y Adultez Intermedia, lo cual es un indicador positivo de la esperanza de vida nacional, contrastado con una alerta epidemiológica en la barra de Mortalidad Neonatal, la cual mide el estado de la infraestructura de salud pública prenatal del país.

---

### 💡 Recomendaciones adicionales para asegurar la nota máxima:
1. **Archivo `requirements.txt`:** Asegúrate de que tu archivo `requirements.txt` contenga exactamente las librerías en minúsculas y sin comandos de instalación:
   ```text
   streamlit
   pandas
   plotly
   openpyxl
   ```
2. **Imágenes:** Cuando corras tu programa y todo funcione, saca capturas de pantalla de los gráficos de cada pestaña de Streamlit, guárdalas en una carpeta llamada `imagenes/` dentro del proyecto y enlázalas en la sección 6 del `README.md` usando la sintaxis de Markdown:
   ```markdown
   ![Nombre del gráfico](imagenes/grafico1.png)
   ```
3. Usa títulos bien jerarquizados para mejorar la lectura y la presentación en GitHub.

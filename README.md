Proyecto_mortalidad_en_colombia_2019/
│
├── datos/                  # Guarda aquí los 3 archivos .xlsx del DANE
│   ├── NoFetal2019.xlsx
│   ├── CodigosDeMuerte.xlsx
│   └── Divipola.xlsx
│
├── vistas/                 # Acà se guardan las interfaces utilizadas
│   ├── __init__.py
│   └── analisis.py
│
├── main.py                 # El archivo principal que ejecutará Streamlit
├── requirements.txt        # Las librerías que usará Azure
└── README.md               # La documentación del proyecto



**Librerias 
pip install streamlit pandas plotly openpyxl
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
venv\Scripts\activate.bat
pip install streamlit pandas plotly openpyxl


**** ejecuciòn 
streamlit run main.py
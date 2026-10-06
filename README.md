# Dashboard de Atenciones

Dashboard desarrollado con Python y Streamlit para analizar atenciones registradas mediante Google Forms y almacenadas en Google Sheets. Actualmente puede ejecutarse con datos ficticios locales; la integración productiva con Google Sheets está prevista para una etapa posterior.

## Tecnologías

- Python 3.12
- Streamlit
- pandas
- Plotly
- Google Sheets API como integración prevista/productiva
- pytest
- Ruff
- Dev Container

## Características

Permitir el seguimiento de:

- total de atenciones;
- atenciones por fecha;
- campus;
- lugar de atención;
- canal;
- área responsable;
- estados de resolución;
- resolución al primer contacto;
- casos derivados;
- motivos de consulta y su top;
- tabla de detalle.

## Arquitectura

```text
src/
├── application/
│   └── services/
├── domain/
│   └── models/
├── infrastructure/
│   └── google_sheets/
└── presentation/
    ├── components/
    └── pages/
```

La aplicación separa la lógica de negocio de la interfaz y de las integraciones externas.

## Desarrollo local

Durante la primera etapa se utiliza:

```text
data/sample_atenciones.csv
```

Este archivo contiene únicamente información ficticia.

La integración real con Google Sheets se implementará posteriormente.

## Requisitos

### Opción recomendada: Dev Container

El proyecto está preparado para ejecutarse mediante VS Code Dev Containers.

Clona el repositorio y ábrelo en VS Code:

```bash
git clone <URL_DEL_REPOSITORIO>
cd dashboard-atenciones
```

Después, ejecuta:

```text
Dev Containers: Reopen in Container
```

Las dependencias se instalan automáticamente desde:

```text
requirements.txt
```

### Ejecución sin Dev Container

```bash
python -m venv .venv
```

En macOS/Linux usa `source .venv/bin/activate`; en Windows PowerShell usa `.venv\\Scripts\\Activate.ps1`. Luego instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run src/app.py
```

Abre http://localhost:8501 en el navegador.

## Datos de ejemplo

`data/sample_atenciones.csv` contiene únicamente datos ficticios. Nunca deben versionarse datos reales de estudiantes.

## Configuración

Usa `.env.example` y `.streamlit/secrets.toml.example` como referencias. No incluyas credenciales reales.

## Calidad

Antes de completar una tarea ejecutar:

```bash
ruff check .
pytest
```

## Seguridad y privacidad

Nunca versionar:

```text
.env
.streamlit/secrets.toml
credentials.json
token.json
client_secret*.json
```

No versionar datos personales reales. La integración con Google Sheets debe utilizar únicamente permisos de lectura.

## Estado actual

El dashboard local funciona con el dataset ficticio incluido, filtros, KPIs, gráficos y tabla de detalle. La integración productiva con Google Sheets aún está pendiente.

## Demo para Windows

Existe una versión demostrativa instalable para Windows que funciona sin Python, Docker ni dependencias en la PC destino. Incluye únicamente el dataset ficticio local `data/sample_atenciones.csv`; Google Sheets todavía no está integrado.

Para generar el instalador, ejecuta manualmente el workflow **Build Windows installer** desde GitHub Actions (o crea un tag `v*`). El artifact generado se llama `DashboardAtenciones-Setup.exe`.

## Licencia

Este proyecto se distribuye bajo la [MIT License](LICENSE).

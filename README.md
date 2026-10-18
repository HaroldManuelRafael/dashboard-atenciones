# Dashboard de Atenciones

Dashboard desarrollado con Python y Streamlit para analizar atenciones registradas mediante Google Forms. Puede usar datos ficticios locales en Excel o una hoja de Google Sheets en modo solo lectura.

## Tecnologías

- Python 3.12
- Streamlit
- pandas
- Plotly
- Google Sheets API en modo solo lectura
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

Durante la primera etapa se utiliza un archivo Excel editable:

```text
data/sample_atenciones.xlsx
```

Este archivo contiene únicamente información ficticia.

La fuente predeterminada es local. Puede seleccionarse Google Sheets con `DASHBOARD_DATA_SOURCE=google_sheets`; requiere configurar el ID del spreadsheet, el nombre de la pestaña y una cuenta de servicio con permisos Viewer. La integración usa únicamente lectura.

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

En una instalación empaquetada, el archivo editable se encuentra en `%APPDATA%\\DashboardAtenciones\\data\\atenciones.xlsx`. Puede editarse o reemplazarse manteniendo el mismo esquema. Contiene únicamente datos ficticios; nunca deben versionarse datos reales de estudiantes.

## Configuración

Usa `.env.example` como referencia. Para Google Sheets configura `GOOGLE_SPREADSHEET_ID`, `GOOGLE_WORKSHEET_NAME` y `GOOGLE_SERVICE_ACCOUNT_FILE`. No incluyas credenciales reales.

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

El dashboard funciona con el dataset local ficticio o, mediante configuración, con Google Sheets en modo solo lectura; filtros, KPIs, gráficos y tabla de detalle son comunes a ambas fuentes.

## Demo para Windows

Existe una versión demostrativa instalable para Windows que funciona sin Python, Docker ni dependencias en la PC destino. Incluye únicamente el dataset ficticio local `data/sample_atenciones.xlsx`; Google Sheets requiere configuración externa de credenciales y no se empaqueta.

Para generar el instalador, ejecuta manualmente el workflow **Build Windows installer** desde GitHub Actions (o crea un tag `v*`). El artifact generado se llama `DashboardAtenciones-Setup.exe`.

## Licencia

Este proyecto se distribuye bajo la [MIT License](LICENSE).

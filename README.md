# Dashboard de Atenciones

Dashboard desarrollado en Python para analizar atenciones realizadas a estudiantes.

La fuente productiva será Google Sheets, alimentada mediante Google Forms. La aplicación tendrá acceso únicamente de lectura.

## Stack

- Python 3.12
- Streamlit
- pandas
- Plotly
- Google Sheets API
- pytest
- Ruff
- Dev Container

## Objetivo

Permitir el seguimiento de:

- total de atenciones;
- atenciones por fecha;
- campus;
- lugar de atención;
- canal;
- área responsable;
- motivos de consulta;
- resolución;
- resolución al primer contacto;
- casos derivados;
- principales casuísticas.

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

### Domain

Contiene modelos y conceptos del negocio.

No debe depender de Streamlit, Google APIs ni Plotly.

### Application

Contiene transformación de datos, filtros, métricas y casos de uso.

### Infrastructure

Contiene integraciones externas.

Inicialmente:

```text
Google Sheets API
```

### Presentation

Contiene la interfaz Streamlit:

- páginas;
- filtros;
- KPIs;
- gráficos;
- tablas.

## Desarrollo local

Durante la primera etapa se utiliza:

```text
data/sample_atenciones.csv
```

Este archivo contiene únicamente información ficticia.

La integración real con Google Sheets se implementará posteriormente.

## Dev Container

El proyecto está preparado para ejecutarse mediante VS Code Dev Containers.

Después de abrir el repositorio:

```text
Dev Containers: Reopen in Container
```

las dependencias se instalan automáticamente desde:

```text
requirements.txt
```

## Ejecutar la aplicación

Cuando la aplicación esté implementada:

```bash
streamlit run src/app.py
```

El puerto 8501 se notificará en VS Code sin abrir pestañas automáticamente. Abre el enlace del puerto desde el panel **Ports** cuando quieras ver el dashboard. Streamlit utilizará por defecto:

```text
http://localhost:8501
```

## Calidad

Antes de completar una tarea ejecutar:

```bash
ruff check .
pytest
```

## Seguridad

Nunca versionar:

```text
.env
.streamlit/secrets.toml
credentials.json
token.json
client_secret*.json
```

La integración con Google Sheets debe utilizar únicamente permisos de lectura.

## Documentación

Los requisitos funcionales se encuentran en:

```text
docs/requirements.md
```

El contrato de datos se encuentra en:

```text
docs/data-contract.md
```

Las instrucciones de desarrollo para agentes de código se encuentran en:

```text
AGENTS.md
```

## Estado actual

Primera etapa:

- [x] Dev Container
- [x] dependencias Python
- [x] arquitectura base
- [x] contrato de datos
- [x] requisitos funcionales
- [x] dataset ficticio
- [ ] implementación del dashboard
- [ ] tests
- [ ] integración con Google Sheets

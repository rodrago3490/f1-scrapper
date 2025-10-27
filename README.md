# F1 Scraper

Herramienta de línea de comandos para descargar los datos de Fórmula 1 (carreras y clasificaciones de qualy) de cualquier temporada y exportarlos a un archivo Excel.

## Requisitos

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py 2023 --output resultados_2023.xlsx
```

Argumentos principales:

- `year`: temporada que se desea descargar (por ejemplo `2023`).
- `--output`: ruta del archivo Excel generado (opcional, por defecto `f1_results.xlsx`).
- `--log-level`: nivel de logging (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).

El archivo Excel resultante contiene dos hojas:

- `races`: resultados de cada gran premio (sin incluir sprints).
- `qualifying`: resultados de cada sesión de clasificación.

La herramienta reintenta automáticamente las descargas frente a errores de red
transitorios (códigos 429/5xx o reinicios de conexión). Si el proceso falla
tras varios intentos, revisa tu conexión o configura los certificados/puerto
según sea necesario para tu entorno.

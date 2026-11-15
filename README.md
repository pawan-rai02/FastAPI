# FastAPI + Pydantic Learning Project

A collection of small FastAPI apps built while learning Pydantic, request validation, and serving a scikit-learn model as an API.

## Project structure

```
.
├── curd-fastapi/
│   ├── 01-create.py          # Read-only patient API (GET routes + JSON file storage)
│   ├── 02-post-req.py        # Adds POST /create with a Pydantic Patient model
│   ├── 03_update_delete.py   # Full CRUD: POST /create, PUT /edit, DELETE /delete
│   ├── 04_fastApi-ML.ipynb   # Notebook: trains the insurance premium model -> model.pkl
│   ├── 05_app.py             # FastAPI app serving the ML model (POST /predict)
│   ├── streamlit_app.py      # Streamlit UI that calls the /predict endpoint
│   ├── model.pkl             # Trained model used by 05_app.py
│   └── patients.json         # Sample data for the CRUD apps
├── pydantic/                 # Standalone Pydantic examples (validators, computed fields)
├── insurance.csv             # Dataset used to train the model
└── myenv/                    # Local virtual environment
```

## Prerequisites

- Python 3.10+
- The packages used here:

```bash
pip install fastapi uvicorn pydantic scikit-learn pandas numpy streamlit requests jupyter
```

This repo already has a virtual environment in `myenv/`. Activate it instead of installing globally:

```bash
# Git Bash / macOS / Linux
source myenv/Scripts/activate      # on Windows Git Bash
source myenv/bin/activate          # on macOS / Linux

# Windows CMD / PowerShell
myenv\Scripts\activate
```

## How to start

All FastAPI apps are started with `uvicorn` from the `curd-fastapi/` folder. Once running, open the interactive docs at the URL printed in the terminal (e.g. `http://127.0.0.1:8000/docs`).

### 1. Patient CRUD API

```bash
cd curd-fastapi

# read-only version
python -m uvicorn 01-create:app --reload --port 8000

# with create
python -m uvicorn 02-post-req:app --reload --port 8000

# full CRUD (create, update, delete)
python -m uvicorn 03_update_delete:app --reload --port 8000
```

> `--reload` restarts the server automatically when you save a file, so a new port per script isn't required — just use one app at a time.

Useful endpoints for `03_update_delete.py`:

| Method | Path                 | Purpose                        |
| ------ | -------------------- | ------------------------------ |
| POST   | `/create`            | Create a new patient           |
| PUT    | `/edit/{patient_id}` | Update fields of a patient     |
| DELETE | `/delete/{patient_id}` | Delete a patient             |

Interactive docs: `http://127.0.0.1:8000/docs`

### 2. Insurance premium predictor API

**Important:** `05_app.py` loads `model.pkl` using a relative path, so run it from inside `curd-fastapi/`.

```bash
cd curd-fastapi
python -m uvicorn 05_app:app --reload --port 8002
```

- Endpoint: `POST http://127.0.0.1:8002/predict`
- Docs: `http://127.0.0.1:8002/docs`

Example request:

```bash
curl -X POST http://127.0.0.1:8002/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 30, "weight": 70, "height": 1.75, "income_lpa": 10, "smoker": false, "city": "Mumbai", "occupation": "private_job"}'
```

Example response:

```json
{ "predicted_category": "Low" }
```

### 3. Streamlit UI

The Streamlit app is a front end for the model API and expects it on **port 8002** (see `requests.post(...)` in `streamlit_app.py`).

```bash
# terminal 1 - start the API
cd curd-fastapi
python -m uvicorn 05_app:app --reload --port 8002

# terminal 2 - start the UI
cd curd-fastapi
streamlit run streamlit_app.py
```

Streamlit opens on `http://localhost:8501`. If you start the API on a different port, update the URL in `streamlit_app.py` to match.

### 4. Pydantic examples

These are plain scripts, not servers:

```bash
python pydantic/01-pydantic_why.py
python pydantic/02-filed_validator.py
python pydantic/03-model_validator.py
python pydantic/04-computed_field.py
```

### 5. Retraining the model (optional)

Open the notebook and run all cells, which rewrites `curd-fastapi/model.pkl`:

```bash
jupyter notebook curd-fastapi/04_fastApi-ML.ipynb
```

## Troubleshooting

- **`ModuleNotFoundError`** — activate `myenv` or install the packages listed above.
- **`FileNotFoundError: model.pkl`** — you launched `05_app.py` from the wrong directory; `cd curd-fastapi` first.
- **Streamlit shows "Could not connect to the API"** — the FastAPI server isn't running, or it's on a port other than 8002.
- **Port already in use** — pick another port (`--port 8003`) or stop the old process.

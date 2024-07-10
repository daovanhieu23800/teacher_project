# Store Items Demand Forecasting

In this example, we serve a [LightGBM model](https://lightgbm.readthedocs.io/en/stable/) using `FastAPI` for the backend service and `streamlit` for the frontend service. `docker compose` orchestrates the two services and allows communication between them.

To run the example in a machine running Docker and docker compose, run:

```bash
docker compose build
docker compose up
```

To visit the FastAPI documentation of the resulting service, visit [http://localhost:8000/docs](http://localhost:8000/docs) with a web browser.
To visit the streamlit UI, visit [http://localhost:8501](http://localhost:8501/).

Logs can be inspected via:

```bash
docker compose logs
```

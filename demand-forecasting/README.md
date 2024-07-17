# Store Items Demand Forecasting

The objective of this competition is to predict 3 months of item-level sales data at different store locations.

## Data fields for Historical data

* **date** - Date of the sale data. There are no holiday effects or store closures.
* **store** - Store ID
* **item** - Item ID
* **sales** - Number of items sold at a particular store on a particular date.

## Input

* **date** - Date of the sale data. There are no holiday effects or store closures.
* **store** - Store ID
* **item** - Item ID

## Ouput

* **predicted sales** - Number of items sold at a particular store on a next 3 months from date on input

## User Interface

Here is the landing page:

![Alt text](/space/hotel/quangd/projects/outsource/teacher_project/demand-forecasting/images/ui-1.png "landing page")

Web app has 2 input option: 

**Input 1 item via filling the form** 

![Alt text](/space/hotel/quangd/projects/outsource/teacher_project/demand-forecasting/images/ui-2.png "Input 1 item")

**Input multi items via uploading file**

![Alt text](/space/hotel/quangd/projects/outsource/teacher_project/demand-forecasting/images/ui-3.png "Input multi items")

## Run demo app

In this example, we serve a [LightGBM model](https://lightgbm.readthedocs.io/en/stable/) using `FastAPI` for the backend service and `streamlit` for the frontend service. `docker compose` orchestrates the two services and allows communication between them.

### Run separated services

*Note: Run 2 services on 2 terminals separately*

**Client side - Streamlit**

```bash
cd streamlit
python -m pip install -r requirements.txt
streamlit run ui.py
```

**Server side - FastAPI**

```bash
cd fastapi
python -m pip install -r requirements.txt
python -m uvicorn api:app --host 0.0.0.0 --port 8080
```

### Run with docker

To run the example in a machine running Docker and docker compose, run:

```bash
docker compose build
docker compose up
```

To visit the FastAPI documentation of the resulting service, visit [http://localhost:8080/docs](http://localhost:8000/docs) with a web browser.
To visit the streamlit UI, visit [http://localhost:8501](http://localhost:8501/).

Logs can be inspected via:

```bash
docker compose logs
```

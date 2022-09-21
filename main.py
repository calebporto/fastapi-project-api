'''
Project Files Structure:

.
├── ibvg-api
│   ├── __init__.py
│   ├── main.py  ------------------------ # "main" module, e.g. import app.main
|   ├── Procfile ------------------------ # heroku Procfile
│   ├── services.py --------------------- # query modules Async SQLAlchemy
|   ├── README.md ----------------------- # README for github
|   ├── requirements.txt ---------------- # Dependencies
|   ├── models
|   |   ├── __init__.py
|   |   ├── basemodels.py --------------- # Pydantic classes
|   |   ├── config.py ------------------- # Connection params
|   |   ├── connection.py --------------- # Connection services
|   |   ├── init_db.py ------------------ # Create database services
|   |   └── tables
|   |       ├── __init__.py
|   |       └── client.py --------------- # SQLAlchemy classes
|   ├── providers
|   |       ├── __init__.py
|   |       └── hash_provider.py -------- # hash generator
│   ├── routers
│   │   ├── __init__.py
│   │   ├── query_endpoints.py ---------- # Back-end endpoints
│   │   └── scheduler_endpoints.py ------ # Scheduler endpoints
│   └── tests ---------------------
│       ├── __init__.py           |
│       ├── conftest.py           |
|       └── api                   └── Under development ...
|           ├── __init__.py
|           └── test_main.py
'''

from routers import query_endpoints, scheduler_endpoints
from fastapi import FastAPI, HTTPException, Request
from secrets import compare_digest
import os


app = FastAPI(
    title='IBVG-API',
    description='API para transações no banco de dados da aplicação',
    version='1.0'
)

@app.middleware("http")
async def auth(request: Request, call_next):
    ''' Middleware para definir autorização de requisições, de acordo com a api_key e o IP da requisição'''
    try:
        # Antes
        if not request.headers['api_key'] or not compare_digest(request.headers['api_key'], os.environ['API_KEY']):
            raise HTTPException(status_code=401, detail="Forbidden")
        
        if not request.headers['id'] or not compare_digest(request.headers['id'], os.environ['AUTHORIZED_ID']):
            raise HTTPException(status_code=401, detail="Forbidden")
        
        response = await call_next(request)

        # Depois
        return response

    except KeyError as error:
        raise HTTPException(status_code=401, detail="Forbidden")
    
app.include_router(query_endpoints.router)
app.include_router(scheduler_endpoints.router)
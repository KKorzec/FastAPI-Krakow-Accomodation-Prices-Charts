from fastapi import FastAPI
from WebScrp.records import router as record_router
from fastapi.middleware.cors import CORSMiddleware
from WebScrp.records import scraper_olx
from WebScrp.records import scraper_tabela

app = FastAPI(title='DB WS CRUD',
              description='Database operations with usage of Web-Scrapper',
              version='0.1')
origins = [
    "http://localhost",
    "http://localhost:3000",  # Front-end
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(record_router.router)

#response = requests.post('http://127.0.0.1:8000/record/olx')

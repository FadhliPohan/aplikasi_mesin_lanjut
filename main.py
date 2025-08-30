from fastapi import FastAPI
from route import route  # Mengimpor router dari file route.py di dalam folder route

app = FastAPI()

# Menambahkan prefix '/api' pada semua rute
app.include_router(route.router, prefix="/api")

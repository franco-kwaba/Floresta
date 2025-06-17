#from app.db import criar_banco
#from app.modelos import adicionar_conselheiro, adicionar_queixa, adicionar_avaliacao, exibir_ranking

# Cria o banco na primeira execução
#criar_banco("data/condominio.db")

from fastapi import FastAPI

app = FastAPI()



from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API FastAPI funcionando no Render!"}

@app.get("/hello")
def hello():
    return {"greet": "Olá!"}


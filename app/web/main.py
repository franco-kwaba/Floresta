from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from app.modelos import (
    listar_conselheiros, adicionar_conselheiro,
    listar_queixas, adicionar_queixa,
    listar_queixas_rankeadas, adicionar_avaliacao, buscar_avaliacao, atualizar_avaliacao, 
    listar_opcoes_risco_seguranca, listar_opcoes_risco_integridade, listar_opcoes_risco_bens,
    listar_opcoes_prioridades, listar_opcoes_probabilidades, 
    listar_opcoes_custos, listar_opcoes_percepcoes, salvar_alteracao_custo, atualizar_medias_queixa, listar_queixas_por_score
)

app = FastAPI()

# Diretório onde estão os templates e arquivos estáticos
BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

from app.db import criar_banco
from app.modelos import adicionar_conselheiro, adicionar_queixa, exibir_ranking, buscar_queixa 

# Cria o banco na primeira execução
criar_banco("data/condominio.db")


@app.get("/conselheiros", response_class=HTMLResponse)
def conselheiros_list(request: Request):
    conselheiros = listar_conselheiros()
    return templates.TemplateResponse(
        "conselheiros.html", {"request": request, "conselheiros": conselheiros}
    )

@app.post("/conselheiros", response_class=HTMLResponse)
def conselheiros_add(
        request: Request,
        nome: str = Form(...),
        unidade: str = Form(...),
        status: str = Form(...),
        tipo: str = Form(...)
    ):
    adicionar_conselheiro(nome, unidade, status, tipo)
    return RedirectResponse("/conselheiros", status_code=302)

# Repita um padrão semelhante para queixas e avaliações...


# ... (rotas já existentes) ...

@app.get("/queixas", response_class=HTMLResponse)
def mostrar_queixas(request: Request):
    queixas = listar_queixas()
    custo_opcoes = listar_opcoes_custos()
    percepcao_opcoes = listar_opcoes_percepcoes()
    return templates.TemplateResponse(
        "queixas.html", {"request": request, 
                         "queixas": queixas,
                         "custos": custo_opcoes,
                         "percepcoes": percepcao_opcoes
                         }
    )



@app.post("/queixas", response_class=HTMLResponse)
def cadastrar_queixa(
    request: Request,
    descricao: str = Form(...),
    custo: int = Form(...),
    percepcao: int = Form(...)
):
    adicionar_queixa(descricao, custo, percepcao)
    
    return RedirectResponse("/queixas", status_code=303)




def mostrar_form_avaliacao(request: Request, queixa_id: int, conselheiro_id: int = None):
    if not conselheiro_id:
        return RedirectResponse("/", status_code=303)
    # Listar conselheiros para o select (opcional)
    from app.modelos import listar_conselheiros
    conselheiros = listar_conselheiros()
    return templates.TemplateResponse("avaliacao.html", {
        "request": request, "queixa_id": queixa_id, "conselheiros": conselheiros
    })





@app.post("/avaliar/{queixa_id}")
def cadastrar_avaliacao(
    request: Request,
    queixa_id: int,
    conselheiro_id: int = Form(...),
    risco_seguranca: float = Form(...),
    risco_integridade: float = Form(...),
    risco_bens: float = Form(...),
    probabilidade: float = Form(...),
    urgencia: float = Form(...),
    
    
    
):
    adicionar_avaliacao(
        queixa_id, conselheiro_id, risco_seguranca, risco_integridade,
        risco_bens, probabilidade, urgencia
    )
    caminho_banco= "data/condominio.db"
    atualizar_medias_queixa(queixa_id, caminho_banco)
    return RedirectResponse(f"/painel?conselheiro_id={conselheiro_id}", status_code=303)



@app.get("/", response_class=HTMLResponse)
def tela_inicial(request: Request):
    from app.modelos import listar_conselheiros
    conselheiros = listar_conselheiros()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "conselheiros": conselheiros
    })
    

@app.get("/painel", response_class=HTMLResponse)
def painel_conselheiro(request: Request, conselheiro_id: int):
    from app.modelos import (
        listar_nome_conselheiro,
        listar_queixas_avaliadas,
        listar_queixas_pendentes,
        listar_queixas_sindico,
    )

    conselheiro_nome = listar_nome_conselheiro(conselheiro_id)
    avaliadas = listar_queixas_avaliadas(conselheiro_id)
    pendentes = listar_queixas_pendentes(conselheiro_id)
    queixas_sindico =  listar_queixas_sindico()

    return templates.TemplateResponse("painel.html", {
        "request": request,
        "conselheiro_id": conselheiro_id,
        "conselheiro_nome": conselheiro_nome,
        "avaliadas": avaliadas,
        "pendentes": pendentes,
        "queixas_sindico": queixas_sindico
    })




@app.get("/avaliar_custo_queixa/{queixa_id}", response_class=HTMLResponse)
def mostrar_form_avaliacao_custo(request: Request, queixa_id: int, conselheiro_id: int = None):
    if not conselheiro_id:
        return RedirectResponse("/", status_code=303)
    # Checar se já existe avaliação dessa queixa por esse conselheiro
    queixa = buscar_queixa(queixa_id)
   
    # Não existe: prossegue exibindo campos em branco
    from app.modelos import listar_nome_conselheiro
    conselheiro_nome = listar_nome_conselheiro(conselheiro_id)
   
    opcoes_custos = listar_opcoes_custos()
    opcoes_percepcoes = listar_opcoes_percepcoes()
   
    return templates.TemplateResponse("avaliar_custo_queixa.html", {
        "request": request,
        "queixa_id": queixa_id,
        "conselheiro_id": conselheiro_id,
        "conselheiro_nome": conselheiro_nome,
        "queixa": queixa,
        "opcoes_custos": opcoes_custos,
        "opcoes_percepcoes": opcoes_percepcoes
    })

@app.post("/avaliar_custo_queixa/{queixa_id}", response_class=HTMLResponse)
def salvar_alteracao_custo_queixa(
    queixa_id: int,
    descricao: str = Form(...), 
    custo: int = Form(...),
    percepcao: int = Form(...),
    conselheiro_id: float = Form(...),

):
    salvar_alteracao_custo(
        queixa_id, descricao, custo,percepcao, conselheiro_id
    )
    caminho_banco= "data/condominio.db"
    atualizar_medias_queixa(queixa_id, caminho_banco)
    # Redireciona para painel (por exemplo)
    return RedirectResponse(f"/painel?conselheiro_id={conselheiro_id}", status_code=303)


@app.post("/avaliar_custo_queixa/{queixa_id}", response_class=HTMLResponse)


@app.get("/avaliar/{queixa_id}", response_class=HTMLResponse)
def mostrar_form_avaliacao(request: Request, queixa_id: int, conselheiro_id: int = None):
    if not conselheiro_id:
        return RedirectResponse("/", status_code=303)
    # Checar se já existe avaliação dessa queixa por esse conselheiro
    from app.modelos import buscar_avaliacao
    avaliacao = buscar_avaliacao(queixa_id, conselheiro_id)
    if avaliacao:
        # Já existe: Redireciona para tela de alteração (ou mostra os dados pra editar, depende do seu fluxo)
        return RedirectResponse(f"/alterar_avaliacao/{queixa_id}?conselheiro_id={conselheiro_id}", status_code=303)
    # Não existe: prossegue exibindo campos em branco
    from app.modelos import listar_nome_conselheiro
    conselheiro_nome = listar_nome_conselheiro(conselheiro_id)
    opcoes_risco_seguranca = listar_opcoes_risco_seguranca()
    opcoes_risco_integridade = listar_opcoes_risco_integridade()
    opcoes_risco_bens = listar_opcoes_risco_bens()
    opcoes_prioridades = listar_opcoes_prioridades()
    opcoes_probabilidades = listar_opcoes_probabilidades()
    opcoes_custos = listar_opcoes_custos()
    opcoes_percepcoes = listar_opcoes_percepcoes()
    itens_queixa =  buscar_queixa(queixa_id)
    return templates.TemplateResponse("avaliacao.html", {
        "request": request,
        "queixa_id": queixa_id,
        "conselheiro_id": conselheiro_id,
        "conselheiro_nome": conselheiro_nome,
        "avaliacao": None,
        "opcoes_risco_seguranca": opcoes_risco_seguranca,
        "opcoes_risco_integridade": opcoes_risco_integridade,
        "opcoes_risco_bens": opcoes_risco_bens,
        "opcoes_prioridades": opcoes_prioridades,
        "opcoes_probabilidades": opcoes_probabilidades,
        "opcoes_custos": opcoes_custos,
        "opcoes_percepcoes": opcoes_percepcoes,
        "valores_queixa": itens_queixa
    })

@app.get("/alterar_avaliacao/{queixa_id}")
def exibir_form_alteracao(request: Request, queixa_id: int, conselheiro_id: int):
    avaliacao = buscar_avaliacao(queixa_id, conselheiro_id)
    opcoes_risco_seguranca = listar_opcoes_risco_seguranca()
    opcoes_risco_integridade = listar_opcoes_risco_integridade()
    opcoes_risco_bens = listar_opcoes_risco_bens()
    opcoes_prioridades = listar_opcoes_prioridades()
    opcoes_probabilidades = listar_opcoes_probabilidades()
    opcoes_custos = listar_opcoes_custos()
    opcoes_percepcoes = listar_opcoes_percepcoes()
    itens_queixa =  buscar_queixa(queixa_id)
    return templates.TemplateResponse(
        "alterar_avaliacao.html", 
        {
            "request": request,
            "queixa_id": queixa_id,
            "conselheiro_id": conselheiro_id,
            "avaliacao": avaliacao,
            "opcoes_risco_seguranca": opcoes_risco_seguranca,
            "opcoes_risco_integridade": opcoes_risco_integridade,
            "opcoes_risco_bens": opcoes_risco_bens,
            "opcoes_prioridades": opcoes_prioridades,
            "opcoes_probabilidades": opcoes_probabilidades,
            "opcoes_custos": opcoes_custos,
            "opcoes_percepcoes": opcoes_percepcoes,
            "valores_queixa": itens_queixa
        }
    )


@app.post("/alterar_avaliacao/{queixa_id}")
def salvar_alteracao_avaliacao(
    queixa_id: int,
    conselheiro_id: int = Form(...),
    risco_seguranca: float = Form(...),
    risco_integridade: float = Form(...),
    risco_bens: float = Form(...),
    probabilidade: float = Form(...),
    urgencia: float = Form(...),
    custo: float = Form(...),
    percepcao_moradores: float = Form(...)
):
    atualizar_avaliacao(
        queixa_id, conselheiro_id, risco_seguranca, risco_integridade,
        risco_bens, probabilidade, urgencia
    )
    caminho_banco= "data/condominio.db"
    atualizar_medias_queixa(queixa_id, caminho_banco)
    # Redireciona para painel (por exemplo)
    return RedirectResponse(f"/painel?conselheiro_id={conselheiro_id}", status_code=303)




@app.get("/ranking", response_class=HTMLResponse)
def ranking_queixas(request: Request):
    queixas = listar_queixas_por_score()
    return templates.TemplateResponse("ranking.html", {"request": request, "queixas": queixas})
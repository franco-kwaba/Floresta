import sqlite3

#CONEXAO
def conectar_banco(caminho_banco="data/condominio.db"):
    return sqlite3.connect(caminho_banco)

#CONSELHEIROS
def adicionar_conselheiro(nome, unidade, status, tipo, caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conselheiros (nome, unidade, status, tipo)
        VALUES (?, ?, ?, ?)
    """, (nome, unidade, status, tipo))
    conn.commit()
    conn.close()

def listar_conselheiros(caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conselheiros")
    conselheiros = cursor.fetchall()
    conn.close()
    return conselheiros

def buscar_conselheiro_por_id(conselheiro_id, caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conselheiros WHERE id = ?", (conselheiro_id,))
    conselheiro = cursor.fetchone()
    conn.close()
    return conselheiro 
        
def listar_nome_conselheiro(conselheiro_id):
    import sqlite3
    conn = sqlite3.connect("data/condominio.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conselheiros WHERE id = ?", (conselheiro_id,))
    nome = cursor.fetchone()
    conn.close()
    return nome[4], nome[1] if nome else "N/A"



#QUEIXAS
def adicionar_queixa(descricao, custo, percepcao):
    import sqlite3
    conn = sqlite3.connect("data/condominio.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO queixas (descricao, custo, percepcao) VALUES (?,?,?)",
        (descricao,custo,percepcao)
    )
    conn.commit()
    conn.close()

def listar_queixas():
    import sqlite3
    conn = sqlite3.connect("data/condominio.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, descricao, criado_em FROM queixas ORDER BY criado_em DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def listar_queixas_sindico():
    import sqlite3
    conn = sqlite3.connect("data/condominio.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, descricao, criado_em FROM queixas")
    rows = cursor.fetchall()
    conn.close()
    return rows

def buscar_queixa(id_queixa, caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM queixas
        WHERE id = ? 
    """, (id_queixa,))
    queixa = cursor.fetchone()
    conn.close()
    return queixa


#AVALIAÇÕES
def adicionar_avaliacao(id_queixa, id_conselheiro, risco_seguranca, risco_integridade,
                        risco_bens, probabilidade, urgencia, caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO avaliacoes (
                id_queixa, id_conselheiro, risco_seguranca, risco_integridade, risco_bens, 
                probabilidade, urgencia
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id_queixa, id_conselheiro, risco_seguranca, risco_integridade, risco_bens,
              probabilidade, urgencia))
        conn.commit()
        #atualizar_medias_queixa(id_queixa, caminho_banco)
    except sqlite3.IntegrityError:
        print("Esse conselheiro já avaliou essa queixa.")
    conn.close()


def listar_queixas_pendentes(conselheiro_id):
    # Queixas que este conselheiro AINDA NÃO avaliou
    import sqlite3
    conn = sqlite3.connect("data/condominio.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT q.id, q.descricao
        FROM queixas q
        WHERE q.id NOT IN (
            SELECT id_queixa FROM avaliacoes WHERE id_conselheiro = ?
        )
        ORDER BY q.criado_em DESC
    """, (conselheiro_id,))
    result = cursor.fetchall()
    conn.close()
    return result

def listar_queixas_avaliadas(conselheiro_id):
    import sqlite3
    conn = sqlite3.connect("data/condominio.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT q.id, q.descricao
        FROM queixas q
        JOIN avaliacoes a ON a.id_queixa = q.id
        WHERE a.id_conselheiro = ?
        ORDER BY q.criado_em DESC
    """, (conselheiro_id,))
    result = cursor.fetchall()
    conn.close()
    return result

#####################################################################


def buscar_avaliacao(id_queixa, id_conselheiro, caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM avaliacoes
        WHERE id_queixa = ? AND id_conselheiro = ?
    """, (id_queixa, id_conselheiro))
    avaliacao = cursor.fetchone()
    conn.close()
    return avaliacao

def salvar_alteracao_custo(id_queixa, descricao, custo, percepcao_moradores, conselheiro_id, caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE queixas SET
            descricao = ?,
            custo = ?,
            percepcao = ?
                  WHERE id = ?
    """, (descricao, custo, percepcao_moradores, id_queixa))
    conn.commit()
    atualizar_medias_queixa(id_queixa, caminho_banco)
    conn.close()
    
def atualizar_avaliacao(id_queixa, id_conselheiro, risco_seguranca, risco_integridade,
                       risco_bens, probabilidade, urgencia, caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE avaliacoes SET
            risco_seguranca = ?,
            risco_integridade = ?,
            risco_bens = ?,
            probabilidade = ?,
            urgencia = ?
         
        WHERE id_queixa = ? AND id_conselheiro = ?
    """, (risco_seguranca, risco_integridade, risco_bens, probabilidade, urgencia, id_queixa, id_conselheiro))
    conn.commit()
    atualizar_medias_queixa(id_queixa, caminho_banco)
    conn.close()

def atualizar_medias_queixa(id_queixa, caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            AVG(risco_seguranca),
            AVG(risco_integridade),
            AVG(risco_bens),
            AVG(probabilidade),
            AVG(urgencia)
            FROM avaliacoes
        WHERE id_queixa = ?
    """, (id_queixa,))
    (media_risco_seguranca, media_risco_integridade, media_risco_bens,
     media_probabilidade, media_urgencia) = cursor.fetchone()

    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            percepcao, custo
            from QUEIXAS
        WHERE id = ?
    """, (id_queixa,))
    (percepcao, custo) = cursor.fetchone()


    # Calculando as fórmulas (com proteção None para novos registros)
    C = media_risco_seguranca or 0
    D = media_risco_integridade or 0
    E = media_risco_bens or 0
    F = media_probabilidade or 0
    G = media_urgencia or 0
    H = custo or 0
    I = percepcao or 0
    
    prioridade = (I*0.7)+(G*0.3)
    media_riscos = (C*4) + (D*2) + E
    custo = H
    
    parcial = prioridade * media_riscos * custo
    
    
    #pontuacao minima 7 e porntuacao maxima 875, seguindo a escala
    pontuacao_ranking = ((parcial-7)/(875-7))*100
    pontuacao_ranking = round(pontuacao_ranking,0)

    cursor.execute("""
        UPDATE queixas SET 
            media_risco_seguranca = ?, 
            media_risco_integridade = ?,
            media_risco_bens = ?,
            media_probabilidade = ?,
            media_urgencia = ?,
            percepcao = ?,
            media_riscos = ?, 
            prioridade = ?,
            custo = ?,
            pontuacao_ranking = ?
        WHERE id = ?
    """, (
        C, D, E, F, G, I, media_riscos, prioridade, custo, pontuacao_ranking,
        id_queixa
    ))
    conn.commit()
    conn.close()
    


def listar_queixas_por_score(caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, descricao, pontuacao_ranking
        FROM queixas
        ORDER BY pontuacao_ranking DESC
    """)
    queixas = cursor.fetchall()
    conn.close()
    return queixas

#####################################################################
    
def listar_queixas_rankeadas(caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, descricao, impacto_total, media_ponderada, pontuacao_ranking
        FROM queixas
        ORDER BY pontuacao_ranking DESC
    """)
    lista = cursor.fetchall()
    conn.close()
    return lista

def exibir_ranking():
    ranking = listar_queixas_rankeadas()
    print("ID | Descrição | Impacto | Média Ponderada | Pontuação Ranking")
    for item in ranking:
        print(f"{item[0]} | {item[1]} | {item[2]:.2f} | {item[3]:.2f} | {item[4]:.2f}")


def listar_opcoes_risco_seguranca(caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("SELECT valor, descricao FROM risco_seguranca_opcoes ORDER BY valor ASC")
    opcoes = cursor.fetchall()
    conn.close()
    return opcoes

def listar_opcoes_risco_integridade(caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("SELECT valor, descricao FROM risco_integridade_opcoes ORDER BY valor ASC")
    opcoes = cursor.fetchall()
    conn.close()
    return opcoes

def listar_opcoes_risco_bens(caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("SELECT valor, descricao FROM risco_bens_opcoes ORDER BY valor ASC")
    opcoes = cursor.fetchall()
    conn.close()
    return opcoes

def listar_opcoes_prioridades(caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("SELECT valor, descricao FROM prioridades_opcoes ORDER BY valor ASC")
    opcoes = cursor.fetchall()
    conn.close()
    return opcoes

def listar_opcoes_custos(caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("SELECT valor, descricao FROM custo_opcoes ORDER BY valor ASC")
    opcoes = cursor.fetchall()
    conn.close()
    return opcoes

def listar_opcoes_probabilidades(caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("SELECT valor, descricao FROM probabilidade_opcoes ORDER BY valor ASC")
    opcoes = cursor.fetchall()
    conn.close()
    return opcoes

def listar_opcoes_percepcoes(caminho_banco="data/condominio.db"):
    conn = conectar_banco(caminho_banco)
    cursor = conn.cursor()
    cursor.execute("SELECT valor, descricao FROM percepcao_opcoes ORDER BY valor ASC")
    opcoes = cursor.fetchall()
    conn.close()
    return opcoes
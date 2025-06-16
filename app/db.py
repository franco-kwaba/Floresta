 
import sqlite3

def criar_banco(caminho_banco="data/condominio.db"):
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()

    # Tabela de conselheiros
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conselheiros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        unidade TEXT,
        status TEXT NOT NULL,
        tipo TEXT NOT NULL,
        criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Tabela de queixas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS queixas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        media_risco_seguranca REAL DEFAULT 0,
        media_risco_integridade REAL DEFAULT 0,
        media_risco_bens REAL DEFAULT 0,
        media_probabilidade REAL DEFAULT 0,
        media_urgencia REAL DEFAULT 0,
        percepcao INTEGER DEFAULT 0,
       
        media_riscos REAL DEFAULT 0,
        prioridade REAL DEFAULT 0,
        custo INTEGER DEFAULT 0,
     
        
        pontuacao_ranking REAL DEFAULT 0,
        criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Tabela de avaliação
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avaliacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_queixa INTEGER NOT NULL,
        id_conselheiro INTEGER NOT NULL,
        risco_seguranca INTEGER NOT NULL CHECK (risco_seguranca BETWEEN 1 AND 5),
        risco_integridade INTEGER NOT NULL CHECK (risco_integridade BETWEEN 1 AND 5),
        risco_bens INTEGER NOT NULL CHECK (risco_bens BETWEEN 1 AND 5),
        probabilidade INTEGER NOT NULL CHECK (probabilidade BETWEEN 1 AND 5),
        urgencia INTEGER NOT NULL CHECK (urgencia BETWEEN 1 AND 5),
        criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_queixa) REFERENCES queixas(id),
        FOREIGN KEY (id_conselheiro) REFERENCES conselheiros(id),
        UNIQUE (id_queixa, id_conselheiro)
    );
    """)
    
    
    # Tabela de risco segurança
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS risco_seguranca_opcoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor INTEGER NOT NULL,
    descricao TEXT NOT NULL
    );
    """)
    
    # Tabela de risco segurança
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS risco_integridade_opcoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor INTEGER NOT NULL,
    descricao TEXT NOT NULL
    );
    """)
    
        
    # Tabela de risco bens
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS risco_bens_opcoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor INTEGER NOT NULL,
    descricao TEXT NOT NULL
    );
    """)

        
    # Tabela de risco bens
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prioridades_opcoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor INTEGER NOT NULL,
    descricao TEXT NOT NULL
    );
    """) 
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS probabilidade_opcoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor INTEGER NOT NULL,
    descricao TEXT NOT NULL
    );
    """) 
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS custo_opcoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor INTEGER NOT NULL,
    descricao TEXT NOT NULL
    );
    """) 
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS percepcao_opcoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor INTEGER NOT NULL,
    descricao TEXT NOT NULL
    );
    """) 
    
    conn.commit()
    conn.close()

# Execute para criar o banco e tabelas:
criar_banco()
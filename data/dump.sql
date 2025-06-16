PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE conselheiros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        unidade TEXT,
        status TEXT NOT NULL,
        tipo TEXT NOT NULL,
        criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
    );
/****** CORRUPTION ERROR *******/
CREATE TABLE queixas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        media_risco_seguranca REAL DEFAULT 0,
        media_risco_integridade REAL DEFAULT 0,
        media_risco_bens REAL DEFAULT 0,
        media_probabilidade REAL DEFAULT 0,
        media_urgencia REAL DEFAULT 0,
        media_custo REAL DEFAULT 0,
        media_percepcao REAL DEFAULT 0,
        impacto_total REAL DEFAULT 0,
        media_ponderada REAL DEFAULT 0,
        pontuacao_ranking REAL DEFAULT 0,
        criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
    );
/****** CORRUPTION ERROR *******/
CREATE TABLE IF NOT EXISTS "avaliacoes" (
	"id"	INTEGER,
	"id_queixa"	INTEGER NOT NULL,
	"id_conselheiro"	INTEGER NOT NULL,
	"risco_seguranca"	INTEGER NOT NULL CHECK("risco_seguranca" BETWEEN 1 AND 5),
	"risco_integridade"	INTEGER NOT NULL CHECK("risco_integridade" BETWEEN 1 AND 5),
	"risco_bens"	INTEGER NOT NULL CHECK("risco_bens" BETWEEN 1 AND 5),
	"probabilidade"	INTEGER NOT NULL CHECK("probabilidade" BETWEEN 1 AND 5),
	"urgencia"	INTEGER NOT NULL CHECK("urgencia" BETWEEN 1 AND 5),
	"custo"	INTEGER NOT NULL CHECK("custo" BETWEEN 1 AND 5),
	"percepcao_moradores"	INTEGER NOT NULL CHECK("percepcao_moradores" BETWEEN 1 AND 5),
	"criado_em"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"conselheiro_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("id_queixa","id_conselheiro"),
	FOREIGN KEY("id_conselheiro") REFERENCES "conselheiros"("id"),
	FOREIGN KEY("id_queixa") REFERENCES "queixas"("id")
);
DELETE FROM sqlite_sequence;
/****** CORRUPTION ERROR *******/
ROLLBACK; -- due to errors

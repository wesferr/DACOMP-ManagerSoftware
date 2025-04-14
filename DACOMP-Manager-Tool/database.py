import sqlite3

def conectar():
    conn = sqlite3.connect("sistema_compras.db")
    cursor = conn.cursor()

    # Tabela de compras
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            local TEXT,
            data_encomenda DATE,
            data_recebimento DATE,
            valor_total REAL,
            chave_nota TEXT UNIQUE
        )
    """)

    # Tabela de produtos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_compra INTEGER,
            validade DATE,
            cod_barras TEXT UNIQUE,
            nome TEXT,
            valor_unit REAL,
            valor_venda REAL,
            FOREIGN KEY (id_compra) REFERENCES compras (id)
        )
    """)

    conn.commit()
    conn.close()

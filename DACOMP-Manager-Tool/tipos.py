import customtkinter as ctk
from tkinter import messagebox
import sqlite3

def criar_entradas(frame, label_txt, placeholder, base_row, col, mode=1):
    label = ctk.CTkLabel(frame, text=label_txt)
    label.grid(row=base_row, column=col, sticky="w", padx=5)
    entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
    if mode == 1:
        entry.insert(0, placeholder)
        entry.grid(row=base_row + 1, column=col, padx=0, pady=(0, 10), columnspan=2, sticky="we")
    else:
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
        entry.grid(row=0, column=col, padx=5, pady=5, sticky="we")
    return entry


class TelaTipos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Expansão das partes internas
        self.grid_columnconfigure(0, weight=1)  # Formulário
        self.grid_columnconfigure(1, weight=0)  # Lista lateral (tamanho fixo)
        self.incremental_widget()

        self.btn_voltar = ctk.CTkButton(self, text="Voltar para Compras", command=self.voltar)
        self.btn_voltar.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.botao_atualizar = ctk.CTkButton(self, text="Atualizar Produtos", command=self.atualizar_produtos)
        self.botao_atualizar.grid(row=2, column=0, padx=5, pady=5)

        self.frame_compras = ctk.CTkScrollableFrame(self, width=300, label_text="Itens da Compra")
        self.frame_compras.grid(row=1, column=0, columnspan=5, pady=10, sticky="nswe")
        self.atualizar_lista_compras()

    def voltar(self):
        self.destroy()
        self.master.abrir_tela_compras()

    def incremental_widget(self):
        self.frame_formulario = ctk.CTkFrame(self)
        self.frame_formulario.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

        self.nome_entry = criar_entradas(self.frame_formulario, "Tipo", "Digite o tipo de item", 1, 0, 0)
        self.valor_entry = criar_entradas(self.frame_formulario, "Valor", "Ex: 12.50", 1, 1, 0)

        self.botao_salvar = ctk.CTkButton(self.frame_formulario, text="Salvar Produto", command=self.salvar_produto)
        self.botao_salvar.grid(row=0, column=6)

        self.nome_entry.grid(row=0, column=0, padx=5, pady=5)
        self.valor_entry.grid(row=0, column=1, padx=5, pady=5)
        
    def recuperar_dados(self):
        conn = sqlite3.connect("sistema_compras.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipos")
        dados = cursor.fetchall()
        conn.close()
        return dados
    
    def atualizar_lista_compras(self):
        self.entries_produtos = []  # ← Adicionado para armazenar os dados editáveis
        # Limpa os botões antigos
        for widget in self.frame_compras.winfo_children():
            widget.destroy()

        dados = self.recuperar_dados()
        for i, dado in enumerate(dados):
            row_base = i * 2  # Espaço para label e entry

            id_tipo = dado[0]

            entry_nome = criar_entradas(self.frame_compras, "Produto", dado[1], row_base, 0)
            entry_valor = criar_entradas(self.frame_compras, "Valor Unitário", str(dado[2]), row_base, 2)

            # Botão para remover produto
            botao_remover = ctk.CTkButton(self.frame_compras, text="Remover", command=lambda id_tipo=id_tipo: self.remover_produto(id_tipo))
            botao_remover.grid(row=row_base + 1, column=14, padx=10, pady=(0,0), sticky="we")

            # Guarda os dados para atualização
            self.entries_produtos.append({
                "id": id_tipo,
                "tipo": entry_nome,
                "valor": entry_valor,
            })

    def salvar_produto(self):
        # Coloca valores padrão para itens não preenchidos]
        try:
            nome = self.nome_entry.get()
            valor = float(self.valor_entry.get() or "0.00")

            dados = (
                nome,
                valor,
            )
        
            conn = sqlite3.connect("sistema_compras.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tipos (tipo, valor)
                VALUES (?, ?)
            """, dados)
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Produto salvo com sucesso.")
            self.atualizar_lista_compras()
        except ValueError:
            messagebox.showerror("Erro", "Valor deve ser real")

        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Código de barras duplicado.")

    def atualizar_produtos(self):
        try:
            conn = sqlite3.connect("sistema_compras.db")
            cursor = conn.cursor()

            for item in self.entries_produtos:
                id_prod = item["id"]
                nome = item["tipo"].get()
                valor = float(item["valor"].get())

                cursor.execute("""
                    UPDATE tipos
                    SET tipo = ?, valor = ?
                    WHERE id = ?
                """, (nome, valor, id_prod))

            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Produtos atualizados com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar produtos: {e}")
        
    def remover_produto(self, id_produto):
        try:
            conn = sqlite3.connect("sistema_compras.db")
            cursor = conn.cursor()

            # Remove o produto da tabela 'produtos' usando o id
            cursor.execute("DELETE FROM tipos WHERE id = ?", (id_produto,))
            conn.commit()
            conn.close()

            # Atualiza a lista de produtos após a remoção
            self.atualizar_lista_compras()

            messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover produto: {e}")

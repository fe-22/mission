import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from datetime import datetime
import csv
import os

class ViagemOnibusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Viagem de Ônibus - Missões AdFidelidade")
        self.root.geometry("600x550")

        # Cabeçalho
        self.label_cabecalho = tk.Label(self.root, text="Controle de Viagens Missionárias-AdFidelidade", font=("Arial", 16, "bold"))
        self.label_cabecalho.pack(pady=10)

        # Frame para dados do motorista
        self.frame_motorista = tk.Frame(self.root)
        self.frame_motorista.pack(pady=10)

        # Labels e campos para dados do motorista
        tk.Label(self.frame_motorista, text="Nome do Motorista:").grid(row=0, column=0, sticky="w")
        self.entry_nome_motorista = tk.Entry(self.frame_motorista, width=50)
        self.entry_nome_motorista.grid(row=0, column=1)

        tk.Label(self.frame_motorista, text="Número da CNH:").grid(row=1, column=0, sticky="w")
        self.entry_numero_cnh = tk.Entry(self.frame_motorista, width=50)
        self.entry_numero_cnh.grid(row=1, column=1)

        tk.Label(self.frame_motorista, text="Validade do Curso:").grid(row=2, column=0, sticky="w")
        self.entry_validade_curso = tk.Entry(self.frame_motorista, width=50)
        self.entry_validade_curso.grid(row=2, column=1)

        # Frame para dados da viagem
        self.frame_viagem = tk.Frame(self.root)
        self.frame_viagem.pack(pady=10)

        # Labels e campos para dados da viagem
        tk.Label(self.frame_viagem, text="Data e Hora de Saída:").grid(row=0, column=0, sticky="w")
        self.entry_data_hora_saida = tk.Entry(self.frame_viagem, width=50)
        self.entry_data_hora_saida.grid(row=0, column=1)
        self.entry_data_hora_saida.insert(0, datetime.now().strftime("%d/%m/%Y %H:%M"))

        tk.Label(self.frame_viagem, text="Data e Hora de Chegada:").grid(row=1, column=0, sticky="w")
        self.entry_data_hora_chegada = tk.Entry(self.frame_viagem, width=50)
        self.entry_data_hora_chegada.grid(row=1, column=1)
        self.entry_data_hora_chegada.insert(0, datetime.now().strftime("%d/%m/%Y %H:%M"))

        tk.Label(self.frame_viagem, text="Destino:").grid(row=2, column=0, sticky="w")
        self.entry_destino = tk.Entry(self.frame_viagem, width=50)
        self.entry_destino.grid(row=2, column=1)

        tk.Label(self.frame_viagem, text="Litros Abastecidos:").grid(row=3, column=0, sticky="w")
        self.entry_litros_abastecidos = tk.Entry(self.frame_viagem, width=50)
        self.entry_litros_abastecidos.grid(row=3, column=1)

        tk.Label(self.frame_viagem, text="Avarias na Saída:").grid(row=4, column=0, sticky="w")
        self.text_avarias_saida = scrolledtext.ScrolledText(self.frame_viagem, width=50, height=3)
        self.text_avarias_saida.grid(row=4, column=1)

        tk.Label(self.frame_viagem, text="Avarias na Chegada:").grid(row=5, column=0, sticky="w")
        self.text_avarias_chegada = scrolledtext.ScrolledText(self.frame_viagem, width=50, height=3)
        self.text_avarias_chegada.grid(row=5, column=1)

        tk.Label(self.frame_viagem, text="Descrição de Falhas Mecânicas ou Elétricas:").grid(row=6, column=0, sticky="w")
        self.text_falhas = scrolledtext.ScrolledText(self.frame_viagem, width=50, height=5)
        self.text_falhas.grid(row=6, column=1)

        self.checklist_var = tk.BooleanVar()
        tk.Checkbutton(self.frame_viagem, text="Checklist realizado", variable=self.checklist_var).grid(row=7, columnspan=2)

        # Botão para salvar em CSV
        self.btn_salvar_csv = tk.Button(self.root, text="Salvar em CSV", command=self.salvar_csv)
        self.btn_salvar_csv.pack(pady=10)

        # Área de texto para exibir os últimos dados salvos
        self.text_ultimos_dados = scrolledtext.ScrolledText(self.root, width=80, height=10)
        self.text_ultimos_dados.pack(pady=10)

        # Rótulo para dados da igreja no rodapé
        self.label_igreja = tk.Label(self.root, text="Assembleia de Deus Fidelidade CNPJ 20.316.786/0001-68 - Rua Ernesta Pelosine,196 - Centro - SBC")
        self.label_igreja.pack(side="bottom", pady=5)

    def salvar_csv(self):
        try:
            dados_viagem = {
                "Nome do Motorista": self.entry_nome_motorista.get(),
                "Número da CNH": self.entry_numero_cnh.get(),
                "Validade do Curso": self.entry_validade_curso.get(),
                "Data e Hora de Saída": self.entry_data_hora_saida.get(),
                "Data e Hora de Chegada": self.entry_data_hora_chegada.get(),
                "Destino": self.entry_destino.get(),
                "Litros Abastecidos": self.entry_litros_abastecidos.get(),
                "Avarias na Saída": self.text_avarias_saida.get("1.0", tk.END).strip(),
                "Avarias na Chegada": self.text_avarias_chegada.get("1.0", tk.END).strip(),
                "Descrição de Falhas Mecânicas ou Elétricas": self.text_falhas.get("1.0", tk.END).strip(),
                "Checklist realizado": "Sim" if self.checklist_var.get() else "Não"
            }

            arquivo_csv = os.path.join(os.path.dirname(__file__), 'viagem_onibus.csv')

            with open(arquivo_csv, "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=dados_viagem.keys())

                if file.tell() == 0:
                    writer.writeheader()

                writer.writerow(dados_viagem)

            messagebox.showinfo("Sucesso", f"Dados da viagem foram salvos em {arquivo_csv}")

            # Atualizar área de texto com os últimos três conjuntos de dados salvos
            self.atualizar_ultimos_dados(arquivo_csv)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar os dados: {e}")

    def atualizar_ultimos_dados(self, arquivo_csv):
        try:
            # Ler os últimos três conjuntos de dados do arquivo CSV
            with open(arquivo_csv, "r") as file:
                reader = csv.DictReader(file)
                dados = [linha for linha in reader]

            # Selecionar os três últimos conjuntos de dados, se houver
            ultimos_tres = dados[-3:] if len(dados) >= 3 else dados

            # Formatar os dados para exibição
            texto_ultimos_dados = ""
            for linha in ultimos_tres:
                texto_linha = ", ".join([f"{chave}: {valor}" for chave, valor in linha.items()])
                texto_ultimos_dados += texto_linha + "\n\n"

            # Atualizar a área de texto com os últimos dados
            self.text_ultimos_dados.delete("1.0", tk.END)
            self.text_ultimos_dados.insert(tk.END, texto_ultimos_dados)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao atualizar os últimos dados: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ViagemOnibusApp(root)
    root.mainloop()

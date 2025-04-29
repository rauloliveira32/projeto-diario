import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from datetime import datetime
import os

ARQUIVO = os.path.join(os.getcwd(), "diario.txt")

def salvar_anotacao():
    texto = entrada_texto.get("1.0", tk.END).strip()
    if texto:
        try:
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            with open(ARQUIVO, "a", encoding="utf-8") as f:
                f.write(f"[{data_hora}] {texto}\n")
            entrada_texto.delete("1.0", tk.END)
            messagebox.showinfo("Salvo!", "Anotação salva com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar a anotação.\n{e}")
    else:
        messagebox.showwarning("Aviso", "A anotação está vazia!")

def mostrar_anotacoes():
    if not os.path.exists(ARQUIVO):
        messagebox.showinfo("Diário", "O diário ainda está vazio.")
        return

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            conteudo = f.readlines()

        janela_anotacoes = tk.Toplevel(root)
        janela_anotacoes.title("📔 Anotações Salvas")
        janela_anotacoes.configure(bg="#f0f0f0")

        lista_anotacoes = tk.Listbox(janela_anotacoes, width=100, height=20)
        lista_anotacoes.pack(padx=20, pady=20)

        for idx, linha in enumerate(conteudo):
            lista_anotacoes.insert(idx, linha.strip())

        def editar_anotacao():
            selecao = lista_anotacoes.curselection()
            if selecao:
                index = selecao[0]
                texto_atual = conteudo[index].split("] ", 1)[-1]
                novo_texto = simpledialog.askstring("Editar Anotação", "Edite sua anotação:", initialvalue=texto_atual)
                if novo_texto:
                    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    conteudo[index] = f"[{data_hora}] {novo_texto}\n"
                    with open(ARQUIVO, "w", encoding="utf-8") as f:
                        f.writelines(conteudo)
                    messagebox.showinfo("Editado", "Anotação editada com sucesso!")
                    janela_anotacoes.destroy()
                    mostrar_anotacoes()

        def apagar_anotacao():
            selecao = lista_anotacoes.curselection()
            if selecao:
                index = selecao[0]
                confirmar = messagebox.askyesno("Confirmar", "Tem certeza que deseja apagar esta anotação?")
                if confirmar:
                    del conteudo[index]
                    with open(ARQUIVO, "w", encoding="utf-8") as f:
                        f.writelines(conteudo)
                    messagebox.showinfo("Apagado", "Anotação apagada com sucesso!")
                    janela_anotacoes.destroy()
                    mostrar_anotacoes()

        frame_botoes = tk.Frame(janela_anotacoes, bg="#f0f0f0")
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text="Editar", command=editar_anotacao, bg="#ff9800", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botoes, text="Apagar", command=apagar_anotacao, bg="#f44336", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botoes, text="Fechar", command=janela_anotacoes.destroy, bg="#9e9e9e", fg="white", font=("Arial", 10, "bold"), width=15).pack(side=tk.LEFT, padx=10)

    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível carregar as anotações.\n{e}")

def buscar_anotacao():
    if not os.path.exists(ARQUIVO):
        messagebox.showinfo("Diário", "O diário ainda está vazio.")
        return

    palavra = simpledialog.askstring("Buscar", "Digite uma palavra para buscar:")
    if palavra:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            conteudo = f.readlines()

        resultados = [linha for linha in conteudo if palavra.lower() in linha.lower()]

        if resultados:
            resultado_texto = "".join(resultados)
            janela_resultados = tk.Toplevel(root)
            janela_resultados.title("🔍 Resultados da Busca")
            janela_resultados.configure(bg="#f0f0f0")

            texto_resultados = scrolledtext.ScrolledText(janela_resultados, width=70, height=20, font=("Arial", 10))
            texto_resultados.pack(padx=20, pady=20)
            texto_resultados.insert(tk.END, resultado_texto)
            texto_resultados.config(state=tk.DISABLED)

            tk.Button(janela_resultados, text="Fechar", command=janela_resultados.destroy, bg="#ff6b6b", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
        else:
            messagebox.showinfo("Busca", "Nenhuma anotação encontrada com essa palavra.")

def criar_interface():
    global entrada_texto, root

    root = tk.Tk()
    root.title("📘 Diário Moderno")
    root.geometry("600x500")
    root.configure(bg="#e0f7fa")
    root.resizable(False, False)

    tk.Label(root, text="Escreva sua anotação:", font=("Helvetica", 14, "bold"), bg="#e0f7fa").pack(pady=15)

    entrada_texto = scrolledtext.ScrolledText(root, width=70, height=10, font=("Arial", 10))
    entrada_texto.pack(pady=10)

    frame_botoes = tk.Frame(root, bg="#e0f7fa")
    frame_botoes.pack(pady=20)

    tk.Button(frame_botoes, text="Salvar Anotação", command=salvar_anotacao, bg="#4caf50", fg="white", font=("Arial", 10, "bold"), width=20).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botoes, text="Ver Anotações", command=mostrar_anotacoes, bg="#2196f3", fg="white", font=("Arial", 10, "bold"), width=20).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botoes, text="Buscar Anotação", command=buscar_anotacao, bg="#ff9800", fg="white", font=("Arial", 10, "bold"), width=20).pack(side=tk.LEFT, padx=10)

    root.mainloop()

if __name__ == "__main__":
    criar_interface()

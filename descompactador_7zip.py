import tkinter as tk
from tkinter import ttk  # Themed Tkinter widgets (melhor aparência)
from tkinter import filedialog, messagebox
import py7zr
import os
import threading  # Para executar a descompactação sem travar a interface

# --- Lógica de Descompactação (adaptada para GUI) ---
def descompactar_7zip(caminho_arquivo, diretorio_saida, senha, status_label, progress_bar, unzip_button):
    """
    Descompacta um arquivo .7z e atualiza a interface gráfica.

    Args:
        caminho_arquivo (str): Caminho para o arquivo .7z.
        diretorio_saida (str): Diretório de destino.
        senha (str or None): Senha do arquivo.
        status_label (tk.Label): Widget Label para exibir mensagens de status.
        progress_bar (ttk.Progressbar): Widget Progressbar para indicar atividade.
        unzip_button (ttk.Button): Botão de descompactar para desabilitar/habilitar.
    """
    try:
        # Atualiza a interface antes de começar
        status_label.config(text=f"Descompactando '{os.path.basename(caminho_arquivo)}'...")
        # Inicia barra de progresso indeterminada (animação)
        progress_bar.config(mode='indeterminate')
        progress_bar.start(10)
        unzip_button.config(state=tk.DISABLED) # Desabilita o botão

        # Abre o arquivo 7zip e extrai
        # O diretório de saída já foi verificado/criado na thread principal
        with py7zr.SevenZipFile(caminho_arquivo, mode='r', password=senha) as z:
            z.extractall(path=diretorio_saida)

        status_label.config(text="Arquivo descompactado com sucesso!")
        messagebox.showinfo("Sucesso", f"Arquivo '{os.path.basename(caminho_arquivo)}' descompactado com sucesso em:\n{os.path.abspath(diretorio_saida)}")

    except py7zr.exceptions.PasswordRequired:
        status_label.config(text="Erro: Senha necessária ou incorreta.")
        messagebox.showerror("Erro de Senha", "O arquivo está protegido por senha. Por favor, forneça a senha correta ou deixe em branco se não houver senha.")
    except py7zr.exceptions.Bad7zFile:
        status_label.config(text="Erro: Arquivo inválido/corrompido ou senha incorreta.")
        messagebox.showerror("Erro de Arquivo", f"O arquivo '{os.path.basename(caminho_arquivo)}' parece inválido, corrompido ou a senha está incorreta.")
    except Exception as e:
        status_label.config(text=f"Erro inesperado: {e}")
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro inesperado:\n{e}")
    finally:
        # Sempre para a barra de progresso, volta ao modo determinado e reabilita o botão
        progress_bar.stop()
        progress_bar.config(mode='determinate', value=0)
        unzip_button.config(state=tk.NORMAL)
        # Mantém a última mensagem de status ou erro visível até nova ação

# --- Funções da Interface Gráfica ---
def browse_file(entry_widget):
    """Abre um diálogo para selecionar o arquivo .7z"""
    filepath = filedialog.askopenfilename(
        title="Selecionar Arquivo .7z",
        filetypes=(("Arquivos 7-Zip", "*.7z"), ("Todos os arquivos", "*.*"))
    )
    if filepath:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filepath)

def browse_directory(entry_widget):
    """Abre um diálogo para selecionar o diretório de saída"""
    dirpath = filedialog.askdirectory(
        title="Selecionar Diretório de Saída"
    )
    if dirpath:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, dirpath)

def start_unzip_thread(file_entry, dir_entry, password_entry, status_label, progress_bar, unzip_button):
    """Inicia a descompactação em uma thread separada para não travar a GUI"""
    arquivo_7z = file_entry.get()
    diretorio_destino = dir_entry.get()
    senha = password_entry.get()
    senha = senha if senha else None # Converte string vazia para None

    # Validações básicas antes de iniciar a thread
    if not arquivo_7z:
        messagebox.showerror("Erro de Entrada", "Por favor, selecione um arquivo .7z para descompactar.")
        return
    if not os.path.exists(arquivo_7z):
         messagebox.showerror("Erro de Arquivo", f"O arquivo selecionado não foi encontrado:\n{arquivo_7z}")
         return
    if not diretorio_destino:
        messagebox.showerror("Erro de Entrada", "Por favor, selecione um diretório de destino para extrair os arquivos.")
        return

    # Tenta criar o diretório de destino se ele não existir (antes de passar para a thread)
    try:
        # Verifica se o caminho de destino é válido e tenta criar
        if not os.path.isdir(diretorio_destino):
             # Se o caminho existe mas não é um diretório, é um erro
             if os.path.exists(diretorio_destino):
                 messagebox.showerror("Erro de Diretório", f"O caminho de destino especificado existe, mas não é um diretório:\n{diretorio_destino}")
                 return
             # Se não existe, tenta criar
             os.makedirs(diretorio_destino, exist_ok=True)
             print(f"Diretório de destino criado: {diretorio_destino}") # Log opcional
    except OSError as e:
        messagebox.showerror("Erro de Diretório", f"Não foi possível criar ou acessar o diretório de destino:\n{diretorio_destino}\n\nErro: {e}")
        return
    except Exception as e:
         messagebox.showerror("Erro de Diretório", f"Ocorreu um erro ao verificar o diretório de destino:\n{e}")
         return


    # Cria e inicia a thread para descompactar
    thread = threading.Thread(
        target=descompactar_7zip,
        args=(arquivo_7z, diretorio_destino, senha, status_label, progress_bar, unzip_button),
        daemon=True # Permite que o programa feche mesmo se a thread estiver rodando
    )
    thread.start()

# --- Criação da Janela Principal e Widgets ---
def create_gui():
    window = tk.Tk()
    window.title("Descompactador 7-Zip (GUI)")
    # window.geometry("550x300") # Tamanho inicial (opcional, ajuste conforme necessário)
    window.resizable(False, False) # Impede redimensionamento

    # Estilo ttk (opcional, pode melhorar a aparência em alguns sistemas)
    style = ttk.Style()
    # print(style.theme_names()) # Descomente para ver temas disponíveis
    # style.theme_use('clam') # Ex: 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'

    # --- Frame Principal com Padding ---
    main_frame = ttk.Frame(window, padding="15 15 15 15") # Aumenta o padding
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    # Configura as colunas do grid dentro do frame para expandir
    main_frame.columnconfigure(0, weight=1) # Coluna do Entry expande
    main_frame.columnconfigure(1, weight=0) # Coluna do botão não expande

    # --- Seleção de Arquivo ---
    ttk.Label(main_frame, text="Arquivo .7z:").grid(column=0, row=0, columnspan=2, sticky=tk.W)
    file_entry = ttk.Entry(main_frame, width=60) # Aumenta largura
    file_entry.grid(column=0, row=1, sticky=(tk.W, tk.E), padx=(0, 5))
    file_button = ttk.Button(main_frame, text="Procurar...", command=lambda: browse_file(file_entry))
    file_button.grid(column=1, row=1, sticky=tk.E) # Alinha à direita

    # --- Seleção de Diretório ---
    ttk.Label(main_frame, text="Extrair para:").grid(column=0, row=2, columnspan=2, sticky=tk.W, pady=(10, 0)) # Espaço acima
    dir_entry = ttk.Entry(main_frame, width=60) # Aumenta largura
    dir_entry.grid(column=0, row=3, sticky=(tk.W, tk.E), padx=(0, 5))
    # LINHA REMOVIDA: dir_entry.insert(0, ".")
    dir_button = ttk.Button(main_frame, text="Procurar...", command=lambda: browse_directory(dir_entry))
    dir_button.grid(column=1, row=3, sticky=tk.E) # Alinha à direita

    # --- Senha ---
    ttk.Label(main_frame, text="Senha (se houver):").grid(column=0, row=4, columnspan=2, sticky=tk.W, pady=(10, 0)) # Espaço acima
    password_entry = ttk.Entry(main_frame, width=30, show="*") # Esconde a senha
    password_entry.grid(column=0, row=5, sticky=tk.W) # Alinha à esquerda

    # --- Botão Descompactar ---
    unzip_button_frame = ttk.Frame(main_frame) # Frame para centralizar o botão
    unzip_button_frame.grid(column=0, row=6, columnspan=2, pady=(20, 10)) # Espaço acima e abaixo
    unzip_button = ttk.Button(unzip_button_frame, text="Descompactar", width=20) # Botão mais largo
    unzip_button.pack() # Centraliza no frame

    # --- Barra de Progresso e Status ---
    progress_bar = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
    progress_bar.grid(column=0, row=7, columnspan=2, pady=(5, 2), sticky=(tk.W, tk.E))
    status_label = ttk.Label(main_frame, text="Pronto.", relief=tk.SUNKEN, anchor=tk.W, padding=(5,2)) # Estilo sunken e padding
    status_label.grid(column=0, row=8, columnspan=2, sticky=(tk.W, tk.E))

    # --- Vincula a ação ao botão ---
    unzip_button.config(command=lambda: start_unzip_thread(
        file_entry, dir_entry, password_entry, status_label, progress_bar, unzip_button
    ))

    # Adiciona padding vertical a todos os widgets dentro do frame principal (exceto o botão no seu próprio frame)
    for i, child in enumerate(main_frame.winfo_children()):
        if i < len(main_frame.winfo_children()) - 3: # Não aplica ao frame do botão, barra e status
           child.grid_configure(pady=3)

    # Define foco inicial (opcional)
    file_entry.focus()

    window.mainloop()

# --- Ponto de Entrada ---
if __name__ == "__main__":
    # Assegura que a biblioteca py7zr está instalada (opcional, mas bom para feedback)
    try:
        import py7zr
    except ImportError:
        # Tenta mostrar um erro gráfico se o Tkinter estiver disponível
        try:
            root = tk.Tk()
            root.withdraw() # Esconde a janela principal vazia
            messagebox.showerror("Erro de Dependência",
                                 "A biblioteca 'py7zr' necessária não está instalada.\n\n"
                                 "Por favor, instale usando o comando:\n"
                                 "pip install py7zr\n\n"
                                 "O programa será encerrado.")
        except tk.TclError:
            # Fallback para console se Tkinter falhar
            print("Erro Crítico: A biblioteca 'py7zr' não está instalada.")
            print("Por favor, instale usando: pip install py7zr")
        exit(1) # Sai com código de erro

    # Cria e executa a interface gráfica
    create_gui()
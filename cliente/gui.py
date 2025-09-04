import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import webbrowser # <--- 1. IMPORTE A BIBLIOTECA WEBBROWSER

# Importa as funções e a URL do servidor do módulo de API
# <--- 2. IMPORTE A CONSTANTE SERVER_URL
from client_api import upload_video, get_video_history, SERVER_URL 
from utils import play_video_from_url

class VideoClientApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cliente de Processamento de Vídeo")
        self.geometry("800x600")

        self.selected_file_path = tk.StringVar()
        self.selected_filter = tk.StringVar(value='grayscale')

        # --- Frame de Upload ---
        upload_frame = ttk.LabelFrame(self, text="Enviar Novo Vídeo", padding="10")
        upload_frame.pack(fill="x", padx=10, pady=10)

        # Configura o grid para expandir
        upload_frame.columnconfigure(1, weight=1)

        ttk.Label(upload_frame, text="Arquivo:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(upload_frame, textvariable=self.selected_file_path, width=50, state="readonly").grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        ttk.Button(upload_frame, text="Selecionar Arquivo...", command=self.select_file).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(upload_frame, text="Filtro:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        filter_options = ['grayscale', 'pixelize', 'edges']
        ttk.Combobox(upload_frame, textvariable=self.selected_filter, values=filter_options, state="readonly").grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # --- 3. ADIÇÃO E POSICIONAMENTO DOS BOTÕES ---
        # Cria um frame interno para os botões de ação
        action_buttons_frame = ttk.Frame(upload_frame)
        action_buttons_frame.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="e")

        ttk.Button(action_buttons_frame, text="Enviar Vídeo", command=self.upload_selected_video).pack(side="left", padx=(0, 5))
        
        # O novo botão que abre o navegador
        ttk.Button(action_buttons_frame, text="Ver Histórico no Navegador", command=self.open_history_in_browser).pack(side="left")
        
        self.progress_bar = ttk.Progressbar(upload_frame, orient='horizontal', mode='determinate')
        self.progress_bar.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=10)

        # --- Frame de Histórico ---
        # ... (o resto do arquivo continua exatamente igual) ...
        history_frame = ttk.LabelFrame(self, text="Histórico de Vídeos", padding="10")
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.history_tree = ttk.Treeview(
            history_frame, 
            columns=("name", "filter", "date", "duration", "actions"),
            show="headings"
        )
        self.history_tree.heading("name", text="Nome Original")
        self.history_tree.heading("filter", text="Filtro")
        self.history_tree.heading("date", text="Data")
        self.history_tree.heading("duration", text="Duração (s)")
        self.history_tree.heading("actions", text="Ações")

        self.history_tree.column("name", width=200)
        self.history_tree.column("filter", width=80, anchor="center")
        self.history_tree.column("date", width=150, anchor="center")
        self.history_tree.column("duration", width=80, anchor="center")
        self.history_tree.column("actions", width=200, anchor="center")
        
        self.history_tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.video_data = {}
        self.history_tree.bind("<Double-1>", self.on_item_double_click)
        self.refresh_history()

    # --- 4. CRIAÇÃO DA FUNÇÃO CHAMADA PELO BOTÃO ---
    def open_history_in_browser(self):
        """Abre a página principal do servidor no navegador padrão."""
        try:
            print(f"Abrindo a URL do servidor: {SERVER_URL}")
            webbrowser.open(SERVER_URL)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o navegador: {e}")

    def select_file(self):
        # ... (resto do seu código, sem alterações)
        file_path = filedialog.askopenfilename(
            title="Selecione um vídeo",
            filetypes=(("Arquivos de Vídeo", "*.mp4 *.avi *.mov"), ("Todos os arquivos", "*.*"))
        )
        if file_path:
            self.selected_file_path.set(file_path)

    def update_progress(self, value):
        self.progress_bar['value'] = value
        self.update_idletasks()

    def upload_selected_video(self):
        # ... (resto do seu código, sem alterações)
        file_path = self.selected_file_path.get()
        if not os.path.exists(file_path):
            messagebox.showerror("Erro", "Arquivo selecionado não encontrado.")
            return

        filter_name = self.selected_filter.get()
        
        self.update_progress(0)
        messagebox.showinfo("Upload", "O upload foi iniciado. Por favor, aguarde.")

        response = upload_video(file_path, filter_name, self.update_progress)

        if response and 'error' in response:
            messagebox.showerror("Erro no Upload", response['error'])
        else:
            messagebox.showinfo("Sucesso", "Vídeo enviado e processado com sucesso!")
            self.refresh_history()
        
        self.update_progress(0)

    def refresh_history(self):
        # ... (resto do seu código, sem alterações)
        for i in self.history_tree.get_children():
            self.history_tree.delete(i)
        
        self.video_data = {}
        history = get_video_history()
        
        for video in history:
            video_id = video['id']
            name = f"{video['original_name']}.{video['original_ext']}"
            duration = f"{video['duration_sec']:.2f}" if video['duration_sec'] else "N/A"
            date = video['created_at'].split("T")[0]
            
            item_id = self.history_tree.insert(
                "", "end", iid=video_id,
                values=(name, video['filter'], date, duration, "Clique duplo para ver")
            )
            self.video_data[video_id] = video


    def on_item_double_click(self, event):
        """Lida com o clique duplo em um item do histórico para exibir os vídeos."""
        # Pega o ID do item selecionado na árvore
        selection = self.history_tree.selection()
        if not selection:
            return
            
        item_id = selection[0]
        if not item_id or item_id not in self.video_data:
            return
            
        video_info = self.video_data[item_id]
        
        # Cria a janela pop-up
        popup = tk.Toplevel(self)
        popup.title(f"Ver Vídeo: {video_info['original_name']}")
        popup.geometry("300x150")
        
        ttk.Label(popup, text="Escolha qual versão assistir:", font=("", 12)).pack(pady=10)
        
        # --- INÍCIO DA CORREÇÃO ---
        # Adiciona o prefixo '/media/' na construção da URL para corresponder à rota do Flask.
        original_url = f"{SERVER_URL}/media/{video_info['path_original'].replace(os.sep, '/')}"
        processed_url = f"{SERVER_URL}/media/{video_info['path_processed'].replace(os.sep, '/')}"
        # --- FIM DA CORREÇÃO ---

        print(f"URL Original: {original_url}") # Adicionado para depuração
        print(f"URL Processada: {processed_url}") # Adicionado para depuração

        ttk.Button(popup, text="Assistir Original", command=lambda: play_video_from_url(original_url)).pack(pady=5, fill="x", padx=20)
        ttk.Button(popup, text="Assistir Processado", command=lambda: play_video_from_url(processed_url)).pack(pady=5, fill="x", padx=20)


if __name__ == "__main__":
    app = VideoClientApp()
    app.mainloop()
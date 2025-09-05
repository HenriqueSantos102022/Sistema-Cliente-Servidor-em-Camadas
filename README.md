# Sistema Cliente/Servidor de Processamento de Vídeos

Este projeto consiste em um sistema cliente/servidor desenvolvido em Python, projetado para realizar o upload, processamento e visualização de vídeos. O sistema é dividido em uma aplicação cliente com interface gráfica construída em Tkinter e um servidor backend utilizando Flask e OpenCV para manipulação dos vídeos.

O cliente permite que o usuário selecione um arquivo de vídeo, escolha um filtro de processamento e o envie para o servidor. O servidor, por sua vez, aplica o filtro, armazena o vídeo original e o processado de forma organizada, e registra seus metadados. O histórico de vídeos pode ser consultado tanto pela interface do cliente quanto por uma página web gerada pelo servidor.

## Capturas de Tela

| Aplicação Cliente (Tkinter) | Página Web do Servidor (Histórico) |
| :-------------------------: | :--------------------------------: |
| ![Imagem do App Cliente](<img width="993" height="783" alt="Captura de tela 2025-09-04 170229" src="https://github.com/user-attachments/assets/b14200b1-48b2-4c02-bb00-ff25d9ef94a9" />
) | ![Servidor exibindo histórico](<img width="734" height="586" alt="Captura de tela 2025-09-04 170306" src="https://github.com/user-attachments/assets/621dbc32-618f-4c69-8372-55ef946f307f" />
) |

## Arquitetura

O projeto foi desenvolvido seguindo uma arquitetura de três camadas, garantindo a separação de responsabilidades e a modularidade do código.
* **Cliente (Tkinter):** Uma interface gráfica de desktop responsável pela interação com o usuário, seleção de arquivos e comunicação com o servidor via API HTTP.
* **Servidor (Flask + OpenCV):** Um servidor web que expõe uma API para receber os vídeos, aplica os filtros de processamento com OpenCV, gerencia o armazenamento dos arquivos e serve uma interface web com o histórico.
* **Banco de Dados (SQLite):** Um banco de dados leve para armazenar os metadados de cada vídeo processado, como nome, duração, filtro aplicado e caminhos dos arquivos.

### Estrutura de Diretórios

O código-fonte está organizado da seguinte forma:

```bash
projeto/
├─ cliente/
│  ├─ gui.py              # Interface gráfica Tkinter
│  ├─ client_api.py       # Funções para comunicação com o servidor
│  └─ utils.py            # Funções auxiliares (ex: abrir player de vídeo)
│
├─ servidor/
│  ├─ app.py              # Inicialização do Flask e rotas principais
│  ├─ video_processor.py  # Lógica de processamento de vídeo com OpenCV
│  ├─ storage.py          # Gerenciamento do armazenamento em disco
│  ├─ database.py         # Operações com o banco de dados SQLite
│  ├─ utils.py            # Funções auxiliares do servidor (UUID, etc.)
│  └─ templates/
│     └─ index.html      # Página web para visualização do histórico
│
├─ media/                  # Diretório raiz para todos os vídeos (criado em tempo de execução) 
│
└─ requirements.txt        # Dependências do projeto
```

## Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Servidor:** Flask
* **Interface Cliente:** Tkinter
* **Processamento de Vídeo:** OpenCV
* **Banco de Dados:** SQLite

## Instruções de Execução

Siga os passos abaixo para configurar e executar o sistema.

### Pré-requisitos
* Python 3.8 ou superior
* Pip (gerenciador de pacotes do Python)

### 1. Clonar o Repositório (se aplicável)
```bash
git clone <url_do_repositorio>
```

### 2. Instalar as Dependências

Abra um terminal na pasta raiz do projeto e execute o seguinte comando para instalar todas as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 3. Execução em um Único Computador (Local)

a) Iniciar o Servidor:
Execute o seguinte comando no terminal. O servidor estará disponível em http://127.0.0.1:5000

```bash
python -m servidor.app
```

b) Iniciar o Cliente:
Abra um novo terminal, navegue até a mesma pasta e execute:

```bash
python cliente/gui.py
```

### 4. Execução em Computadores Distintos (Rede Local) 

Para que o cliente e o servidor se comuniquem em máquinas diferentes na mesma rede:

a) No Computador do Servidor:

* Descubra o endereço IP local da máquina (no Windows, use ipconfig; no macOS/Linux, use ifconfig ou ip addr). O IP geralmente se parece com 192.168.x.x.

* Configure o firewall do sistema operacional para permitir conexões de entrada na porta TCP 5000.

* Inicie o servidor como no passo anterior: python -m servidor.app.

b) No Computador do Cliente:

* Abra o arquivo cliente/client_api.py.

* Altere a variável SERVER_URL, substituindo 127.0.0.1 pelo endereço IP do servidor.


```bash
Exemplo de alteração
SERVER_URL = "http://192.168.1.10:5000"
cd projeto/
```

Inicie o cliente: python cliente/gui.py.

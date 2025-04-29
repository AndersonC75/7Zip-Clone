# 7Zip-Clone
# Descompactador 7-Zip com Interface Gráfica (Python/Tkinter)

Uma aplicação simples com interface gráfica (GUI) desenvolvida em Python para descompactar arquivos no formato `.7z`. Utiliza a biblioteca `tkinter` para a interface e `py7zr` para a manipulação dos arquivos compactados.

![7zip-clone](https://github.com/user-attachments/assets/f529e090-1dfc-4774-bd53-9f3f2d5ca89c)

## Funcionalidades

*   **Interface Gráfica Amigável:** Fácil de usar, mesmo para usuários não técnicos.
*   **Seleção de Arquivo:** Permite navegar e selecionar o arquivo `.7z` desejado.
*   **Seleção de Destino:** Permite navegar e selecionar a pasta onde os arquivos serão extraídos.
*   **Suporte a Senha:** Campo para inserir a senha caso o arquivo `.7z` esteja protegido.
*   **Feedback Visual:**
    *   Barra de progresso (indeterminada) indica que a operação está em andamento.
    *   Mensagens de status informam o progresso e o resultado (sucesso ou erro).
    *   Alertas pop-up para confirmações e erros.
*   **Responsividade:** A descompactação ocorre em uma thread separada para evitar que a interface do usuário congele durante o processo.
*   **Portabilidade:** Pode ser facilmente compilado em um executável `.exe` para Windows usando PyInstaller.

## Tecnologias Utilizadas

*   **Python 3.x**
*   **Tkinter:** Biblioteca padrão do Python para criação de interfaces gráficas.
*   **py7zr:** Biblioteca para trabalhar com arquivos `.7z` (ler, escrever, extrair).
*   **Threading:** Módulo do Python para execução de tarefas em paralelo (evita congelamento da GUI).
*   **(Opcional) PyInstaller:** Ferramenta para empacotar a aplicação Python em um executável independente.

## Como Usar

Existem duas formas principais de usar esta aplicação:

**1. Executando o Script Python (.py):**

*   **Pré-requisitos:**
    *   Python 3 instalado (verifique com `python --version`).
    *   Biblioteca `py7zr` instalada. Se não tiver, instale via pip:
        ```bash
        pip install py7zr
        ```
*   **Execução:**
    1.  Clone ou baixe este repositório.
    2.  Navegue até a pasta do projeto pelo terminal ou prompt de comando.
    3.  Execute o script:
        ```bash
        python descompactador_gui.py
        ```
    4.  A interface gráfica será aberta. Use os botões "Procurar..." para selecionar o arquivo `.7z` e o diretório de destino, digite a senha (se necessário) e clique em "Descompactar".

**2. Usando o Executável (.exe) (Windows):**

*   **Pré-requisitos:** Nenhum (o `.exe` é independente).
*   **Execução:**
    1.  Baixe o arquivo `.exe` da seção [Releases](https://github.com/SEU_USUARIO/SEU_REPOSITORIO/releases) deste repositório (se você o disponibilizou lá) ou gere-o você mesmo (veja abaixo).
    2.  Dê um duplo clique no arquivo `.exe` para iniciar a aplicação.
    3.  Use a interface gráfica conforme descrito acima.
    *   **Nota:** Alguns antivírus podem sinalizar executáveis criados com PyInstaller como suspeitos (falso positivo). Se você compilou o código a partir desta fonte confiável, geralmente é seguro permitir a execução.

## Como Gerar o Executável (.exe)

Se desejar criar o arquivo `.exe` você mesmo:

1.  **Instale o PyInstaller:**
    ```bash
    pip install pyinstaller
    ```
2.  **Navegue até a pasta** onde o script `descompactador_gui.py` está localizado usando o terminal.
3.  **Execute o comando do PyInstaller:**
    ```bash
    pyinstaller --onefile --windowed --name "Descompactador7ZipGUI" descompactador_gui.py
    ```
    *   `--onefile`: Cria um único arquivo executável.
    *   `--windowed`: Impede que um console (janela preta) seja aberto junto com a GUI.
    *   `--name "Descompactador7ZipGUI"`: Define o nome do arquivo `.exe` gerado.
    *   *(Opcional)* `--icon="caminho/para/seu_icone.ico"`: Adiciona um ícone personalizado ao `.exe`.
4.  O arquivo `Descompactador7ZipGUI.exe` estará localizado na subpasta `dist` criada pelo PyInstaller.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir *issues* para relatar bugs ou sugerir melhorias, ou enviar *pull requests* com suas implementações.

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` (se você adicionar um) para mais detalhes.

import customtkinter as ctk
import pandas as pd
import os



# Inicializa a aplicação
app = ctk.CTk()
app.geometry('600x500')

# Variáveis globais
file_path = ctk.StringVar()
df = None
column_dropdown = ctk.CTkComboBox(app)  

# Função para carregar o arquivo Excel
def print_nome():
    global df
    filename = ctk.filedialog.askopenfilename()
    if filename:
        file_path.set(filename)
        name = os.path.basename(filename)  # Utiliza os.path.basename para obter o nome do arquivo
        label.configure(text=f"Arquivo selecionado -> {name}")
        try:
            df = pd.read_excel(filename)
            update_column_dropdown()
        except Exception as e:
            print(f"Erro ao ler o arquivo Excel: {e}")

# Atualiza os ComboBoxes com as colunas do DataFrame
def update_column_dropdown():
    global df
    column_dropdown.configure(values=list(df.columns))

# Abre uma janela modal para selecionar as colunas
def abrir_janela_modal():
    global df

    root = ctk.CTkToplevel()
    root.title("Selecionar Colunas")
    root.geometry('400x400')
    root.lift()
    root.attributes('-topmost', True)

    colunas = list(df.columns)
    coluna_aluno = ctk.StringVar()
    coluna_responsavel = ctk.StringVar()
    coluna_telefone = ctk.StringVar()

    # Aluno
    label_aluno = ctk.CTkLabel(root, text="Selecione a coluna com os NOMES DOS ALUNOS")
    label_aluno.pack(pady=(2))

    dropdown_aluno = ctk.CTkComboBox(root, values=colunas, variable=coluna_aluno)
    dropdown_aluno.pack(pady=10)

    label_nomes = ctk.CTkLabel(root, text="Selecione a coluna com os NOMES DOS RESPONSÁVEIS")
    label_nomes.pack(pady=(2))

    dropdown_nome = ctk.CTkComboBox(root, values=colunas, variable=coluna_responsavel)
    dropdown_nome.pack(pady=10)

    label_numeros = ctk.CTkLabel(root, text="Selecione a coluna com os NUMEROS DOS RESPONSÁVEIS")
    label_numeros.pack(pady=(2))

    dropdown_telefone = ctk.CTkComboBox(root, values=colunas, variable=coluna_telefone)
    dropdown_telefone.pack(pady=10)


    botao_confirmar = ctk.CTkButton(root, text="Confirmar", command=lambda: [root.destroy(), atualizar_rotulos(coluna_aluno.get(),coluna_responsavel.get(), coluna_telefone.get())])
    botao_confirmar.pack(pady=10)

    root.mainloop()

# Atualiza os rótulos na janela principal com os dados selecionados
def atualizar_rotulos(coluna_aluno,coluna_responsavel, coluna_telefone):
    # Assumindo que você quer exibir o primeiro valor de cada coluna
    label_aluno_selecionado.configure(text=f"Aluno: {df[coluna_aluno].values[0]}")
    label_responsavel_selecionado.configure(text=f"Responsavel: {df[coluna_responsavel].values[0]}")
    label_telefone_selecionado.configure(text=f"Telefone: {df[coluna_telefone].values[0]}")


# Elementos da interface principal
label_arquivo = ctk.CTkLabel(app, text="Selecione o arquivo excel com as informações dos contatos:")
label_arquivo.pack(pady=(10,2))

button = ctk.CTkButton(master=app, text="Selecione o arquivo", command=print_nome)
button.pack(pady=(5))

label = ctk.CTkLabel(master=app, text="Nome do arquivo:")
label.pack(pady=0)

botao_selecionar_coluna = ctk.CTkButton(app, text="Selecionar Colunas", command=abrir_janela_modal)
botao_selecionar_coluna.pack(pady=(30,10))


label_print_exemplos = ctk.CTkLabel(app, text="Verifique se os valores exemplo correspondem às colunas selecionadas:")
label_print_exemplos.pack(pady=(10,5))


label_aluno_selecionado = ctk.CTkLabel(app, text="Aluno:")
label_aluno_selecionado.pack(pady=(0,5))

label_responsavel_selecionado = ctk.CTkLabel(app, text="Responsavel:")
label_responsavel_selecionado.pack(pady=(0,5))

label_telefone_selecionado = ctk.CTkLabel(app, text="Telefone:")
label_telefone_selecionado.pack(pady=(5,10))


def rodar_tudo():
    # df = df[[coluna_responsavel,coluna_telefone]]
    # df = df.rename(columns={coluna_responsavel: 'nome', coluna_telefone: 'telefone'})
    
    pass
    

button_2 = ctk.CTkButton(master=app, text="Iniciar Automação !!!", command=rodar_tudo)
button_2.pack(pady=(40))


app.mainloop()



# coluna_responsavel='Responsável'
# coluna_telefone='Telefone'


# df = pd.read_excel(r'C:\Users\Prange\Downloads\Busca Ativa Joaquim.xlsx')

# df = df[[coluna_responsavel,coluna_telefone]]
# df = df.rename(columns={coluna_responsavel: 'nome', coluna_telefone: 'telefone'})


# df
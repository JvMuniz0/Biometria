import tkinter as tk

from db_components.db_control import BancoDados
from biometria_components.biometria_control import processamento_fingerprint
from pathlib import Path
from tkinter import ttk, messagebox, filedialog

#Global Vars
USER_NAME = ''
USER_ROLE = ''
USER_HASH = ''

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(
    r'C:\Users\Joao Vitor\Downloads\APS-Biometria-main\assets\frame0'
)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class MainWindow(tk.Tk):
    """Main Window"""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.title('Ministerio do Meio Ambiente')
        self.geometry('700x550')
        self.resizable(width=False, height=False)

        self.frames = {}

        for F in (CadastroScreen, LoginScreen, ConsultaScreen, InserirScreen, DeletarScreen):
            frame = F(container, self)
            frame.grid_remove()
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=(tk.E + tk.W + tk.N + tk.S))

        self.show_frame(LoginScreen)

    def show_frame(self, cont):
            frame = self.frames[cont]
            frame.tkraise()

class LoginScreen(tk.Frame):
    """Janela Inicial da aplicação"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Canvas Principal
        self.canvas = tk.Canvas(
            self,
            bg='#FFFFFF',
            height=550,
            width=700,
            bd=0,
            highlightthickness=0,
            relief='ridge',
        )
        self.canvas.grid(row=0, column=0, sticky=(tk.E + tk.W + tk.N + tk.S))

        # Imagem fundo
        self.imagem_imagem_fundo = tk.PhotoImage(
            file=relative_to_assets('image_fundo.png')
        )
        self.imagem_fundo = self.canvas.create_image(
            350.0, 275.0, image=self.imagem_imagem_fundo
        )
        # Imagem do GOV
        self.imagem_imagem_gov = tk.PhotoImage(
            file=relative_to_assets('image_gov.png')
        )
        self.image_gov = self.canvas.create_image(
            600.5282287597656, 492.2825622558594, image=self.imagem_imagem_gov
        )
        # Imagem da Logo
        self.imagem_imagem_logo = tk.PhotoImage(
            file=relative_to_assets('image_logo.png')
        )
        self.image_logo = self.canvas.create_image(
            170.0, 47.0, image=self.imagem_imagem_logo
        )
        # Texto principal - Ministerio
        self.canvas.create_text(
            195.0,
            42.0,
            anchor='nw',
            text='MINISTERIO DO MEIO AMBIENTE',
            fill='#1E1E1E',
            font=('Poppins ExtraBold', 20 * -1),
        )
        # Area do formulario
        self.canvas.create_rectangle(
            214.0, 110.0, 487.0, 504.0, fill='#EFEFEF', outline='#DDDDDD'
        )
        # Insert e Icon Login
        self.image_icon_user = tk.PhotoImage(
            file=relative_to_assets('icon_user.png')
        )
        self.icon_user = self.canvas.create_image(
            245.0452880859375, 140.5, image=self.image_icon_user
        )
        self.canvas.create_text(
            255,
            134,
            anchor='nw',
            text='Login',
            fill='#000000',
            font=('Poppins Regular', 13 * -1),
        )
        self.entry_image_login = tk.PhotoImage(
            file=relative_to_assets('entry_small.png')
        )
        self.entry_bg_login = self.canvas.create_image(
            350.5, 175.5, image=self.entry_image_login
        )
        self.entry_login = tk.Entry(
            self.canvas, bd=0, bg='#FFFFFF', fg='#000716', highlightthickness=0
        )
        self.entry_login.place(
            x=244.80000019073486,
            y=161,
            width=211.39999961853027,
            height=30,
        )
        # Insert e Icon de Senha
        self.image_icon_key = tk.PhotoImage(
            file=relative_to_assets('icon_key.png')
        )
        self.icon_key = self.canvas.create_image(
            244.00000762939453, 220.5, image=self.image_icon_key
        )
        self.canvas.create_text(
            255,
            214,
            anchor='nw',
            text='Senha',
            fill='#000000',
            font=('Poppins Regular', 13 * -1),
        )
        self.entry_image_senha = tk.PhotoImage(
            file=relative_to_assets('entry_small.png')
        )
        self.entry_bg_senha = self.canvas.create_image(
            349.5782012939453, 258.9906311035156, image=self.entry_image_senha
        )
        self.entry_senha = tk.Entry(
            self.canvas, bd=0, bg='#FFFFFF', fg='#000716', highlightthickness=0
        )
        self.entry_senha.place(
            x=243.87820148468018,
            y=244,
            width=211.39999961853027,
            height=30,
        )
        # Botão 'Esqueci minha senha'
        self.button_image_esqueci = tk.PhotoImage(
            file=relative_to_assets('button_esqueci.png')
        )
        self.button_esqueci = tk.Button(
            self.canvas,
            image=self.button_image_esqueci,
            borderwidth=0,
            highlightthickness=0,
            relief='flat',
            command=lambda: print('botao esqueci senha foi clicado'),
        )
        self.button_esqueci.place(
            x=239.0452880859375, y=282.4906311035156, width=107.0, height=15.0
        )
        # Botão de Entrar
        self.button_image_entrar = tk.PhotoImage(
            file=relative_to_assets('button_entrar.png')
        )
        self.button_entrar = tk.Button(
            self.canvas,
            image=self.button_image_entrar,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_entrar_func(controller),
            relief='flat',
        )
        self.button_entrar.place(
            x=238.0, y=320.04449462890625, width=225.0, height=35.0
        )
        # Botão da Digital
        self.button_image_digital = tk.PhotoImage(
            file=relative_to_assets('button_digital.png')
        )
        self.button_digital = tk.Button(
            self.canvas,
            image=self.button_image_digital,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_entrar_digital(controller),
            relief='flat',
        )
        self.button_digital.place(
            x=316.0, y=385.70574951171875, width=68.0, height=77.0
        )
        # Botão Criar Conta
        self.button_image_criarconta = tk.PhotoImage(
            file=relative_to_assets('button_criarconta.png')
        )
        self.button_criarconta = tk.Button(
            self.canvas,
            image=self.button_image_criarconta,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.show_frame(CadastroScreen),
            relief='flat',
        )
        self.button_criarconta.place(
            x=616.0,
            y=12.34405517578125,
            width=64.0,
            height=46.65594482421875,
        )
    
    def button_entrar_func(self, controller):
        global USER_NAME, USER_ROLE
        self.username = self.entry_login.get()
        self.username = self.username.strip()
        self.password = self.entry_senha.get()
        self.password = self.password.strip()

        db_conn = BancoDados()
        acesso, name, role = db_conn.altenticar_user(self.username, self.password)

        if not acesso:
            messagebox.showerror(title='ERROR', message='Login ou senha incorreta')
        else:
            controller.show_frame(ConsultaScreen)
            USER_NAME = name
            USER_ROLE = role

        db_conn.desconecta_db()

    def button_entrar_digital(self, controller):
        # Pegar imagem do explorador de arquivos
        filepath = filedialog.askopenfilename()
        # Rodar extração de minucias
        self.hash = processamento_fingerprint(filepath)
        # Chamar banco para comparar
        global USER_NAME, USER_ROLE
        db_conn = BancoDados()
        acesso, name, role = db_conn.altenticar_user_fingerprint(self.hash)

        if not acesso:
            messagebox.showerror(title='ERROR', message='Digital não cadastrada')
        else:
            controller.show_frame(ConsultaScreen)
            USER_NAME = name
            USER_ROLE = role
        db_conn.desconecta_db()

class CadastroScreen(tk.Frame):
    """Janela de Cadastro do User"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Canvas Principal
        self.canvas = tk.Canvas(
            self,
            bg='#FFFFFF',
            height=550,
            width=700,
            bd=0,
            highlightthickness=0,
            relief='ridge',
        )
        self.canvas.grid(row=0, column=0, sticky=(tk.E + tk.W + tk.N + tk.S))
        # Imagem fundo
        self.imagem_imagem_fundo = tk.PhotoImage(
            file=relative_to_assets('image_fundo.png')
        )
        self.imagem_fundo = self.canvas.create_image(
            350.0, 275.0, image=self.imagem_imagem_fundo
        )
        # Imagem do GOV
        self.imagem_imagem_gov = tk.PhotoImage(
            file=relative_to_assets('image_gov.png')
        )
        self.image_gov = self.canvas.create_image(
            600.5282287597656, 492.2825622558594, image=self.imagem_imagem_gov
        )
        # Imagem da Logo
        self.imagem_imagem_logo = tk.PhotoImage(
            file=relative_to_assets('image_logo.png')
        )
        self.image_logo = self.canvas.create_image(
            170.0, 47.0, image=self.imagem_imagem_logo
        )
        # Texto principal - Ministerio
        self.canvas.create_text(
            195.0,
            42.0,
            anchor='nw',
            text='MINISTERIO DO MEIO AMBIENTE',
            fill='#1E1E1E',
            font=('Poppins ExtraBold', 20 * -1),
        )
        # Area do formulario
        self.canvas.create_rectangle(
            214.0, 110.0, 487.0, 504.0, fill='#EFEFEF', outline='#DDDDDD'
        )
        # Insert e Icon Login
        self.image_icon_user = tk.PhotoImage(
            file=relative_to_assets('icon_user.png')
        )
        self.icon_user = self.canvas.create_image(
            245.0452880859375, 140.5, image=self.image_icon_user
        )
        self.canvas.create_text(
            255,
            134,
            anchor='nw',
            text='Login',
            fill='#000000',
            font=('Poppins Regular', 13 * -1),
        )
        self.entry_image_login = tk.PhotoImage(
            file=relative_to_assets('entry_small.png')
        )
        self.entry_bg_login = self.canvas.create_image(
            350.5, 175.5, image=self.entry_image_login
        )
        self.entry_login = tk.Entry(
            self.canvas, bd=0, bg='#FFFFFF', fg='#000716', highlightthickness=0
        )
        self.entry_login.place(
            x=244.80000019073486,
            y=161,
            width=211.39999961853027,
            height=30,
        )
        # Insert e Icon de Senha
        self.image_icon_key = tk.PhotoImage(
            file=relative_to_assets('icon_key.png')
        )
        self.icon_key = self.canvas.create_image(
            244.00000762939453, 220.5, image=self.image_icon_key
        )
        self.canvas.create_text(
            255,
            214.0,
            anchor='nw',
            text='Senha',
            fill='#000000',
            font=('Poppins Regular', 13 * -1),
        )
        self.entry_image_senha = tk.PhotoImage(
            file=relative_to_assets('entry_small.png')
        )
        self.entry_bg_senha = self.canvas.create_image(
            349.5782012939453, 258.9906311035156, image=self.entry_image_senha
        )
        self.entry_senha = tk.Entry(
            self.canvas, bd=0, bg='#FFFFFF', fg='#000716', highlightthickness=0
        )
        self.entry_senha.place(
            x=243.87820148468018,
            y=245,
            width=211.39999961853027,
            height=30,
        )
        # Insert e Icon de ACL
        self.image_icon_acl = tk.PhotoImage(
            file=relative_to_assets('icon_acl.png')
        )
        self.icon_acl = self.canvas.create_image(
            244.00000762939453, 300, image=self.image_icon_acl
        )
        self.canvas.create_text(
            257,
            292,
            anchor='nw',
            text='Nível de Acesso',
            fill='#000000',
            font=('Poppins Regular', 13 * -1),
        )
        self.entry_image_acl = tk.PhotoImage(
            file=relative_to_assets('entry_small.png')
        )
        self.entry_bg_acl = self.canvas.create_image(
            349.5782012939453, 330, image=self.entry_image_acl
        )
        self.choices = ['3 - ALTO', '2 - MEDIO', '1 - BAIXO']
        self.combo_style = ttk.Style()
        self.combo_style.theme_use('alt')
        self.combo_style.map(
            'TCombobox', fieldbackground=[('readonly', 'white')]
        )
        self.combo_style.configure(
            'TCombobox',
            background='white',
            font=('Helvetica', 24),
            borderwidth=0,
            relif='flat',
            bordercolor='#FFFFFF',
        )
        self.entry_acl = ttk.Combobox(
            self.canvas,
            values=self.choices,
            style='TCombobox',
            state='readonly',
        )
        self.entry_acl.place(
            x=243.87820148468018,
            y=316,
            width=211.39999961853027,
            height=30,
        )
        # Botão de Cadastrar
        self.button_image_entrar = tk.PhotoImage(
            file=relative_to_assets('button_cadastrar.png')
        )
        self.button_entrar = tk.Button(
            self.canvas,
            image=self.button_image_entrar,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:self.button_cadastro_user_function(),
            relief='flat',
        )
        self.button_entrar.place(x=238.0, y=365, width=225.0, height=35.0)
        # Botão de Cadastro da Digital
        self.button_image_cadastradigital = tk.PhotoImage(
            file=relative_to_assets('button_cadastro_digital.png')
        )
        self.button_cadastradigital = tk.Button(
            self.canvas,
            image=self.button_image_cadastradigital,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:self.pegar_digital(),
            relief='flat',
        )
        self.button_cadastradigital.place(
            x=316.0, y=410, width=72.0, height=75.0
        )
        # Botão voltar
        self.button_image_voltar = tk.PhotoImage(
            file=relative_to_assets('button_voltar.png')
        )
        self.button_voltar = tk.Button(
            self.canvas,
            image=self.button_image_voltar,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:controller.show_frame(LoginScreen),
            relief='flat',
        )
        self.button_voltar.place(
            x=20,
            y=12.34405517578125,
            width=55.0,
            height=44,
        )
    
    def button_cadastro_user_function(self):
        self.username = self.entry_login.get()
        self.username = self.username.strip()
        self.password = self.entry_senha.get()
        self.password = self.password.strip()
        self.role = self.entry_acl.get()
        global USER_HASH
        if USER_HASH == '':
            self.hash = self.pegar_digital()
            self.hash = USER_HASH
        else:
            self.hash = USER_HASH

        if self.role == '3 - ALTO':
            self.role = 3
        elif self.role == '2 - MEDIO':
            self.role = 2
        elif self.role == '1 - BAIXO':
            self.role = 1
        else:
            self.role = ''
        
        if self.username =='' or self.password == '' or self.role == '' or self.hash == '':
            messagebox.showerror(title='ERROR', message='Nenhum dos campos deve estar vazio')
        else:
            db_conn = BancoDados()
            inserido = db_conn.inserir_user(self.username, self.password, self.role, self.hash)

            if inserido:
                messagebox.showerror(title='ERROR', message='Já Existe um User com esse nome')
            else: 
                messagebox.showinfo(title='SUCESSO', message='Usuario Criado')
    
    def pegar_digital(self):
        # Pegar imagem do explorador de arquivos
        filepath = filedialog.askopenfilename()
        # Rodar extração de minucias
        global USER_HASH
        USER_HASH = processamento_fingerprint(filepath)

class ConsultaScreen(tk.Frame):
    """Janela Principal"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Canvas Principal
        self.canvas = tk.Canvas(
            self,
            bg='#FFFFFF',
            height=550,
            width=700,
            bd=0,
            highlightthickness=0,
            relief='ridge',
        )
        self.canvas.grid(row=0, column=0, sticky=(tk.E + tk.W + tk.N + tk.S))
        # Area do header
        self.canvas.create_rectangle(
            0, 0, 700, 50, fill='#AAFF90', outline='#DDDDDD'
        )
        # Botão voltar
        self.button_image_voltar = tk.PhotoImage(
            file=relative_to_assets('button_voltar_header.png')
        )
        self.button_voltar = tk.Button(
            self.canvas,
            image=self.button_image_voltar,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:parent.quit(),
            relief='flat',
        )
        self.button_voltar.place(
            x=10,
            y=1,
            width=30,
            height=44,
        )
        # Botão cadastrar
        self.button_image_cadastrar = tk.PhotoImage(
            file=relative_to_assets('button_cadastro_header.png')
        )
        self.button_cadastrar = tk.Button(
            self.canvas,
            image=self.button_image_cadastrar,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:controller.show_frame(InserirScreen),
            relief='flat',
        )
        self.button_cadastrar.place(
            x=115,
            y=14,
            width=181,
            height=25,
        )
        # Botão deletar
        self.button_image_deletar = tk.PhotoImage(
            file=relative_to_assets('button_deletar_header.png')
        )
        self.button_deletar = tk.Button(
            self.canvas,
            image=self.button_image_deletar,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:controller.show_frame(DeletarScreen),
            relief='flat',
        )
        self.button_deletar.place(
            x=350,
            y=14,
            width=160,
            height=25,
        )
        # Icon User e Nome
        self.label_nome = tk.Label(
            self.canvas,
            bg= '#AAFF90',
            anchor='center',
            text= 'Nome do user',
            font=('Poppins Regular', 13 * -1),
        )
        self.label_nome.place(
            x=525,
            y=36,
            width=170,
            height=12,
        )
        self.image_icon_user = tk.PhotoImage(
            file=relative_to_assets('image_user.png')
        )
        self.icon_user = self.canvas.create_image(
            610, 18, image=self.image_icon_user
        )
        # Area do form
        self.form_image_rectangle = tk.PhotoImage(
            file=relative_to_assets('form_area.png')
        )
        self.form_bg = self.canvas.create_image(
            349.5782012939453, 320, image=self.form_image_rectangle
        )
        # Texto principal - Propriedas rurais
        self.canvas.create_text(
            27,
            70,
            anchor='nw',
            text='PROPRIEDADES RURAIS',
            fill='#1E1E1E',
            font=('Poppins ExtraBold', 20 * -1),
        )
        # Barra de pesquisa e botão
        self.entry_image_pesquisar = tk.PhotoImage(
            file=relative_to_assets('entry_pesquisar.png')
        )
        self.entry_bg_pesquisar = self.canvas.create_image(
            510, 80, image=self.entry_image_pesquisar
        )
        self.entry_pesquisar = tk.Entry(
            self.canvas, bd=0, bg='#E6E6E6', fg='#000716', highlightthickness=0
        )
        self.entry_pesquisar.place(
            x= 405,
            y= 65,
            width=211.39999961853027,
            height=30,
        )
        self.button_image_pesquisar = tk.PhotoImage(
            file=relative_to_assets('button_pesquisar.png')
        )
        self.button_pesquisar = tk.Button(
            self.canvas,
            image=self.button_image_pesquisar,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:self.button_pesquisar_func(),
            relief='flat',
        )
        self.button_pesquisar.place(
            x=630,
            y=60,
            width=40,
            height=40,
        )
        # Lista de dados
        self.table_propriedades = ttk.Treeview(
            self.canvas,
            height= 3,
            columns=('col1','col2','col3'),
            selectmode='browse',
        )
        self.table_propriedades.heading('#0', text='')
        self.table_propriedades.heading('#1', text='ID')
        self.table_propriedades.heading('#2', text='Nome')
        self.table_propriedades.heading('#3', text='Informações')
        self.table_propriedades.column('#0', width=1, stretch=0)
        self.table_propriedades.column('#1', width=20)
        self.table_propriedades.column('#2', width=200)
        self.table_propriedades.column('#3', width=350)
        self.table_propriedades.place(
            x=40,
            y=120,
            width=610,
            height=400,
        )
        self.scroll_table = tk.Scrollbar(self.canvas, orient='vertical', command=self.table_propriedades.yview)
        self.table_propriedades.configure(yscrollcommand=self.scroll_table.set)
        self.scroll_table.place(
            x=650,
            y=120,
            width=20,
            height=400, 
        )
        #Botão atualizar lista
        self.button_image_atualizar = tk.PhotoImage(
            file=relative_to_assets('button_atualizar.png')
        )
        self.button_esqueci = tk.Button(
            self.canvas,
            image=self.button_image_atualizar,
            borderwidth=0,
            highlightthickness=0,
            relief='flat',
            command=lambda: self.mostrar_lista(),
        )
        self.button_esqueci.place(
            x=352,
            y=60,
            width=40,
            height=40,
        )
    
    def mostrar_lista(self):
        self.table_propriedades.delete(*self.table_propriedades.get_children())
        db_conn = BancoDados()
        lista_dados = db_conn.select_lista(USER_ROLE)

        for i in lista_dados:
            self.table_propriedades.insert('','end',values=i)
        
        db_conn.desconecta_db()
    
    def button_pesquisar_func(self):
        global USER_NAME, USER_ROLE
        self.pesquisa = self.entry_pesquisar.get()
        self.table_propriedades.delete(*self.table_propriedades.get_children())
        db_conn = BancoDados()
        lista_dados = db_conn.pesquisar_lista(self.pesquisa, USER_ROLE)

        for i in lista_dados:
            self.table_propriedades.insert('','end',values=i)
        
        db_conn.desconecta_db()      
class InserirScreen(tk.Frame):
    """Janela para Inserir Cadastros de dados"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Canvas Principal
        self.canvas = tk.Canvas(
            self,
            bg='#FFFFFF',
            height=550,
            width=700,
            bd=0,
            highlightthickness=0,
            relief='ridge',
        )
        self.canvas.grid(row=0, column=0, sticky=(tk.E + tk.W + tk.N + tk.S))
        # Area do header
        self.canvas.create_rectangle(
            0, 0, 700, 50, fill='#AAFF90', outline='#DDDDDD'
        )
        # Botão voltar
        self.button_image_voltar = tk.PhotoImage(
            file=relative_to_assets('button_voltar_header.png')
        )
        self.button_voltar = tk.Button(
            self.canvas,
            image=self.button_image_voltar,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:controller.show_frame(ConsultaScreen),
            relief='flat',
        )
        self.button_voltar.place(
            x=10,
            y=1,
            width=30,
            height=44,
        )
                # Area do header
        self.canvas.create_rectangle(
            0, 0, 700, 50, fill='#AAFF90', outline='#DDDDDD'
        )
        # Botão voltar
        self.button_image_voltar = tk.PhotoImage(
            file=relative_to_assets('button_voltar_header.png')
        )
        self.button_voltar = tk.Button(
            self.canvas,
            image=self.button_image_voltar,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:controller.show_frame(ConsultaScreen),
            relief='flat',
        )
        self.button_voltar.place(
            x=10,
            y=1,
            width=30,
            height=44,
        )
        # Botão cadastrar
        self.button_image_cadastrar = tk.PhotoImage(
            file=relative_to_assets('button_cadastro_header.png')
        )
        self.button_cadastrar = tk.Button(
            self.canvas,
            image=self.button_image_cadastrar,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:controller.show_frame(InserirScreen),
            relief='flat',
        )
        self.button_cadastrar.place(
            x=115,
            y=14,
            width=181,
            height=25,
        )
        # Botão deletar
        self.button_image_deletar = tk.PhotoImage(
            file=relative_to_assets('button_deletar_header.png')
        )
        self.button_deletar = tk.Button(
            self.canvas,
            image=self.button_image_deletar,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:controller.show_frame(DeletarScreen),
            relief='flat',
        )
        self.button_deletar.place(
            x=350,
            y=14,
            width=160,
            height=25,
        )
        # Icon User e Nome
        self.label_nome = tk.Label(
            self.canvas,
            bg= '#AAFF90',
            anchor='center',
            text='Nome do user',
            font=('Poppins Regular', 13 * -1),
        )
        self.label_nome.place(
            x=525,
            y=36,
            width=170,
            height=12,
        )
        self.image_icon_user = tk.PhotoImage(
            file=relative_to_assets('image_user.png')
        )
        self.icon_user = self.canvas.create_image(
            610, 18, image=self.image_icon_user
        )
        # Area do form
        self.form_image_rectangle = tk.PhotoImage(
            file=relative_to_assets('form_area.png')
        )
        self.form_bg = self.canvas.create_image(
            349.5782012939453, 320, image=self.form_image_rectangle
        )
        # Texto principal - Propriedas rurais
        self.canvas.create_text(
            27,
            70,
            anchor='nw',
            text='CADASTRAR PROPRIEDADE',
            fill='#1E1E1E',
            font=('Poppins ExtraBold', 20 * -1),
        )
        # Botão limpar
        self.button_image_limpar = tk.PhotoImage(
            file=relative_to_assets('button_limpar.png')
        )
        self.button_limpar = tk.Button(
            self.canvas,
            image=self.button_image_limpar,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:self.button_limpar_func(),
            relief='flat',
        )
        self.button_limpar.place(
            x=560,
            y=120,
            width=100,
            height=30,
        )
        # Campos do form
        self.entry_image_nome = tk.PhotoImage(
            file=relative_to_assets('entry_large.png')
        )
        self.entry_bg_nome = self.canvas.create_image(
            265, 195, image=self.entry_image_nome
        )
        self.entry_nome = tk.Entry(
            self.canvas, bd=0, bg='#FFFFFF', fg='#000716', highlightthickness=0
        )
        self.entry_nome.place(
            x= 65,
            y= 181,
            width=400,
            height=30,
        )
        self.canvas.create_text(
            60,
            150,
            anchor='nw',
            text='Nome da Propriedade',
            fill='#000000',
            font=('Poppins Regular', 13 * -1),
        )
        self.entry_image_nivel = tk.PhotoImage(
            file=relative_to_assets('entry_large.png')
        )
        self.entry_bg_nivel = self.canvas.create_image(
            265, 270, image=self.entry_image_nivel
        )
        self.choices = ['3 - ALTO', '2 - MEDIO', '1 - BAIXO']
        self.combo_style = ttk.Style()
        self.combo_style.theme_use('alt')
        self.combo_style.map(
            'TCombobox', fieldbackground=[('readonly', 'white')]
        )
        self.combo_style.configure(
            'TCombobox',
            background='white',
            font=('Helvetica', 24),
            borderwidth=0,
            relif='flat',
            bordercolor='#FFFFFF',
        )
        self.entry_nivel = ttk.Combobox(
            self.canvas,
            values=self.choices,
            style='TCombobox',
            state='readonly',
        )
        self.entry_nivel.place(
            x= 65,
            y= 256,
            width=400,
            height=30,
        )
        self.canvas.create_text(
            60,
            225,
            anchor='nw',
            text='Nível de acesso',
            fill='#000000',
            font=('Poppins Regular', 13 * -1),
        )
        self.entry_image_info = tk.PhotoImage(
            file=relative_to_assets('entry_text_area.png')
        )
        self.entry_bg_info = self.canvas.create_image(
            360, 380, image=self.entry_image_info
        )
        self.entry_info = tk.Text(
            self.canvas, bd=0, bg='#FFFFFF', fg='#000716', highlightthickness=0
        )
        self.entry_info.place(
            x= 65,
            y= 330,
            width=590,
            height=100,
        )
        self.canvas.create_text(
            60,
            300,
            anchor='nw',
            text='Informações',
            fill='#000000',
            font=('Poppins Regular', 13 * -1),
        )
        # Botão Cadastrar
        self.button_image_cadastrar_registro = tk.PhotoImage(
            file=relative_to_assets('button_cadastrar_registro.png')
        )
        self.button_cadastrar_resgitro = tk.Button(
            self.canvas,
            image=self.button_image_cadastrar_registro,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:self.button_cadastrar_func(),
            relief='flat',
        )
        self.button_cadastrar_resgitro.place(
            x=220,
            y=460,
            width=254,
            height=34,
        )

    def button_limpar_func(self):
        self.entry_nome.delete(0, 'end')
        self.entry_info.delete('1.0','end')
        self.entry_nivel.delete(0, 'end')
    
    def button_cadastrar_func(self):
        self.name = self.entry_nome.get()
        self.name = self.name.strip()
        self.info = self.entry_info.get('1.0','end')
        self.acl = self.entry_nivel.get()
        if self.acl == '3 - ALTO':
            self.acl = 3
        elif self.acl == '2 - MEDIO':
            self.acl = 2
        elif self.acl == '1 - BAIXO':
            self.acl = 1
        else:
            self.acl = ''
        
        if self.name =='' or self.info == '' or self.acl == '':
            messagebox.showerror(title='ERROR', message='Nenhum dos campos deve estar vazio')
        else:
            db_conn = BancoDados()
            db_conn.inserir_propriedade(self.name, self.info, self.acl)

class DeletarScreen(tk.Frame):
    """Janela para Deletar cadastros de dados"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Canvas Principal
        self.canvas = tk.Canvas(
            self,
            bg='#FFFFFF',
            height=550,
            width=700,
            bd=0,
            highlightthickness=0,
            relief='ridge',
        )
        self.canvas.grid(row=0, column=0, sticky=(tk.E + tk.W + tk.N + tk.S))
                # Area do header
        self.canvas.create_rectangle(
            0, 0, 700, 50, fill='#AAFF90', outline='#DDDDDD'
        )
        # Botão voltar
        self.button_image_voltar = tk.PhotoImage(
            file=relative_to_assets('button_voltar_header.png')
        )
        self.button_voltar = tk.Button(
            self.canvas,
            image=self.button_image_voltar,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:controller.show_frame(ConsultaScreen),
            relief='flat',
        )
        self.button_voltar.place(
            x=10,
            y=1,
            width=30,
            height=44,
        )
        # Botão cadastrar
        self.button_image_cadastrar = tk.PhotoImage(
            file=relative_to_assets('button_cadastro_header.png')
        )
        self.button_cadastrar = tk.Button(
            self.canvas,
            image=self.button_image_cadastrar,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:controller.show_frame(InserirScreen),
            relief='flat',
        )
        self.button_cadastrar.place(
            x=115,
            y=14,
            width=181,
            height=25,
        )
        # Botão deletar
        self.button_image_deletar = tk.PhotoImage(
            file=relative_to_assets('button_deletar_header.png')
        )
        self.button_deletar = tk.Button(
            self.canvas,
            image=self.button_image_deletar,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:controller.show_frame(DeletarScreen),
            relief='flat',
        )
        self.button_deletar.place(
            x=350,
            y=14,
            width=160,
            height=25,
        )
        # Icon User e Nome
        self.label_nome = tk.Label(
            self.canvas,
            bg= '#AAFF90',
            anchor='center',
            text='Nome do user',
            font=('Poppins Regular', 13 * -1),
        )
        self.label_nome.place(
            x=525,
            y=36,
            width=170,
            height=12,
        )
        self.image_icon_user = tk.PhotoImage(
            file=relative_to_assets('image_user.png')
        )
        self.icon_user = self.canvas.create_image(
            610, 18, image=self.image_icon_user
        )
        # Area do form
        self.form_image_rectangle = tk.PhotoImage(
            file=relative_to_assets('form_area.png')
        )
        self.form_bg = self.canvas.create_image(
            349.5782012939453, 320, image=self.form_image_rectangle
        )
        # Texto principal - Deletar Registros
        self.canvas.create_text(
            27,
            70,
            anchor='nw',
            text='DELETAR REGISTRO',
            fill='#1E1E1E',
            font=('Poppins ExtraBold', 20 * -1),
        )
        # Botão limpar
        self.button_image_limpar = tk.PhotoImage(
            file=relative_to_assets('button_limpar.png')
        )
        self.button_limpar = tk.Button(
            self.canvas,
            image=self.button_image_limpar,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:self.button_limpar_func(),
            relief='flat',
        )
        self.button_limpar.place(
            x=560,
            y=120,
            width=100,
            height=30,
        )
        # Campos do form
        self.entry_image_nome = tk.PhotoImage(
            file=relative_to_assets('entry_large.png')
        )
        self.entry_bg_nome = self.canvas.create_image(
            265, 195, image=self.entry_image_nome
        )
        self.entry_nome = tk.Entry(
            self.canvas, bd=0, bg='#FFFFFF', fg='#000716', highlightthickness=0
        )
        self.entry_nome.place(
            x= 65,
            y= 181,
            width=400,
            height=30,
        )
        self.canvas.create_text(
            60,
            150,
            anchor='nw',
            text='Nome da Propriedade',
            fill='#000000',
            font=('Poppins Regular', 13 * -1),
        )
        # Botão Registro
        self.button_image_deletar_registro = tk.PhotoImage(
            file=relative_to_assets('button_deletar_registro.png')
        )
        self.button_deletar_resgitro = tk.Button(
            self.canvas,
            image=self.button_image_deletar_registro,
            borderwidth=0,
            highlightthickness=0,
            command= lambda:self.button_deletar_func(),
            relief='flat',
        )
        self.button_deletar_resgitro.place(
            x=220,
            y=260,
            width=254,
            height=34,
        )

    def button_limpar_func(self):
        self.entry_nome.delete(0, 'end')
    
    def button_deletar_func(self):
        self.nome = self.entry_nome.get()

        db_conn = BancoDados()
        db_conn.deletar_propriedade(self.nome)

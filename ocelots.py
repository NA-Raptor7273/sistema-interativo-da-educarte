import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3 as sq
from datetime import datetime

if 'page' not in st.session_state:
    st.session_state.page = 'login'

con = sq.connect('ocelots.db')
cursor = con.cursor()

#------TABELAS------

adm = '''
CREATE TABLE IF NOT EXISTS adm (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    senha TEXT NOT NULL
)
'''

cursor.execute(adm)

con.commit()

#-----TELA SING-UP-----

def sign_up():
    st.title('SING-UP')
    with st.form('adm_cad'):
        usuario = st.text_input('Crie um nome de usuário:')
        senha = st.text_input('Crie uma senha:', type='password')
        senha_conf = st.text_input('Confirme a senha:', type='password')
        submit = st.form_submit_button('SignUp')
        login = st.button('LogIn')
        if submit and usuario and senha and senha_conf and senha == senha_conf:
            verificacao = cursor.execute('SELECT * FROM adm WHERE usuario = ?', (usuario))
            if verificacao:
                st.error(f'Usuário {usuario} já cadastrado! Faça log-in.')
            else:
                cursor.execute('INSERT INTO adm (usuario, senha) VALUES (?, ?)', (usuario, senha))
                st.success(f'Cadastro realizado com sucesso {usuario}! Seja bem-vindo ao SIO: Sistema Interativo Ocelots!')
        elif submit and usuario and senha and senha_conf:
            st.error('As senhas não coincidem!')
        else:
            st.error('Por favor, preencha todos os campos!')
        
        if login:
            st.session_state.page = 'login'

#-----TELA LOG-IN-----

def log_in():
    st.title('LOG-IN')
    with st.form('adm_log'):
        usuario = st.text_input('Usuário:')
        senha = st.text_input('Digite a Senha:', type='password')
        submit = st.form_submit_button('Log-in')
        signup = st.button('Sign-Up')
        if submit and usuario and senha:
            verificacao = cursor.execute('SELECT * FROM adm WHERE usuario = ?', (usuario))
            if verificacao:
                st.session_state.page = 'start'
            else:
                st.error('Usuário ou senha incorreto!')
        else:
            st.error('Por favor, preencha todos os campos!')
        if signup:
            st.session_state.page = 'signup'

#-----TELA INÍCIO-----

def start():
    st.title('SIO: Sistema Interativo Ocelots')
    menu = st.sidebar('Menu', ['Início', 'Gerenciar', 'Painel de Controle', 'Sair'])
    if menu == 'Início':
        st.session_state.page = 'start'
    elif menu == 'Gerenciar':
        submenu = st.sidebar.radio('Gerenciar', ['Gerenciar Pagamentos', 'Gerenciar Frequências'])
        if submenu == 'Gerenciar Pagamentos':
            st.title('SIO: Sistema Interativo Ocelots')
            st.text('Gerenciar Pagamentos')
        elif submenu == 'Gerenciar Frequências':
            st.title('SIO: Sistema Interativo Ocelots')
            st.text('Gerenciar Frequências')
    elif menu == 'Painel de Controle':
        st.title('SIO: Sistema Interativo Ocelots')
    elif menu == 'Sair':
        st.session_state.page = 'login'

#-----MULTIAPP-----

if st.session_state.page == 'start':
    start()
elif st.session_state.page == 'login':
    log_in()
elif st.session_state.page == 'signup':
    sign_up()

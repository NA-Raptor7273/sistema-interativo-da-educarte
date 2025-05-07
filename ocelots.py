import streamlit as st
import sqlite3
import hashlib

# ========================
# Funções auxiliares
# ========================
def conectar_bd():
    return sqlite3.connect("usuarios.db")

def criar_tabela():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_usuario(username, password):
    senha_hash = hash_senha(password)
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, senha_hash))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def criar_usuario(username, password):
    senha_hash = hash_senha(password)
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, senha_hash))
        conn.commit()
        sucesso = True
    except sqlite3.IntegrityError:
        sucesso = False  # Usuário já existe
    conn.close()
    return sucesso

# ========================
# Interface do Streamlit
# ========================
st.set_page_config(page_title="Login App", page_icon="🔐")

# Cria a tabela no banco de dados, se ainda não existir
criar_tabela()

# Estado de navegação
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'login'
if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = None

# ========== TELA DE LOGIN ==========
if st.session_state.pagina == 'login':
    st.title("🔐 Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if verificar_usuario(usuario, senha):
            st.success("Login bem-sucedido!")
            st.session_state.usuario_logado = usuario
            st.session_state.pagina = 'app'
        else:
            st.warning("Usuário ou senha incorretos.")
            if st.button("Ir para Cadastro"):
                st.session_state.pagina = 'cadastro'

# ========== TELA DE CADASTRO ==========
elif st.session_state.pagina == 'cadastro':
    st.title("📝 Cadastro")
    novo_usuario = st.text_input("Novo Usuário")
    nova_senha = st.text_input("Nova Senha", type="password")

    if st.button("Cadastrar"):
        if criar_usuario(novo_usuario, nova_senha):
            st.success("Cadastro realizado com sucesso! Faça login.")
            st.session_state.pagina = 'login'
        else:
            st.error("Usuário já existe. Tente outro nome.")

    if st.button("Voltar para Login"):
        st.session_state.pagina = 'login'

# ========== APLICATIVO PRINCIPAL ==========
elif st.session_state.pagina == 'app':
    st.title("📱 Meu Aplicativo")
    st.success(f"Bem-vindo, {st.session_state.usuario_logado}!")
    st.write("✅ Aqui está o conteúdo principal do seu app...")

    if st.button("Sair"):
        st.session_state.pagina = 'login'
        st.session_state.usuario_logado = None

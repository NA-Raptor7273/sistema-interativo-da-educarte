import streamlit as st
import sqlite3 as sq
from datetime import datetime

# Conexão com o banco
conn = sq.connect('educarte.db')
cursor = conn.cursor()

# Criação da tabela (sem o campo id)
cursor.execute('''
CREATE TABLE IF NOT EXISTS alunos (
    nome TEXT PRIMARY KEY,
    telefone TEXT,
    turma TEXT,
    payday TEXT,
    status_pagamento INTEGER DEFAULT 1,  -- 1 para regular, 0 para inadimplente
    data_pagamento DATE
)
''')
conn.commit()


# Função para atualizar o status dos alunos
def atualizar_status():
    hoje = datetime.now()
    cursor.execute("SELECT nome, payday, status_pagamento, data_pagamento FROM alunos WHERE status_pagamento = 1")
    alunos = cursor.fetchall()

    for aluno in alunos:
        nome, payday, status, data_pagamento = aluno

        # Verifica se a data de pagamento já foi registrada e se é no mesmo mês
        if data_pagamento:
            data_pagamento = datetime.strptime(data_pagamento, '%Y-%m-%d')
            # Se o pagamento foi feito depois do vencimento, manter como regular
            if data_pagamento.month == hoje.month and data_pagamento.day >= int(payday.split()[1]):
                continue

        # Se o pagamento não foi feito ou passou o dia, marcar como inadimplente
        dia_pag = int(payday.split()[1])
        if hoje.day > dia_pag:
            cursor.execute("UPDATE alunos SET status_pagamento = 0 WHERE nome = ?", (nome,))

    conn.commit()


# Chama a função de atualização
atualizar_status()


# Função para registrar pagamento
def registrar_pagamento(nome_aluno):
    hoje = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("UPDATE alunos SET status_pagamento = 1, data_pagamento = ? WHERE nome = ?", (hoje, nome_aluno))
    conn.commit()


# Início do app
st.title('EducArte')
menu = st.sidebar.selectbox('Escolha uma opção:',
                            ['Início', 'Cadastro de Aluno', 'Cadastro de Funcionário', 'Gerenciamento', 'Consultar',
                             'Ajuda'])

# Aba Início
if menu == 'Início':
    st.title('SIE: Sistema Interativo da EducArte')
    st.text(
        'Seja bem-vindo ao SIE! Aqui você tem acesso a todos os alunos e funcionários cadastrados nessa empresa, bem como seus status de pagamento. \n'
        'No canto superior esquerdo você encontrará o menu interativo com as opções: Início; Cadastro de Aluno; Cadastro de Funcionário; Consultar; Ajuda.\n'
        'Início: a aba de início contém todas as informações pertinentes ao uso do aplicativo. Funciona de maneira similar a um guia de uso.\n'
        'Cadastro de Aluno: a aba de cadastro de aluno é responsável por adicionar alunos ao banco de dados da empresa.\n'
        'Cadastro de Funcionário: a aba de cadastro de funcionário é responsável por adicionar funcionários ao banco de dados da empresa.\n'
        'Gerenciamento: a aba de gerenciamento é responsável pelo gerenciamento de pessoas cadastradas, nela você poderá mudar o status, editar dados e deletar pessoas do sistema.\n'
        'Consultar: a aba de consulta é responsável por consultar pessoas cadastradas no sistema, bem como suas informações de cadastro e status.\n'
        'Ajuda: a aba de ajuda contém informações de contato para ajuda técnica caso se faça necessário.')

# Aba Cadastro de Aluno
elif menu == 'Cadastro de Aluno':
    st.title('Cadastro de Aluno')
    with st.form('Cadastro de Aluno'):
        nome = st.text_input('Nome do aluno:')
        telefone = st.text_input('Telefone:')
        turma = st.selectbox('Selecione a Turma', ['BabyClass 1', 'BabyClass 2', 'Infantil 1', 'Infantil 2', 'Adultos'])
        payday = st.radio('Selecione o Dia de Pagamento:', ['Dia 10', 'Dia 20'])
        submit = st.form_submit_button('Cadastrar')

    if submit:
        cursor.execute("INSERT INTO alunos (nome, telefone, turma, payday) VALUES (?, ?, ?, ?)",
                       (nome, telefone, turma, payday))
        conn.commit()
        st.success('Aluno Cadastrado com Sucesso!')

# Aba Cadastro de Funcionário
elif menu == 'Cadastro de Funcionário':
    st.title('Cadastro de Funcionário')
    with st.form('Cadastro de Funcionário'):
        nome = st.text_input('Nome do Funcionário:')
        telefone = st.text_input('Telefone:')
        funcao = st.selectbox('Selecione a Função',
                              ['Sócio', 'Professor', 'Administração', 'Marketing', 'Jurídico', 'Limpeza'])
        salario = st.text_input('Salário (R$):')
        submit = st.form_submit_button('Cadastrar')

    if submit:
        st.success('Funcionário Cadastrado com Sucesso!')

# Aba Gerenciamento
elif menu == 'Gerenciamento':
    st.title('Gerenciamento de Alunos')
    nome = st.text_input('Digite o nome para buscar:')

    if st.button('Buscar'):
        cursor.execute("SELECT nome, status_pagamento, payday FROM alunos WHERE nome LIKE ?", (f"%{nome}%",))
        alunos = cursor.fetchall()
        if alunos:
            for aluno in alunos:
                nome_aluno, status_pagamento, payday = aluno
                status = '✔️ Regular' if status_pagamento == 1 else '❌ Inadimplente'
                st.write(f"Nome: {nome_aluno} | Status: {status} | Dia de Pagamento: {payday}")
                if status_pagamento == 0:
                    if st.button(f"Registrar pagamento para {nome_aluno}"):
                        registrar_pagamento(nome_aluno)
                        st.success(f"Pagamento de {nome_aluno} registrado com sucesso!")
        else:
            st.warning("Aluno não encontrado.")

# Aba Consultar
elif menu == 'Consultar':
    st.title('Consultar Alunos')
    nome = st.text_input('Nome do Aluno:')

    if st.button('Buscar'):
        cursor.execute("SELECT nome, status_pagamento, payday FROM alunos WHERE nome LIKE ?", (f"%{nome}%",))
        alunos = cursor.fetchall()
        if alunos:
            for aluno in alunos:
                nome_aluno, status_pagamento, payday = aluno
                status = '✔️ Regular' if status_pagamento == 1 else '❌ Inadimplente'
                st.write(f"Nome: {nome_aluno} | Status: {status} | Dia de Pagamento: {payday}")
        else:
            st.warning("Aluno não encontrado.")

# Aba Ajuda
elif menu == 'Ajuda':
    st.text('E-mail para contato: bassi.31.01.06@gmail.com')

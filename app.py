import streamlit as st
import sqlite3 as sq

# Conexão e criação da tabela
conn = sq.connect('educarte.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    turma TEXT,
    payday TEXT,
    status_pagamento INTEGER DEFAULT 0
)
''')
conn.commit()

st.title('EducArte')
menu = st.sidebar.selectbox('Escolha uma opção:', ['Início', 'Cadastro de Aluno', 'Cadastro de Funcionário', 'Gerenciamento', 'Consultar', 'Ajuda'])

if menu == 'Início':
    st.title('SIE: Sistema Interativo da EducArte')
    st.text('''
Seja bem-vindo ao SIE! Aqui você tem acesso a todos os alunos e funcionários cadastrados nessa empresa, bem como seus status de pagamento.

Menu:
- Início: guia de uso.
- Cadastro de Aluno: adicionar alunos.
- Cadastro de Funcionário: adicionar funcionários.
- Gerenciamento: editar status ou remover.
- Consultar: ver dados e status.
- Ajuda: contato técnico.
''')

elif menu == 'Cadastro de Aluno':
    st.title('Cadastro de Aluno')
    with st.form('form_aluno'):
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

elif menu == 'Cadastro de Funcionário':
    st.title('Cadastro de Funcionário')
    with st.form('form_funcionario'):
        nome = st.text_input('Nome do Funcionário:')
        telefone = st.text_input('Telefone:')
        funcao = st.selectbox('Selecione a Função', ['Sócio', 'Professor', 'Administração', 'Marketing', 'Jurídico', 'Limpeza'])
        salario = st.text_input('Salário (R$):')
        submit = st.form_submit_button('Cadastrar')

    if submit:
        st.success('Funcionário Cadastrado com Sucesso!')
        st.write(f'**Nome**: {nome}')
        st.write(f'**Telefone**: {telefone}')
        st.write(f'**Função**: {funcao}')
        st.write(f'**Salário**: R${salario}')

elif menu == 'Gerenciamento':
    st.title('Gerenciamento de Alunos')
    nome = st.text_input('Digite o nome para buscar:')

    if st.button('Buscar'):
        cursor.execute("SELECT id, nome, status_pagamento FROM alunos WHERE nome LIKE ?", (f"%{nome}%",))
        resultados = cursor.fetchall()
        if resultados:
            for r in resultados:
                status = '✔️' if r[2] == 1 else '❌'
                st.write(f"ID: {r[0]} | Nome: {r[1]} | Status: {status}")

            id_aluno = st.number_input("ID do aluno para atualizar:", min_value=1, step=1)
            if st.button("Marcar como Regular"):
                cursor.execute("UPDATE alunos SET status_pagamento = 1 WHERE id = ?", (id_aluno,))
                conn.commit()
                st.success("Status atualizado para ✔️")
            if st.button("Marcar como Inadimplente"):
                cursor.execute("UPDATE alunos SET status_pagamento = 0 WHERE id = ?", (id_aluno,))
                conn.commit()
                st.success("Status atualizado para ❌")
            if st.button("Remover Aluno"):
                cursor.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))
                conn.commit()
                st.warning("Aluno removido.")
        else:
            st.warning("Nenhum aluno encontrado.")

elif menu == 'Consultar':
    st.title('Consultar Alunos')
    nome = st.text_input('Nome do Aluno:')
    if st.button('Procurar por Nome'):
        cursor.execute("SELECT nome, telefone, turma, payday, status_pagamento FROM alunos WHERE nome LIKE ?", (f"%{nome}%",))
        resultados = cursor.fetchall()
        if resultados:
            for r in resultados:
                status = "✔️ Regular" if r[4] == 1 else "❌ Inadimplente"
                st.write(f"**Nome:** {r[0]} | **Telefone:** {r[1]} | **Turma:** {r[2]} | **Pagamento:** {r[3]} | **Status:** {status}")
        else:
            st.warning("Aluno não encontrado.")

elif menu == 'Ajuda':
    st.title('Ajuda')
    st.text('E-mail para contato: bassi.31.01.06@gmail.com')

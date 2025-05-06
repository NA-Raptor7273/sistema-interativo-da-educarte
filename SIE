import streamlit as st
import sqlite3 as sq
from datetime import datetime

con = sq.connect('educarte.db')
cursor = con.cursor()

alunos = '''
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    turma TEXT NOT NULL
)'''

funcionarios = '''
CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    funcao TEXT NOT NULL,
    salario NUMERIC(10, 2)
)'''

pagamento = '''
CREATE TABLE IF NOT EXISTS pagamentos (
    id_aluno INTEGER PRIMARY KEY,
    status TEXT DEFAULT 'em dia',
    mes INTEGER,
    FOREIGN KEY (id_aluno) REFERENCES alunos (id)
)'''

controle_pagamentos = '''
CREATE TABLE IF NOT EXISTS controle_pagamento (
    id INTEGER PRIMARY KEY,
    ultima_atualizacao TEXT
)
'''

cursor.execute(alunos)
cursor.execute(funcionarios)
cursor.execute(pagamento)
cursor.execute(controle_pagamentos)

con.commit()

def atualizar_pagamentos():
    hoje = datetime.now()
    cursor.execute("SELECT ultima_atualizacao FROM controle_pagamento WHERE id = 1")
    dado = cursor.fetchone()

    # Se nunca atualizou, ou se foi em outro mês
    if not dado or datetime.strptime(dado[0], '%Y-%m-%d').month != hoje.month:
        cursor.execute("SELECT id_aluno FROM pagamentos")
        todos = cursor.fetchall()
        for aluno_id in todos:
            cursor.execute("UPDATE pagamentos SET status = 'devendo', mes = ? WHERE id_aluno = ?", (hoje.month, aluno_id[0]))

        # Atualiza ou insere a nova data de verificação
        if dado:
            cursor.execute("UPDATE controle_pagamento SET ultima_atualizacao = ? WHERE id = 1", (hoje.strftime('%Y-%m-%d'),))
        else:
            cursor.execute("INSERT INTO controle_pagamento (id, ultima_atualizacao) VALUES (1, ?)", (hoje.strftime('%Y-%m-%d'),))

        con.commit()

atualizar_pagamentos()

turmas = ['Baby Class 1 A', 'Baby Class 1 B', 'Baby Class Sexta', 'Baby Class 2 A', 'Baby Class 2 B', 'Pré A', 'Pré B', '1e 2° ano', '3e 4° ano',
          'Jazz Infantil', 'Jazz Juvenil', 'Teatro Musical', 'Musicalização Infantil']

funcoes = ['Sócio', 'Professor', 'Administração', 'Limpeza']

menu = st.sidebar.selectbox('MENU', ['Início', 'Cadastrar', 'Gerenciar', 'Consultar', 'Excluir', 'Ajuda'])


if menu == 'Início':
    st.title('SIE: Sistema Interativo EducArte')
    st.markdown('Bem-vindo ao Sistema Interativo EducArte!\n\n'
            '**Início:** Tela Inicial\n\n'
            '**Cadastrar:** Cadastro de Alunos/Funcionários\n\n'
            '**Gerenciar:** Gerenciar Informações de Pessoas Cadastradas\n\n'
            '**Consultar:** Consultar Pessoas Cadastradas'
            )
elif menu == 'Cadastrar':
    submenu = st.sidebar.radio('Cadastrar:', ['Alunos', 'Funcionários'])
    if submenu == 'Alunos':
        st.title('SIE: Sistema Interativo EducArte')
        st.subheader('Cadastro de Alunos')
        with st.form('cadastro_aluno'):
            nome = st.text_input('Nome:')
            telefone = st.text_input('Telefone:')
            turma = st.selectbox('Selecione a Turma', turmas)
            submit = st.form_submit_button('Cadastrar')
            if submit and nome and telefone and turma:
                cursor.execute("INSERT INTO alunos (nome, telefone, turma) VALUES (?, ?, ?)", (nome, telefone, turma))
                con.commit()
                id_aluno = cursor.lastrowid
                cursor.execute("INSERT INTO pagamentos (id_aluno, status, mes) VALUES (?, 'em dia', ?)", (id_aluno, datetime.now().month))
                con.commit()
                st.success(f'Cadastro Realizado com Sucesso!')
            else:
                st.error('Preencha todos os campos!')
    elif submenu == 'Funcionários':
        st.title('SIE: Sistema Interativo EducArte')
        st.subheader('Cadastro de Funcionários')
        with st.form('cadastro_funcionario'):
            nome = st.text_input('Nome:')
            telefone = st.text_input('Telefone:')
            funcao = st.selectbox('Selecione a Função', funcoes)
            salario = st.number_input('Salário (R$):')
            submit = st.form_submit_button('Cadastrar')
            if submit and nome and telefone and funcao and salario:
                cursor.execute("INSERT INTO funcionarios (nome, telefone, funcao, salario) VALUES (?, ?, ?, ?)", (nome, telefone, funcao, salario))
                con.commit()
                st.success('Cadastro Realizado com Sucesso!')
            else:
                st.error('Preencha todos os campos!')
elif menu == 'Gerenciar':
                submenu = st.sidebar.radio('Gerenciar:', ['Alunos', 'Funcionários'])
                if submenu == 'Alunos':
                    st.subheader('Gerenciar Alunos')
                    if 'resultado_aluno' not in st.session_state:
                        st.session_state.resultado_aluno = None

                    busca = st.text_input('Nome:')
                    btn_buscar = st.button('Buscar')

                    if btn_buscar and busca:
                        cursor.execute('SELECT * FROM alunos WHERE nome = (?)', (busca,))
                        st.session_state.resultado_aluno = cursor.fetchone()

                    resultado = st.session_state.resultado_aluno

                    if resultado:
                        st.success(
                            f'Aluno encontrado!\n\nNome: {resultado[1]}\n\nTelefone: {resultado[2]}\n\nTurma: {resultado[3]}')
                        cursor.execute("SELECT status FROM pagamentos WHERE id_aluno = ?", (resultado[0],))
                        status_atual = cursor.fetchone()[0]

                        with st.form("form_editar_aluno"):
                            nome = st.text_input('Editar Nome', value=resultado[1])
                            telefone = st.text_input('Editar Telefone', value=resultado[2])
                            turma = st.selectbox('Editar Turma', turmas, index=turmas.index(resultado[3]))
                            novo_status = st.radio('Alterar Status de Pagamento:', ['em dia', 'devendo'],
                                                   index=0 if status_atual == 'em dia' else 1)
                            submit = st.form_submit_button('Salvar Alterações')
                            if submit:
                                cursor.execute(
                                    'UPDATE alunos SET nome = ?, telefone = ?, turma = ? WHERE id = ?',
                                    (nome, telefone, turma, resultado[0])
                                )
                                cursor.execute('UPDATE pagamentos SET status = ? WHERE id_aluno = ?',
                                               (novo_status, resultado[0]))
                                con.commit()
                                st.success(
                                    f'Alterações feitas com sucesso!\n\nNome: {nome}\n\nTelefone: {telefone}\n\nTurma: {turma}\n\nStatus de pagamento atualizado para: {novo_status}')

                    else:
                        st.error('Aluno não encontrado!')

                elif submenu == 'Funcionários':
                    st.subheader('Gerenciar Funcionários')
                    if 'resultado_funcionario' not in st.session_state:
                        st.session_state.resultado_funcionario = None


                    busca = st.text_input('Nome:')
                    btn_buscar = st.button('Buscar')
                    if btn_buscar and busca:
                        cursor.execute('SELECT * FROM funcionarios WHERE nome = (?)', (busca,))
                        st.session_state.resultado_funcionario = cursor.fetchone()
                        con.commit()

                    resultado = st.session_state.resultado_funcionario

                    if resultado:
                            st.success(
                                f'Funcionário encontrado!\n\nNome: {resultado[1]}\n\nTelefone: {resultado[2]}\n\nFunção: {resultado[3]}\n\nSalário: R${resultado[4]}')
                            with st.form("form_editar_funcionarios"):
                                nome = st.text_input('Editar Nome', value=resultado[1])
                                telefone = st.text_input('Editar Telefone', value=resultado[2])
                                funcao = st.selectbox('Editar Função', funcoes, index=funcoes.index(resultado[3]))
                                salario = st.number_input('Editar Salário', value=resultado[4])
                                submit = st.form_submit_button('Salvar Alterações')
                                if submit:
                                    cursor.execute(
                                        'UPDATE funcionarios SET nome = ?, telefone = ?, funcao = ?, salario = ? WHERE id = ?',
                                        (nome, telefone, funcao, salario, resultado[0])
                                    )
                                    con.commit()
                                    st.success(
                                        f'Alterações feitas com sucesso!\nNome: {nome}\nTelefone: {telefone}\nFunção: {funcao}\nSalário: R${salario}')


                    else:
                            st.error('Funcionário não encontrado!')

elif menu == 'Consultar':
    submenu = st.sidebar.radio('Consultar:', ['Alunos', 'Funcionários'])
    if submenu == 'Alunos':
        st.title('SIE: Sistema Interativo EducArte')
        st.subheader('Consultar Alunos')
        busca = st.text_input('Nome:')
        btn_buscar = st.button('Buscar')
        if btn_buscar and busca:
            cursor.execute('SELECT * FROM alunos WHERE nome = (?)', (busca,))
            con.commit()
            resultado = cursor.fetchone()

            if resultado:
                st.success(
                    f'Aluno encontrado!\nID: {resultado[0]}\nNome: {resultado[1]}\nTelefone: {resultado[2]}\nTurma: {resultado[3]}')
                cursor.execute("SELECT status FROM pagamentos WHERE id_aluno = ?", (resultado[0],))
                status = cursor.fetchone()
                st.info(f'Status de Pagamento: {status[0]}')
            else:
                st.error('Aluno não encontrado!')
    elif submenu == 'Funcionários':
        st.title('SIE: Sistema Interativo EducArte')
        st.subheader('Consultar Funcionários')
        busca = st.text_input('Nome:')
        btn_buscar = st.button('Buscar')
        if btn_buscar and busca:
            cursor.execute('SELECT * FROM funcionarios WHERE nome = (?)', (busca,))
            con.commit()
            resultado = cursor.fetchone()

            if resultado:
                st.success(
                    f'Funcionário encontrado!\n\nNome: {resultado[1]}\n\nTelefone: {resultado[2]}\n\nFunção: {resultado[3]}\n\nSalário: R${resultado[4]}')
            else:
                st.error('Funcionário não encontrado!')
elif menu == 'Ajuda':
    st.title('SIE: Sistema Interativo EducArte')
    st.text('bassi.31.01.06@gmail.com')
elif menu == 'Excluir':
    submenu = st.sidebar.radio('Excluir:', ['Alunos', 'Funcionários'])
    if submenu == 'Funcionários':
        st.title('SIE: Sistema Interativo EducArte')
        st.text('Digite o Nome da Pessoa a ser Excluída do SIE')
        nome = st.text_input('NOME:')
        cursor.execute('SELECT * FROM funcionarios WHERE nome = ?', (nome,))
        con.commit()
        resultado = cursor.fetchone()
        excluir = st.button('Excluir')
        if resultado:
            if excluir:
                cursor.execute('DELETE FROM funcionarios WHERE nome = ?', (nome,))
                con.commit()
                st.warning(f'Funcionário {nome} excluído com sucesso!')
        else:
            st.error('Funcionário Não Encontrado!')
    if submenu == 'Alunos':
        st.title('SIE: Sistema Interativo EducArte')
        st.text('Digite o Nome do Aluno a ser Excluído do SIE')
        nome = st.text_input('NOME:')
        cursor.execute('SELECT * FROM alunos WHERE nome = ?', (nome,))
        con.commit()
        resultado = cursor.fetchone()
        excluir = st.button('Excluir')
        if resultado:
            if excluir:
                cursor.execute('DELETE FROM alunos WHERE nome = ?', (nome,))
                cursor.execute('DELETE FROM pagamentos WHERE id_aluno = ?', (resultado[0],))
                con.commit()
                st.warning(f'Aluno {nome} excluído com sucesso!')
        else:
            st.error('Aluno Não Encontrado!')

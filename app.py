import streamlit as st
import sqlite3 as sq
import random

st.title('EducArte')
menu = st.sidebar.selectbox('Escolha uma opção:', ['Início', 'Cadastro de Aluno', 'Cadastro de Funcionário', 'Gerenciamento', 'Consultar', 'Ajuda'])

if menu == 'Início':
    st.title('SIE: Sistema Interativo da EducArte')
    st.text('Seja bem-vindo ao SIE! Aqui você tem acesso a todos os alunos e funcionários cadastrados nessa empresa, bem como seus status de pagamento. \n'
            'No canto superior esquerdo você encontrará o menu interativo com as opções: Início; Cadastro de Aluno; Cadastro de Funcionário; Consultar; Ajuda.\n'
            'Início: a aba de início contém todas as informações pertinentes ao uso do aplicativo. Funciona de maneira similar a um guia de uso.\n'
            'Cadastro de Aluno: a aba de cadastro de aluno é responsável por adicionar alunos ao banco de dados da empresa.\n'
            'Cadastro de Funcionário: a aba de cadastro de funcionário é responsável por adicionar funcionários ao banco de dados da empresa.\n'
            'Gerenciamento: a aba de gerenciamento é responsável pelo gerenciamento de pessoas cadastradas, nela você poderá mudar o status, editar dados e deletar pessoas do sitema.\n'
            'Consultar: a aba de consulta é resposável por consultar pessoas cadastradas no sistema, bem como suas informações de cadastro e status.\n'
            'Ajuda: a aba de ajuda contém informações de contato para ajuda técnica caso se faça necessário.')
elif menu == 'Cadastro de Aluno':
    st.title('SIE: Sistema Interativo da EducArte')
    with st.form('Cadastro de Aluno'):
        nome = st.text_input('Nome do aluno:')
        telefone = st.text_input('Telefone:')
        turma = st.selectbox('Selecione a Turma', ['BabyClass 1', 'BabyClass 2', 'Infantil 1', 'Infantil 2', 'Adultos'])
        payday = st.radio('Selecione o Dia de Pagamento:', ['Dia 10', 'Dia 20'])
        submit = st.form_submit_button('Cadastrar')
    if submit:
        st.success('Aluno Cadastrado com Sucesso!')
        st.write(f'**Nome**: {nome}')
        st.write(f'**Telefone**: {telefone}')
        st.write(f'**Turma**: {turma}')
        st.write(f'**Dia de Pagamento**: {payday}')
elif menu == 'Cadastro de Funcionário':
    st.title('SIE: Sistema Interativo da EducArte')
    with st.form('Cadastro de Funcionário'):
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
    st.title('SIE: Sistema Interativo da EducArte')
    st.text('Gerencie as Informações de Pessoas Cadastradas no Sistema')
    nome = st.text_input('Nome do Aluno:')
    if st.button('Procurar por Nome'):
        st.write(f'{nome} está cadastrado!')
elif menu == 'Consultar':
    st.title('SIE: Sistema Interativo da EducArte')
    st.text('Consulte as Informações de Pessoas Cadastradas no Sistema')
    nome = st.text_input('Nome do Aluno:')
    if st.button('Procurar por Nome'):
        st.write(f'{nome} está cadastrado!')
elif menu == 'Ajuda':
    st.text('E-mail para contato: bassi.31.01.06@gmail.com')

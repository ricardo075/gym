import streamlit as st
import sqlite3
import datetime

# Criando a conexão com o banco de dados
conn = sqlite3.connect('gym_database.db')
c = conn.cursor()

# Criando a tabela no banco de dados se ela não existir
c.execute('''CREATE TABLE IF NOT EXISTS gym_members
             (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, categoria TEXT, idade INTEGER, mes_inscricao INTEGER, dia_inscricao INTEGER, ano_inscricao INTEGER)''')

# Configurações gerais do aplicativo
st.set_page_config(page_title="Gym Membership App", page_icon=":muscle:", layout="wide")

# Adicionando imagem de fundo
st.markdown(
    """
    <style>
    .reportview-container {
        background: url('https://static-storage.dnoticias.pt/www-assets.dnoticias.pt/images/configuration/LG/Gin%C3%A1
        sio.jpg');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Inserir nova pessoa no ginásio
st.title("Inscrever Nova Pessoa no Ginásio")
nome = st.text_input("Nome")
idade = st.number_input("Idade", min_value=1, max_value=150)

categoria = st.selectbox("Categoria", ("Karate", "Ginásio", "Aeróbica"))

mes = st.number_input("Mês de Inscrição", min_value=1, max_value=12)
dia = st.number_input("Dia de Inscrição", min_value=1, max_value=31)
ano = st.number_input("Ano de Inscrição", min_value=1900, max_value=2100)

if st.button("Registrar"):
    c.execute("INSERT INTO gym_members (nome, categoria, idade, mes_inscricao, dia_inscricao, ano_inscricao) VALUES (?, ?, ?, ?, ?, ?)",
              (nome, categoria, idade, mes, dia, ano))
    conn.commit()
    st.success("Pessoa cadastrada com sucesso!")

# Ver pessoas inscritas no ginásio
st.title("Ver Pessoas Inscritas no Ginásio")
opcao = st.selectbox("Escolha a opção", ("Todas as inscrições", "Karate", "Ginásio", "Aeróbica"))

if opcao == "Todas as inscrições":
    data = c.execute("SELECT nome, mes_inscricao, dia_inscricao, ano_inscricao FROM gym_members").fetchall()
else:
    data = c.execute("SELECT nome, mes_inscricao, dia_inscricao, ano_inscricao FROM gym_members WHERE categoria=?", (opcao,)).fetchall()

if len(data) == 0:
    st.warning("Nenhuma pessoa encontrada com essa categoria.")
else:
    for pessoa in data:
        inscricao = datetime.date(pessoa[3], pessoa[1], pessoa[2])
        diferenca = datetime.date.today() - inscricao
        if diferenca.days > 1:
            st.warning(f"{pessoa[0]} - Inscrição expirada ({inscricao})")
        else:
            st.write(f"{pessoa[0]} se inscreveu em {pessoa[2]}/{pessoa[1]}/{pessoa[3]}")

# Apagar nome de pessoas inscritas
st.title("Apagar Nome de Pessoa Inscrita")
nome_apagar = st.text_input("Nome da pessoa a ser apagada")

if st.button("Apagar"):
    c.execute("DELETE FROM gym_members WHERE nome=?", (nome_apagar,))
    conn.commit()
    st.success("Nome apagado com sucesso!")


import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objs as go
import plotly.express as px
import colorlover as cl


# Personalização da página

st.set_page_config(
    page_title="Título da Página",
    page_icon=":memo:",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown('<h1 style="color: blue; align:center">Dashboard para Análise e Visualização</h1>', unsafe_allow_html=True)


# Leitura dos dados iniciais
df_position = pd.read_csv('fake_position.csv')
df_policies = pd.read_excel('fake_allocation_policies.xlsx', names=['class_name', 'conservador', 'moderado-conservador', 'moderado', 'moderado-agressivo', 'agressivo'])


def get_metrica(row):
    politica = row['account_suitability']
    if politica == 'conservador':
        return row['conservador']

    elif politica == 'moderado conservador':
        return row['moderado_conservador']

    elif politica == 'moderado':
        return row['moderado']

    elif politica == 'moderado agressivo':
        return row['moderado_agressivo']

    elif politica == 'agressivo':
        return row['agressivo']
    else:
        return None

# Merge das duas tabelas 
merged = pd.merge(df_position, df_policies, on='class_name')
# Aplicar a função na tabela agrupada
merged['metrica'] = merged.apply(get_metrica, axis=1)



# Encontrar o valor das classes de ativos
asset_class = merged.groupby(['account_code', 'asset_name', 'account_suitability','class_name', 'metrica']).agg({'position_value': 'sum'}).reset_index()
asset_class = asset_class.groupby(['asset_name', 'class_name']).agg({'position_value': 'sum'}).reset_index()
df_maior_asset_class = asset_class.groupby(['asset_name']).agg({'position_value': 'sum'}).reset_index().sort_values('position_value', ascending=False)
df_maior_asset_class_value = df_maior_asset_class.iloc[0]['position_value']
df_maior_asset_class_name = df_maior_asset_class.iloc[0]['asset_name']



# -----------
df_class_maior_aderencia = df_position.groupby(['class_name']).agg({'position_value': 'sum'}).reset_index().sort_values('position_value', ascending=False)
df_class_maior_valor = df_class_maior_aderencia.iloc[0]['position_value']
df_class_maior_valor_classe = df_class_maior_aderencia.iloc[0]['class_name']


df_peso_carteira = df_position.groupby(['asset_name', 'account_suitability']).agg({'position_value': 'sum'}).reset_index().sort_values('position_value', ascending=False)
df_peso_carteira = df_peso_carteira.iloc[:6]

asset_class = merged.groupby(['account_code', 'asset_name', 'account_suitability','class_name', 'metrica']).agg({'position_value': 'sum'}).reset_index()
asset_class.head(7)

# Leitura dos dados finais
df = pd.read_csv('database.csv')

menor_aderencia = df.groupby(['account_code']).agg({'aderencia': 'mean'}).reset_index().sort_values('aderencia', ascending=False)
menor_aderencia_valor = menor_aderencia.iloc[1]['aderencia']
menor_aderencia_account = menor_aderencia.iloc[1]['account_code']


# filtros
st.sidebar.image('imagem_perfil.png', width=100)
# Adicionando o título e nome
st.sidebar.title('Página do Analista')
st.sidebar.write('User: John Doe')


# informações gerais
with st.container():
    col1, col2, col3 = st.columns(3)
    
with col1:
    st.write(f"Conta com Menor Aderência: {menor_aderencia_account}")
    st.write(f"{round(menor_aderencia_valor, 2)} %")
    

    
with col2:
    st.write(f"Classe com maior aderência: {df_class_maior_valor_classe}")
    st.write(f"R$ {round(df_class_maior_valor, 2)}")
   

    
with col3:
    st.write(f"Carteira com maior Aderência: {df_maior_asset_class_name}")
    st.write(f"{round(df_maior_asset_class_value, 2)}")
    

   
#=======================
# Gráfico de 
fig1 = px.bar(df, x='class_name', y='aderencia', color='class_name',
             labels={'class_name': 'Classe', 'aderencia': 'Valor Total Aderência'},
             title='Classes X Aderência')
fig1.show()


#=======================
# Gráfico de Barras
df_account = df.groupby(['account_suitability']).agg({'account_code': 'count'}).reset_index().sort_values(by='account_code', ascending=False)
fig2 = px.bar(df_account, x='account_suitability', y='account_code', title='Número de contas por account_suitability', color='account_suitability')



#=======================
# Gráfico de Radar
classes_ativos = df['class_name']
alocacao_atual = df['valor_porcentagem_atual']
alocacao_politica = df['metrica'] * 100
fig3 = go.Figure()

fig3.add_trace(go.Scatterpolar(
        r=alocacao_atual,
        theta=classes_ativos,
        fill='toself',
        name='Alocação atual'
))

fig3.add_trace(go.Scatterpolar(
        r=alocacao_politica,
        theta=classes_ativos,
        fill='toself',
        name='Alocação política'
))
fig3.update_layout(
        polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0,80]
        )),
        showlegend=True,
        paper_bgcolor=cl.scales['9']['seq']['Blues'][1],
        plot_bgcolor=cl.scales['9']['seq']['Blues'][1],
        font=dict(
        family='Arial, sans-serif',
        size=14,
        color='black',
        
    ),
        title='Alocação Atual x Alocação Política',
)

#=======================
# Gráfico barras Top 5 ativos com maiores valores
fig4 = px.bar(df_peso_carteira, x='asset_name', y='position_value', color='asset_name',
             labels={'asset_name': 'Ativo', 'total_value': 'Valor Total Investido'},
             title='Top 5 ativos com maiores valores')
fig4.show()


# Gráfico de Pizza
fig5 = go.Figure()
df_account = df.groupby(['account_suitability']).agg({'aderencia': 'mean'}).reset_index().sort_values(by='aderencia', ascending=False)
df_account.head()

# Adicionando as fatias do gráfico de pizza
fig5.add_trace(go.Pie(
    labels=df_account['account_suitability'], 
    values=df_account['aderencia'],
    marker_colors=['steelblue', 'lightblue', 'cornflowerblue', 'skyblue', 'deepskyblue'],
    textinfo='label+percent',  # adicionando o nome da account_suitability e a aderência nas fatias
    hole=0.3,  # definindo o tamanho do "buraco" no meio do gráfico
))

# Configurando o layout
color_scale = cl.scales['5']['seq']['Blues']
fig5.update_layout(
    title='Aderência das contas por account_suitability',legend=dict(
        orientation="v",
        yanchor="middle",
        y=1.02,
        xanchor="left",
        x=1,
        font=dict(size=14)
    )
)

# Mostrando o gráfico
fig5.show()




# Exibição dos gráficos
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
    with col3:
        st.plotly_chart(fig3, use_container_width=True, )
        

col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(fig4, use_containter_width=True)
    with col3:
        st.plotly_chart(fig5, use_containter_width=True)
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go

engine = create_engine('sqlite:///banco.db', echo = True)

# Título da aplicação
st.write('Preços Placas de Video no site Kabum')

# Leitura do arquivo CSV
df = pd.read_sql('SELECT * FROM dados', con = engine)


# Boxplot - Preço à vista
fig_box = px.box(df, x='Valor', title='Boxplot - Valores à Vista')
st.plotly_chart(fig_box)

fig_box2 = px.box(df, x='valor parcelado', title='Boxplot - Valores Parcelados')
st.plotly_chart(fig_box2)

# Histograma - Comparação entre duas colunas
fig_hist = go.Figure()

# Adicionar o histograma da coluna 'Valor'
fig_hist.add_trace(go.Histogram(
    x=df['Valor'],
    name='Valor',
    opacity=0.5,
    marker_color='blue',
    nbinsx=20
))

# Adicionar o histograma da coluna 'valor parcelado'
fig_hist.add_trace(go.Histogram(
    x=df['valor parcelado'],
    name='Valor Parcelado',
    opacity=0.5,
    marker_color='orange',
    nbinsx=20
))

# Ajustar layout
fig_hist.update_layout(
    title='Histograma dos valores parcelados e a vista',
    barmode='overlay',  # Sobrepor os histogramas
    xaxis_title='Valores',
    yaxis_title='Frequência',
    legend_title='Legenda'
)

st.plotly_chart(fig_hist)


#st.plotly_chart(fig_hist)
labels=["R$ 0-1000","R$ 1001-2000","R$ 2001-3000","R$ 3001-4000","R$ 4001-5000"]
bins=[0,1000, 2000, 3000, 4000, 5000]
df['Intervalo'] = pd.cut(df['Valor'], bins=bins,
                          labels=labels, 
                          right=True,
                          )
faixas = pd.DataFrame(df['Intervalo'].value_counts())

# Contando os valores por faixa de preço parcelado

# Criando o gráfico de pizza
fig_pizza = px.pie(
    faixas,
    names=faixas.index,  # Nome das fatias
    values=faixas[faixas.columns[0]],     # Tamanho das fatias
    title='Distribuição por Faixa de Valor à vista',  # Título do gráfico
    color_discrete_sequence=px.colors.sequential.RdBu  # Opcional: paleta de cores
)

# Exibindo o gráfico de pizza no Streamlit
st.plotly_chart(fig_pizza)

# Gráfico de dispersão com relação entre Preço à Vista e Valor Parcelado
fig_scatter = px.scatter(
    df,
    x='Valor',
    y='valor parcelado',
    color='Intervalo',  # Diferencia por faixa de preço parcelado
    size='valor parcelado',   # Tamanho dos pontos baseado no valor parcelado
    hover_data=['Valor', 'valor parcelado'],  # Informações ao passar o mouse
    labels={
        'Preco_a_vista': 'Preço à Vista',
        'Valor_parcelado': 'Valor Parcelado',
        'Faixa_parcelado': 'Faixa de Preço'
    },
    title='Relação entre Preço à Vista, Valor Parcelado e Faixa de Preço'
)

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig_scatter)

# Histograma Multivariado: Preço à Vista por Faixa de Preço Parcelado
fig_hist_mult = px.histogram(
    df,
    x='Valor',
    color='Intervalo',  # Categorização por faixa de preço parcelado
    nbins=20,
    labels={
        'Valor': 'Preço à Vista',
        'Faixa_parcelado': 'Faixa de Preço Parcelado'
    },
    title='Distribuição de Preço à Vista por Faixa de Preço Parcelado',
    barmode='overlay',  # Sobreposição das barras para comparar distribuições
    opacity=0.7         # Ajusta a transparência para facilitar a visualização
)
st.plotly_chart(fig_hist_mult)

# Gráfico de Barras: Média de Preço à Vista por Faixa de Preço Parcelado
media_preco = df.groupby('Intervalo')['Valor'].mean().reset_index()
fig_bar_mult = px.bar(
    media_preco,
    x='Intervalo',
    y='Valor',
    labels={
        'Intervalo': 'Faixa de Preço Parcelado',
        'Valor': 'Média de Preço à Vista'
    },
    title='Média de Preço à Vista por Faixa de Preço Parcelado',
    color='Intervalo',  # Opcional: pode usar uma paleta de cores
    text='Valor'  # Exibe os valores no topo das barras
)
fig_bar_mult.update_traces(texttemplate='%{text:.2f}', textposition='outside')

st.plotly_chart(fig_bar_mult)




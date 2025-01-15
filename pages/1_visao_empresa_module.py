# Bibliotecas
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# bibliotecas necessárias
import pandas as pd
import streamlit as st
from PIL import Image
from datetime import datetime
import folium
from streamlit_folium import folium_static

st.set_page_config (page_title='Visão Empresa', page_icon="📊", layout='wide')

#-----------------------------------------------------------
# Funções:
#-----------------------------------------------------------
def clean_code(df1):
    """ Esta funcao tem a responsabilidade de limpar o dataframe
        
        Tipos de limpeza:
        1. Remoção dos NaN
        2. Mudança do tipo da coluna de dados 
        3. Remoção dos espaços das variáveis de texto
        4. Formatação da coluna de data
        5. Limpreza da coluna de tempo (remoção do texto da variável numérica
        
        Input: Dataframe
        Output: Dataframe
    """
    # 0. Removendo as NaNs de todas as observações que possuem NaN em alguma variável
    # Substitui os "NaN " (string) por valores NaN do pandas
    df1 = df1.replace("NaN ", pd.NA)
    # Agora, remove as linhas que possuem pelo menos um NaN
    df1 = df1.dropna()
    
    # 1. Converter a coluna Delivery_person_Age para inteiro
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    
    # 2. Convertendo a coluna Order_Date de texto para data
    df1['Order_Date']=pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    
    # 3. Convertendo a coluna Delivery_person_Ratings de string para float
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    
    # 4. Convertendo multiple_deliveries de texto para inteiro
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    
    # 5. Removendo os espaços em branco dentro das strings
    # o strip remove os espaços em branco
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    
    # 6. Limpando a coluna de time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    return df1
    
    

def order_metric (df1):
    cols = ['ID', 'Order_Date']
    #linhas selecionadas agrupadas por Order_Date
    df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()
    # desenhar o gráfico de linhas
    fig =  px.bar(df_aux, x='Order_Date', y='ID')
    return fig

def traffic_order_share(df1):
    df_aux = (df1.loc[:,['ID', 'Road_traffic_density']]
                 .groupby('Road_traffic_density')
                 .count()
                 .reset_index())
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
    fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')
    return fig

def traffic_order_city(df1):
    df_aux = (df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
                 .groupby(['City', 'Road_traffic_density'])
                 .count()
                 .reset_index())
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
    return fig

def order_by_week(df1):
        # criar a coluna de semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U') 
    # o U% significa que o primeiro dia da semana vai começar com domingo
    df_aux = (df1.loc[:, ['ID', 'week_of_year']]
                 .groupby('week_of_year')
                 .count()
                 .reset_index())
    fig = px.line(df_aux, x='week_of_year', y='ID')
    return fig

def order_share_by_week(df1):
    # Quantidade de pedidos por semana / Quantidade de entregadores únicos por semana
    a = (df1.loc[:, ['ID', 'week_of_year']]
            .groupby('week_of_year')
            .count()
            .reset_index())
    b = (df1.loc[:, ['Delivery_person_ID', 'week_of_year']]
            .groupby('week_of_year')
            .nunique()
                    .reset_index())
    df_aux = pd.merge(a, b, how='inner')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
            
    fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')
    return fig

def country_maps (df1):
    cols = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
    df_aux = (df1.loc[:, cols]
                 .groupby(['City', 'Road_traffic_density'])
                 .median()
                 .reset_index())
    
    map = folium.Map()
    
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],
                       location_info['Delivery_location_longitude']],
                       popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
    folium_static (map, width=1024, height=600)
# =========================================================================================================
# ---------------------------------------- Inicio da estrutura lógica do código ---------------------------
# =========================================================================================================

# Import dataset
df = pd.read_csv('train.csv')

# Limpando os dados
df1 = clean_code (df)


# =================================================================================================
# Barra Lateral
# =================================================================================================

st.header ('Marketplace - Visão Cliente')
#image_path = 'eu.jpeg'
image = Image.open('eu.jpeg')
st.sidebar.image(image, width = 120)
st.sidebar.markdown('# Curry Company')
st.sidebar.markdown("""____""")
st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor',
    value = datetime(2022, 4, 13).date(),
    min_value = datetime(2022, 2, 11).date(),
    max_value = datetime(2022, 4, 6).date(),
    format='DD-MM-YYYY'
)

#st.dataframe(df1)
#st.header(date_slider)
st.sidebar.markdown("""____""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default = ['Low', 'Medium', 'High', 'Jam'])
#st.header(traffic_options)
st.sidebar.markdown("""____""")
st.sidebar.markdown('### Powered by Aline Barreto')


# Filtro de data
# Drill down dos dados ou zoom
date_slider = pd.to_datetime(date_slider) # Converter date_slider para datetime64 antes da comparação
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe(df1)

# Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe(df1)

# =================================================================================================
# Layout streamlit
# =================================================================================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        # 1. Quantidade de pedidos por dia e colocar num gráfico em barras
        # colunas selecionadas
        st.markdown('# Orders by day')
        st.markdown("<h1 style='text-align: center;'>Pedidos por dia</h1>", unsafe_allow_html=True)
        fig = order_metric (df1)
        st.plotly_chart(fig, use_container_width=True)
               
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('## Pedidos por tráfego')
            fig = traffic_order_share(df1)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.markdown('## Volume de pedidos por cidade e tipo de tráfego')
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width=True)
    
    
with tab2:
    with st.container():
        st.markdown('# Order by week')
        fig = order_by_week(df1)        
        st.plotly_chart (fig, use_container_width = True)
        
    with st.container():
        st.markdown('# Order share by week')
        fig = order_share_by_week(df1)        
        st.plotly_chart (fig, use_container_width = True)

with tab3:    
    st.markdown('# Country Maps')
    country_maps (df1)
    
      


    





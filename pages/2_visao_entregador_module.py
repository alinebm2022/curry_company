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

st.set_page_config (page_title='Visão Restaurante', page_icon="🚴🏼‍♂️", layout='wide')

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

def top_delivers(df1, top_asc):
    df2 = (df1.loc[:, ['Time_taken(min)', 'City', 'Delivery_person_ID']]
            .groupby(['City', 'Delivery_person_ID'])
            .mean()
            .sort_values(['City','Time_taken(min)'], ascending = top_asc)
            .reset_index())

    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
    
    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
    return df3
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

st.header ('Marketplace - Visão Entregadores')
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

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '-', '-'])

with tab1:
    with st.container():
        st.title('Overall Metric')
        col1, col2, col3, col4 = st.columns (4, gap='large')
        with col1:
            #st.markdown('### Entregador mais velho')
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric ('Maior idade', maior_idade)
        with col2:
            #st.markdown('### Entregador mais novo')
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric ('Menor idade', menor_idade)
        with col3:
            #st.markdown('### Melhor condição de veículos')
            best_vehi = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric ('Melhor condição veículo', best_vehi)
        with col4:
            #st.markdown('### Pior condição de veículos')
            worst_vehi = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric ('Pior condição veículo', worst_vehi)
    
    with st.container():
        st.markdown ("""___""")
        st.title('Avaliações')
        col1, col2 = st.columns (2, gap='large')
        with col1:
            st.markdown('##### Avaliação média por entregador')
            df_aux = (df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                      .groupby('Delivery_person_ID')
                      .mean()
                      .reset_index())
            st.dataframe (df_aux)
            
        with col2:
            st.markdown('##### Avaliação média por trânsito')
            df_aux = (df1.loc[:, ['Road_traffic_density', 'Delivery_person_Ratings']]
                      .groupby('Road_traffic_density')
                      .agg({'Delivery_person_Ratings':['mean', 'std']}))
            # mudança de nome das colunas
            df_aux.columns = ['delivery_mean', 'delivery_std']
            # reset de index
            df_aux = df_aux.reset_index()
            # exibir o dataframe
            st.dataframe (df_aux)

            st.markdown('##### Avaliação média por condições climáticas')
            df_aux = (df1.loc[:, ['Weatherconditions', 'Delivery_person_Ratings']]
                      .groupby('Weatherconditions')
                      .agg({'Delivery_person_Ratings':['mean', 'std']}))
            # mudança de nome das colunas
            df_aux.columns = ['delivery_mean', 'delivery_std']
            df_aux = df_aux.reset_index()
            # exibir o dataframe
            st.dataframe (df_aux)

    with st.container():
        st.markdown ("""___""")
        st.title('Velocidade de entrega')
        col1, col2 = st.columns (2, gap='large')
        with col1:
            st.markdown('### Top entregadores mais rápidos')
            df3 = top_delivers(df1, top_asc = True)     
            st.dataframe (df3)
        with col2:
            st.markdown('### Top entregadores mais lentos')
            df3 = top_delivers(df1, top_asc = False)                     
            st.dataframe (df3)
           



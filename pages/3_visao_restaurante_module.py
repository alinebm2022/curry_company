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
from haversine import haversine
import numpy as np

st.set_page_config (page_title='Visão Restaurante', page_icon="👨🏻‍🍳", layout='wide')

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

def distance (df1, fig):
    if fig == False:
        cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
        df1['distance'] = (df1.loc[:, cols].apply (lambda x:
                                                        haversine ((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                        (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1))
        # Calcular a distancia media
        avg_distance = np.round (df1['distance'].mean(), 2)
        return avg_distance
    else:
        cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
        df1['distance'] = (df1.loc[:, cols].apply (lambda x:
                                                    haversine ((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                    (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1))
        # Calcular a distancia media
        avg_distance = df1.loc [:, ['City', 'distance']].groupby('City').mean().reset_index()
        fig = go.Figure(data = [go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0.1,0.1,0.1])])
        
        return fig
    

def avg_std_time_delivery(df1, festival, op):
    """
    Esta função calcula o tempo médio e o desvio padrão do temp de entrega.
    Parâmetros:
    Input:
        - df: dataframe dos dados
        - op: Tipo de operação que precisa ser calculada: 
              'avg_time': Calcula o tempo médio
              'std_time': Calcula o desvio padrão do tempo
    Output:
        - df: Dataframe com 2 colunas e 1 linha
    """
    df_aux = (df1.loc[:, ['Time_taken(min)', 'Festival']]
                 .groupby('Festival')
                 .agg({'Time_taken(min)': ['mean', 'std']}))
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    linhas_selecionadas = df_aux['Festival'] == festival
    df_aux = np.round (df_aux.loc[linhas_selecionadas, op], 2)
    return df_aux


def avg_std_time_graph (df1):
    df_aux = df1.loc[:, ['Time_taken(min)', 'City']].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()   
    fig = go.Figure()
    fig.add_trace (go.Bar(name = 'Control',
                          x=df_aux['City'],
                          y=df_aux['avg_time'],
                          error_y=dict(type='data', array=df_aux['std_time'])))
    fig.update_layout(barmode='group')
    return fig

def avg_std_time_on_traffic(df1):
    df_aux = (df1.loc[:, ['Time_taken(min)', 'City', 'Road_traffic_density']]
                 .groupby(['City','Road_traffic_density'])
                 .agg({'Time_taken(min)': ['mean', 'std']}))
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time',                                color='std_time', color_continuous_scale='RdBu', color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig

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

st.header ('Marketplace - Visão Restaurante')
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
        #st.markdown ("""___""")
        st.markdown('## Overall Metric')
        col1, col2, col3, col4, col5, col6 = st.columns (6)
        
        with col1:
            df_aux = len (df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric ('Entregadores', df_aux) # Entregadores únicos
            
        with col2:
            avg_distance = distance (df1, fig=False)
            col2.metric ('Distância média', avg_distance)
            
        with col3:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'avg_time')
            col3.metric('Tempo c/ Festival', df_aux) # Tempo médio de entrega com festival
                        
        with col4:
            df_aux = avg_std_time_delivery(df1,'Yes', 'std_time')
            col4.metric('STD c/ Festival', df_aux) # Desvio padrão das entregas com festival
                                 
        with col5:
           df_aux = avg_std_time_delivery(df1, 'No', 'avg_time')
           col5.metric('Tempo s/ festival', df_aux) # Tempo médio de entrega sem festival
            
        with col6:
            df_aux = avg_std_time_delivery(df1,'No', 'std_time')
            col6.metric('STD s/ festival', df_aux)  # Desvio padrão das entregas sem festival 
    
    with st.container():
        st.markdown ("""___""")
        st.markdown ("## Tempo médio de entrega por cidade")
        fig = distance (df1, fig=True)
        st.plotly_chart(fig)

    with st.container():
        st.markdown ("""___""")
        st.markdown ("## Distribuição do tempo")
        col1, col2 = st.columns (2)
        with col1:
            fig = avg_std_time_graph (df1)
            st.plotly_chart(fig)
            
        with col2:
            fig = avg_std_time_on_traffic(df1)
            st.plotly_chart(fig)
    
    with st.container():
        st.markdown ("""___""")
        st.markdown ("## Distribuição da distância")
        df_aux = (df1.loc[:, ['Time_taken(min)', 'City', 'Type_of_order']]
                     .groupby(['City', 'Type_of_order'])
                     .agg({'Time_taken(min)': ['mean', 'std']}))

        df_aux.columns = ['avg_time', 'std_tima']
        df_aux = df_aux.reset_index()

        st.dataframe (df_aux)
        
    









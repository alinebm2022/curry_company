import streamlit as st
from PIL import Image

st.set_page_config (
    page_title="Home",
    page_icon="🎲",
)

#image_path = 'eu.jpeg'
image = Image.open('eu.jpeg')
st.sidebar.image(image, width = 120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""____""")


st.write('# Curry Company Growth Dashboard')

st.markdown(
    """
    Growth Dashboard foi contruído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes
    ### Como utilizar o Growth Dashboard?
    - Visão Empresa:
        - Visão gerencial: Métricas gerais de comportamento
        - Visão tática: Indicadores semanais de crescimento
        - Visão geográfica: Insights de geolocalização
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes
    ### Ask for Help
    - Time de Data science no Discord
        - @alinebarreto
    """ )
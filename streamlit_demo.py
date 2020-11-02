import streamlit
import torch
import torch as th
import syft as sy
from syft.grid.clients.data_centric_fl_client import DataCentricFLClient
import pandas as pd
import streamlit as st
import webbrowser




hook = sy.TorchHook(torch)
# The local worker
me = hook.local_worker
me.is_client_worker = False
# The remote workers
bob = DataCentricFLClient(hook, "http://18.220.216.78:5001/")
#alice = DataCentricFLClient(hook, "ws://localhost:5006/")
# The crypto provider
sam = DataCentricFLClient(hook, "http://18.220.216.78:5001/")
kim = DataCentricFLClient(hook, "http://18.220.216.78:5001/")

grid = sy.PrivateGridNetwork(bob,sam, kim)

query = streamlit.text_input('Data Search Query')
data = grid.search(query)

nd = [[id,val[0].description, (list(val[0].shape)), val[0].tags] for id,val in data.items()]

df = pd.DataFrame(nd,columns=['Location','Description','Size','Tags'])
streamlit.table(df)


values = df['Location'].tolist()


def genreate_url(id):

    if id in me._known_workers.keys():
            return me._known_workers[id].url


#a = st.sidebar.selectbox('Choose a Location', values, format_func=genreate_url)


location_id = st.text_input('Location Id')

if location_id not in me._known_workers.keys() and location_id:
  st.warning('Please input a correct Location Id')
  st.stop()


def access_req():
    return genreate_url(location_id)


if st.button('Request access'):
    streamlit.text(" Use This URL to connect to the Data ownner client.")
    url = access_req()
    streamlit.text(url)




url = "http://18.191.60.72/hub/login"
if st.button('Open Playground'):
    webbrowser.open_new_tab(url)

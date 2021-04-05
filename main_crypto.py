"""
@author: Nic93

INFO: Please provide your own API-Key
      Non-commercial use only

Li: GNU
"""

import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from dataloading import fetch_data, load_data

b_fetch = False
b_load = False

st.title(""" Your cryptocurrencies """)

fetch_range = st.slider('Fetching numbers',1,4400,(1,200))
key = st.text_input('Please provide your key here')

st.write(""" List of your currencies currently watched: """)
b_data = st.checkbox('Show/Hide big data')

if st.button('Refresh'):
    df = fetch_data(fetch_range,key)
    #df.reset_index(drop=True,inplace=True)
    #st.dataframe(df.head())
    b_fetch = True

if st.button('Load'):
    df, timestamp = load_data()
    #df.reset_index(drop=True,inplace=True)
    #st.dataframe(df.head())
    b_load = True

if b_fetch or b_load:
    
    disp_df = df.drop(['id','slug','date_added','tags',
             'platform','cmc_rank','last_updated','quote'],axis=1)
    sliced_indcs = ['HBAR','HYVE','BTC','ETH']
    subset_df = disp_df[disp_df['symbol'].isin(sliced_indcs)]
    st.write('Your subset')
    st.dataframe(subset_df)
    st.write('Bulk data (if checkbox set)')
    if b_data:
        st.dataframe(disp_df)
        
    


now_time = datetime.now()
date_time = now_time.strftime('%m_%d_%H_%M')
disp_time = now_time.strftime('%H:%M - %b %d')
if b_fetch:
    st.write(""" Last fetched: """ + disp_time)
if b_load:
    st.write(""" Data from: """ + timestamp)

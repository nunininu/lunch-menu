import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.write("""
# My first app
Hello **world!**

![img](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMDmITYUL3-dQiE99pPRG-f1gLO76Wh_UjEXTSvx0RiNdbvu_d4-L5OR43qlce8eNfeHld83WgawlwjNkQvWM7cA)
""")

df = pd.read_csv('note/menu.csv')

start_idx = df.columns.get_loc('2025-01-07')
melted_df = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2], 
                     var_name='dt', value_name='menu')

not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]
gdf = not_na_df.groupby('ename')['menu'].count().reset_index()
#gdf.plot(x="ename", y="menu", kind="bar")

# 📊 Matplotlib로 바 차트 그리기
fig, ax = plt.subplots()
gdf.plot(x="ename", y="menu", kind="bar", ax=ax)
st.pyplot(fig)

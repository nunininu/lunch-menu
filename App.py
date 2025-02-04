import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psycopg

DB_CONFIG = {
    "dbname": "sunsindb",
    "user": "sunsin",
    "password": "mysecretpassword",
    "host": "localhost",
    "port": "5432"
}

def get_connection():
    return psycopg.connect(**DB_CONFIG)


st.title("점심메뉴 집계")
st.subheader("입력")
menu_name = st.text_input("메뉴 이름", placeholder = "예: 김치찌개")
member_name = st.text_input("먹은 사람", value="nuni")
dt = st.date_input("먹은 날짜")

isPress = st.button("메뉴 저장")

st.success(f"버튼{isPress}")


if isPress:
    if menu_name and member_name and dt:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO lunch_menu(menu_name, member_name, dt) VALUES (%s, %s, %s);",
            (menu_name, member_name, dt)
        )
        conn.commit()
        cursor.close()
        st.success(f"버튼{isPress}: {menu_name},{member_name},{dt}")
    else:
        st.warning(f"모든 값을 입력해주세요!")


# st.write("""
# 점심메뉴 집계
#  **lunch menu**

# ![img](https://static.wikia.nocookie.net/pokemon/images/a/aa/%EA%BC%AC%EB%B6%80%EA%B8%B0_%EA%B3%B5%EC%8B%9D_%EC%9D%BC%EB%9F%AC%EC%8A%A4%ED%8A%B8.png/revision/latest?cb=20170404233452&path-prefix=ko) 
# """)

df = pd.read_csv('note/lunch_menu.csv')

start_idx = df.columns.get_loc('2025-01-07')
melted_df = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2], 
                     var_name='dt', value_name='menu')

not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]
gdf = not_na_df.groupby('ename')['menu'].count().reset_index()

gdf # gdf 만 써도 알아서 표 출력해줌

# 📊 Matplotlib로 바 차트 그리기
fig, ax = plt.subplots()
gdf.plot(x="ename", y="menu", kind="bar", ax=ax)
st.pyplot(fig)

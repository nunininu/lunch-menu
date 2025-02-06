import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psycopg
import os
from dotenv import load_dotenv

members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}

# https://docs.streamlit.io/develop/concepts/connections/secrets-management
load_dotenv()
db_name = os.getenv("DB_NAME")
DB_CONFIG = {
    "user": os.getenv("DB_USERNAME"),
    "dbname": db_name,
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT") 
}

def get_connection():
    return psycopg.connect(**DB_CONFIG)

def insert_menu(menu_name, member_id, dt):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO lunch_menu (menu_name, member_id, dt) VALUES (%s, %s, %s);",
            (menu_name, member_id, dt)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Exception:{e}")
        return False 


st.title(f"점심메뉴집계 {db_name}")

st.subheader("입력")
menu_name = st.text_input("메뉴 이름", placeholder="예: 김치찌개")
member_name = st.selectbox(
    "먹은 사람",
    options=list(members.keys()),
    index=list(members.keys()).index('nuni')
)
member_id = members[member_name]

checkdt = st.date_input("조회할 날짜")
checkPress = st.button ("입력 안 한 사람은?")

query = """
select 
    m.name,
    count(l.id) as lcount
from
    member m
left join lunch_menu 1
on
    l.member_id = m.id and l.dt = %s
group by
        m.id, m.name
having 
        count(l.id) = 0
order by 
        count(l.id) desc
"""
if checkPress:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(queryy,(cdt,))
        rowss = cursor.fetchall()
         
        fdf=pd.DataFrame(rows,columns=['name','count'])
        team_member=fdf['name'].tolist()
        if len(team_member) >=1:
            #st.text(",  ".join(teamember))
            cursor.close()
            conn.close()
            st.success(",  ".join(team_member))
        else:
            cursor.close()
            conn.close()
            st.warning("모든 요원 입력 완료!")
    except Exception as e:
        st.warning(f"조회 중 오류가 발생했습니다")
        print(f"Exception: {e}")

st.subheader("Result check")
#query = "select menu_name as menu,member_id as ename,dt from lunch_menu order by dt desc"
query="""SELECT 
    lunch_menu.menu_name AS menu, 
    member.name AS ename, 
    lunch_menu.dt 
FROM member
INNER JOIN lunch_menu ON member.id = lunch_menu.member_id
ORDER BY lunch_menu.dt DESC"""

conn = get_connection()
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()
cursor.close()
conn.close()


# isPress = st.button("메뉴 저장")

# if isPress:
#     if menu_name and member_id and dt:
#         if insert_menu(menu_name, member_id, dt):
#             st.success(f"입력성공")
#         else:
#             st.error(f"입력실패")
#     else:
#         st.warning(f"모든 값을 입력해주세요!")


st.subheader("확인")
query = """
SELECT
	l.menu_name,
	m.name,
	l.dt
FROM member
INNER JOIN lunch_menu l on l.member_id = m.id
ORDER BY l.dt desc 
"""

conn = get_connection()
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()
cursor.close()
conn.close()

#selected_df = pd.DataFrame([[1,2,3],[4,5,6]], columns=['a','b','c'])
select_df = pd.DataFrame(rows, columns=['menu','ename','dt'])
select_df

st.subheader("통계")

#gdf = not_na_df.groupby('ename')['menu'].count().reset_index()
gdf = select_df.groupby('ename')['menu'].count().reset_index()
#gdf.plot(x="ename", y="menu", kind="bar")

gdf

# 📊 Matplotlib로 바 차트 그리기
# https://docs.streamlit.io/develop/api-reference/charts/st.pyplot
try:
    fig, ax = plt.subplots()
    gdf.plot(x="ename", y="menu", kind="bar", ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.warning(f"차트를 그리기에 충분한 데이터가 없습니다")
    print(f"Exception:{e}")

# TODO
# CSV 로드해서 한번에 다 디비에 INSERT 하는거
st.subheader("벌크 인서트")
if st.button("한방에 인서트"):
    df = pd.read_csv('note/menu.csv')
    start_idx = df.columns.get_loc('2025-01-07')
    melted_df = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2], 
                     var_name='dt', value_name='menu')
   
    not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]

    total_count = len(not_na_df)
    success_count = 0
    fail_count = 0
    fail_messages = []


    for _, row in not_na_df.iterrows():
        m_id = members[row['ename']] ## 50line에서 가져옴
        insert_menu(row['menu'], m_id, row['dt'])

        else:
            fail_count += 1
            fail_messages.append(f"{row['ename']}의 {row['dt']} 메뉴 {row['menu']} 입력 실패")

    if fail_count == 0:
        st.success(f"총 {total_count}건 벌크인서트 성공")
    else:
        st.error(f"총 {total_count}건 중 {fail_count}건 실패")
        for message in fail_messages:
            st.error(message)


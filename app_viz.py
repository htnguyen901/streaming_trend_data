import streamlit as st
import psycopg2
import pandas as pd

st.write("[Spotify Streaming Activity Dashboard](http://localhost:8088/superset/dashboard/spotify-trend/)")

st.write("[Airflow DAG](http://localhost:8080/home)")

@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        colnames = [desc[0] for desc in cur.description]
        return colnames, cur.fetchall()


names, rows = run_query("SELECT * from public.recommended;")
count = run_query("SELECT count(*) from public.recommended;")

st.write(f"You have {count[1][0][0]} recommended tracks")

# Print results.
# for row in rows:
#     st.write(f"{row[0]} has a :{row[1]}:")

df = pd.DataFrame(rows, columns=names)

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = 'Open in Spotify'
    return f'<a target="_blank" href="{link}">{text}</a>'

df = df[['name','artist_name', 'album_name', 'uri']]
df['uri'] = df['uri'].apply(make_clickable)
df.rename(columns={'name': 'Track', 'artist_name': 'Artist', 'album_name': 'Album', 'uri': ''}, inplace=True)
df = df.to_html(escape=False)
st.write(df, unsafe_allow_html=True)


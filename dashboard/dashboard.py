import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# Load dataset
file_path = 'https://raw.githubusercontent.com/username/repository/main/dashboard/all_data.csv'
df = pd.read_csv(file_path)

# Pastikan format tanggal benar
df['dteday'] = pd.to_datetime(df['dteday'])
df['year_month'] = df['dteday'].dt.to_period('M').astype(str)
df['day_of_week'] = df['dteday'].dt.day_name()

# Menambahkan kolom jam transaksi jika ada dalam dataset
if 'hr' in df.columns:
    df['hour'] = df['hr']
else:
    df['hour'] = np.nan

# Mengelompokkan data berdasarkan waktu
df_time = df.groupby('year_month', as_index=False).agg({'instant': 'count'})
df_time.columns = ['year_month', 'transaction_count']

# Mengelompokkan data berdasarkan hari dalam seminggu
df_weekday = df.groupby('day_of_week', as_index=False)['instant'].count()
df_weekday.columns = ['day_of_week', 'transaction_count']

# Mengelompokkan data berdasarkan musim jika tersedia
df_season = df.groupby('season', as_index=False)['instant'].count()
df_season.columns = ['season', 'transaction_count']

# Menyesuaikan label musim
season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df_season['season'] = df_season['season'].map(season_labels)

# Heatmap hubungan waktu transaksi dengan jumlah transaksi jika kolom hour tersedia
if 'hour' in df.columns:
    pivot_time = df.pivot_table(index='day_of_week', columns='hour', values='instant', aggfunc='count', fill_value=0)
    pivot_time = pivot_time.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
else:
    pivot_time = None

# Streamlit UI
st.title("Dashboard Analisis Data Penjualan")

st.header("Kapan transaksi paling banyak terjadi?")
time_chart = px.line(df_time, x='year_month', y='transaction_count', title='Tren Jumlah Transaksi per Bulan')
st.plotly_chart(time_chart)
st.write("Grafik ini menunjukkan tren jumlah transaksi yang terjadi setiap bulan. Dengan melihat tren ini, kita bisa memahami pola musiman atau perubahan signifikan dalam transaksi.")

st.header("Hari apa transaksi paling tinggi?")
weekday_chart = px.bar(df_weekday, x='day_of_week', y='transaction_count', title='Jumlah Transaksi berdasarkan Hari dalam Seminggu')
st.plotly_chart(weekday_chart)
st.write("Grafik ini menggambarkan jumlah transaksi berdasarkan hari dalam seminggu. Informasi ini dapat digunakan untuk mengidentifikasi hari dengan aktivitas transaksi tertinggi.")

st.header("Bagaimana pengaruh musim terhadap jumlah transaksi?")
season_chart = px.bar(df_season, x='season', y='transaction_count', title='Jumlah Transaksi Berdasarkan Musim', 
                      labels={'season': 'Musim', 'transaction_count': 'Jumlah Transaksi'})
st.plotly_chart(season_chart)
st.write("Grafik ini menunjukkan jumlah transaksi pada berbagai musim (Spring, Summer, Fall, Winter). Data ini berguna untuk melihat apakah ada perbedaan pola transaksi yang dipengaruhi oleh perubahan musim.")

if pivot_time is not None:
    st.header("Jam berapa transaksi paling tinggi?")
    heatmap_chart = px.imshow(pivot_time.values,
                              labels={'x': 'Hour', 'y': 'Day of Week', 'color': 'Transaction Count'},
                              x=pivot_time.columns,
                              y=pivot_time.index,
                              title='Heatmap Jumlah Transaksi Berdasarkan Hari dan Jam')
    st.plotly_chart(heatmap_chart)
    st.write("Heatmap ini menunjukkan jumlah transaksi yang terjadi pada berbagai jam dalam sehari dan hari dalam seminggu. Informasi ini dapat membantu dalam memahami waktu-waktu dengan transaksi paling ramai.")

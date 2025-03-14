import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency

# Load dataset
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(r"D:\Laskar Ai\Submission Visualisasi Data\VisualisasiData\dashboard\all_data.csv")

        # Pastikan kolom 'dteday' ada
        if 'dteday' in df.columns:
            df['dteday'] = pd.to_datetime(df['dteday'])
        else:
            st.error("Kolom 'dteday' tidak ditemukan dalam dataset.")
            st.stop()
        
        return df
    except FileNotFoundError:
        st.error("File 'all_data.csv' tidak ditemukan. Periksa direktori file.")
        st.stop()

df = load_data()

# Sidebar untuk filter tanggal
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Mulai Tanggal", df['dteday'].min().date())
end_date = st.sidebar.date_input("Sampai Tanggal", df['dteday'].max().date())

# Filter data berdasarkan tanggal
df_filtered = df[(df['dteday'].dt.date >= start_date) & (df['dteday'].dt.date <= end_date)]

# Menampilkan total pesanan dan pendapatan
total_orders = df_filtered['instant'].nunique()
total_revenue = df_filtered['cnt'].sum()

st.title("📊 Dashboard Analisis Penyewaan Sepeda")

col1, col2 = st.columns(2)
col1.metric("Total Transaksi", total_orders)
col2.metric("Total Pengguna", f"{total_revenue:,}")

# Grafik jumlah transaksi per hari
st.subheader("📅 Jumlah Penyewaan Harian")
daily_orders = df_filtered.groupby(df_filtered['dteday'].dt.date)['instant'].nunique()
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(daily_orders.index, daily_orders.values, marker='o', linestyle='-', color='blue')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Transaksi")
ax.set_title("Jumlah Penyewaan Sepeda Harian")
plt.xticks(rotation=45)
st.pyplot(fig)

# Grafik kondisi cuaca dan penyewaan
st.subheader("🌦️ Pengaruh Cuaca terhadap Penyewaan")
weather_counts = df_filtered.groupby('weathersit')['cnt'].sum()
weather_labels = {1: "Cerah", 2: "Mendung", 3: "Hujan Ringan", 4: "Hujan Lebat"}
weather_counts.index = weather_counts.index.map(weather_labels)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=weather_counts.index, y=weather_counts.values, ax=ax, palette="coolwarm")
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Penyewaan Sepeda Berdasarkan Cuaca")
st.pyplot(fig)

# Grafik distribusi jam penggunaan
st.subheader("⏰ Distribusi Penyewaan Berdasarkan Jam")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df_filtered['hr'], bins=24, kde=True, ax=ax, color="green")
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Distribusi Penyewaan Sepeda per Jam")
st.pyplot(fig)

# Grafik penyewaan berdasarkan musim
st.subheader("🍂 Penyewaan Berdasarkan Musim")
season_counts = df_filtered.groupby('season')['cnt'].sum()
season_labels = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
season_counts.index = season_counts.index.map(season_labels)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=season_counts.index, y=season_counts.values, ax=ax, palette="viridis")
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)

st.sidebar.text("© 2024 Dashboard by Deosa")

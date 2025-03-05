import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Fungsi untuk mendapatkan total penyewaan berdasarkan jam
def get_total_count_by_hour_df(hour_df):
    return hour_df.groupby(by="hr").agg({"cnt": "sum"}).reset_index()

# Membaca dataset
days_df = pd.read_csv("day.csv")
hours_df = pd.read_csv("hour.csv")

# Konversi kolom tanggal
days_df["dteday"] = pd.to_datetime(days_df["dteday"])
hours_df["dteday"] = pd.to_datetime(hours_df["dteday"])

# Rentang tanggal untuk filter
min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])

# Filter data berdasarkan rentang tanggal
main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & 
                       (days_df["dteday"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) & 
                        (hours_df["dteday"] <= str(end_date))]

# Analisis
hour_count_df = get_total_count_by_hour_df(main_df_hour)

# HEADER DASHBOARD
st.header('Bike Sharing Dashboard')

# METRIC TOTAL PENYEWAAN
st.subheader('Statistik Penyewaan Sepeda')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = main_df_days["cnt"].sum()
    st.metric("Total Penyewaan", value=total_orders)

with col2:
    avg_temp = main_df_days["temp"].mean()
    st.metric("Rata-rata Suhu", value=f"{avg_temp:.2f}°C")

with col3:
    avg_humidity = main_df_days["hum"].mean() * 100
    st.metric("Rata-rata Kelembaban", value=f"{avg_humidity:.1f}%")


# VISUALISASI PENYEWAAN BERDASARKAN JAM
st.subheader("Jam dengan Penyewaan Tertinggi & Terendah")

fig, ax = plt.subplots(1, 2, figsize=(16, 6))

# Jam dengan penyewaan terbanyak
top_hours = hour_count_df.sort_values(by="cnt", ascending=False).head(5)
sns.barplot(x="hr", y="cnt", data=top_hours, ax=ax[0], palette=["#90CAF9"])
ax[0].set_title("Jam dengan Penyewaan Tertinggi")
ax[0].set_xlabel("Jam")
ax[0].set_ylabel("Total Penyewaan")

# Jam dengan penyewaan terendah
low_hours = hour_count_df.sort_values(by="cnt", ascending=True).head(5)
sns.barplot(x="hr", y="cnt", data=low_hours, ax=ax[1], palette=["#D3D3D3"])
ax[1].set_title("Jam dengan Penyewaan Terendah")
ax[1].set_xlabel("Jam")
ax[1].set_ylabel("Total Penyewaan")

st.pyplot(fig)

# VISUALISASI MUSIM
st.subheader("Musim dengan Penyewaan Terbanyak")

colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
season_df = main_df_days.groupby("season").cnt.sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="season", y="cnt", data=season_df, palette=colors, ax=ax)
ax.set_title("Penyewaan Berdasarkan Musim", fontsize=14)
ax.set_xlabel("Musim")
ax.set_ylabel("Total Penyewaan")

st.pyplot(fig)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Ubah kolom 'dteday' menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

try:
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
except FileNotFoundError:
    st.write("File tidak ditemukan. Harap periksa kembali.")

# Ubah kolom 'dteday' menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    min_date, max_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Ubah min_date dan max_date menjadi format yang sama dengan 'dteday'
min_date = pd.to_datetime(min_date)
max_date = pd.to_datetime(max_date)

# Ambil data hari yang sama dari kedua dataframe
same_day_data = pd.merge(day_df, hour_df, on='dteday', how='inner')

# Buat filter berdasarkan min_date dan max_date untuk day_df
mask_day = (day_df['dteday'] >= min_date) & (day_df['dteday'] <= max_date)
filtered_day = day_df.loc[mask_day]

# Buat filter berdasarkan min_date dan max_date untuk same_day_data
mask_hour = (hour_df['dteday'] >= min_date) & (hour_df['dteday'] <= max_date)
filtered_hour = hour_df.loc[mask_hour]

#Header 
st.header('Bike Sharing Dashboard:sparkles:')


#Grafik Penggunaan Sepeda dari hari ke hari
st.subheader('Grafik Penggunaan Sepeda dari Hari ke Hari')
total_penggunaan = filtered_day['cnt'].sum()  # Menggunakan filtered_day 
st.metric('Total Penggunaan', value=total_penggunaan)

# Ambil hanya 80 data pertama
data_to_plot = filtered_day.iloc[:80] 

# Grafik
plt.figure(figsize=(10, 6))
plt.plot(data_to_plot['dteday'], data_to_plot['cnt'], marker='o', color='b', linewidth=2, markersize=8)
plt.title('Penggunaan Sepeda dari Hari ke Hari')
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Penggunaan Sepeda (cnt)')
plt.xticks(rotation=45) 
plt.tight_layout()

# Menampilkan grafik di Streamlit
st.pyplot(plt)


#Grafik Pengguna Sepeda Casual dan Pengguna yang sudah registered
st.subheader("Demografi Pelanggan dari Hari ke Hari")

col1, col2 = st.columns(2)

with col1:
    # Ambil 20 data pertama
    first_20 = day_df.iloc[:20]

    casual = first_20['casual']
    registered = first_20['registered']

    # Membuat bar plot
    categories = ['Casual', 'Registered']
    values = [casual.sum(), registered.sum()]

    plt.figure(figsize=(8, 6))
    plt.barh(categories, values, color=['skyblue', 'orange'])
    plt.xlabel('Jumlah Penggunaan Sepeda')
    plt.title('Penggunaan Sepeda antara Pengguna Casual dan Registered')

    st.pyplot(plt)

with col2: 
    # Mengelompokkan data berdasarkan 'holiday' dan menghitung total 'cnt' per 'holiday'
    holiday_data = day_df.groupby('holiday')['cnt'].sum()

    # Membuat daftar nama untuk 'holiday'
    holiday_names = ['Hari Biasa', 'Hari Libur']

    plt.figure(figsize=(8, 6))
    plt.barh(holiday_names, holiday_data, color=['skyblue', 'orange'])
    plt.ylabel('Jumlah Penggunaan Sepeda')
    plt.title('Penggunaan Sepeda pada Hari Libur dan Hari Biasa')

    st.pyplot(plt)


st.subheader("Temperature dari hari ke hari")

mean_temp = filtered_day['temp'].mean()
st.metric('Rata-Rata Suhu : ', value=mean_temp)
# Ambil data 'dteday' dan 'temp'
# Ambil 20 data pertama
first_20 = day_df.iloc[:20]

date = first_20['dteday']
temp = first_20['temp']

plt.figure(figsize=(10, 6))
plt.plot(date, temp, marker='o', color='b', linewidth=2, markersize=8)
plt.xlabel('Tanggal')
plt.ylabel('Suhu')
plt.title('Perubahan Suhu dari Hari ke Hari')
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(plt)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import io

sns.set(style='dark')

def get_total_count_by_hour_df(hour_df):
    hour_count_df = hour_df.groupby(by="hr").agg({"cnt": ["sum"]})
    hour_count_df.columns = ['total_count']
    return hour_count_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query('dteday >= "2011-01-01" and dteday < "2012-12-31"')
    return day_df_count_2011

def total_registered_df(day_df):
    reg_df = day_df.groupby(by="dteday").agg({
        "registered": "sum"
    })
    reg_df = reg_df.reset_index()
    reg_df.rename(columns={"registered": "register_sum"}, inplace=True)
    return reg_df

def total_casual_df(day_df):
    cas_df = day_df.groupby(by="dteday").agg({
        "casual": ["sum"]
    })
    cas_df = cas_df.reset_index()
    cas_df.rename(columns={"casual": "casual_sum"}, inplace=True)
    return cas_df

def sum_order(hour_df):
    sum_order_items_df = hour_df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def macem_season(day_df):
    season_df = day_df.groupby(by="season").cnt.sum().reset_index()
    return season_df

# Membaca data
days_df = pd.read_csv("day.csv")
hours_df = pd.read_csv("hour.csv")

# Mengatur tampilan DataFrame
datetime_columns = ["dteday"]
for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

# Inisialisasi aplikasi Streamlit
with st.sidebar:
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days]
    )

main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & (days_df["dteday"] <= str(end_date))]
main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) & (hours_df["dteday"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = macem_season(main_df_hour)

# Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Dashboard visualisasi data bisnis pinjaman sepeda :sparkles:')
st.subheader('Information')

col1, col2, col3 = st.columns(3)
with col1:
    total_orders = day_df_count_2011.cnt.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

st.subheader("1. Pada jam berapa saja yang paling banyak di sewakan dan paling sedikit disewakan? ")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(x="hr", y="cnt", data=sum_order_items_df.head(5), palette=["#EE4266", "#EE4266", "#87A922", "#EE4266", "#EE4266"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hours (PM)", fontsize=30)
ax[0].set_title("Jam dengan banyak penyewa sepeda", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="hr", y="cnt", data=sum_order_items_df.sort_values(by="hr", ascending=True).head(5), palette=["#EE4266", "#EE4266", "#EE4266", "#EE4266","#87A922"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hours (AM)", fontsize=30)
ax[1].set_title("Jam dengan sedikit penyewa sepeda", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

# Menyimpan subplot pertama
buffer = io.BytesIO()
fig.savefig(buffer, format='png')
buffer.seek(0)

# Inisialisasi aplikasi Streamlit
st.subheader('Information')

# Menampilkan subplot pertama di Streamlit
st.image(buffer)

# Catatan keterangan
st.write("Pada gambar di atas dapat kita lihat bahwa penyewaan sepedah paling banyak adalah jam 17.00 dan berbeda dengan jam dengan sedikit penyewaan sepeda adalah pada jam 04.00.")

st.subheader("2. Pada musim apasaja penyewaan sepeda terendah?")
colors = ["#EE4266", "#EE4266", "#EE4266", "#87A922"]
# Definisikan data frame day_df
day_df = pd.DataFrame({
    'season': ['Spring', 'Summer', 'Autumn', 'Winter'],
    'count_cr': [100, 200, 150, 180]  # contoh data penyewaan untuk setiap musim
})

# palette warna
colors = ["#EE4266", "#EE4266", "#87A922", "#EE4266"]

# subplot dengan 1 baris dan 1 kolom, dengan ukuran (20, 10)
fig, ax = plt.subplots(figsize=(20, 10))

# barplot untuk y="season" dan x="count_cr", menggunakan data=day_df
sns.barplot(
    x="count_cr", 
    y="season",
    data=day_df.sort_values(by="season", ascending=False),
    palette=colors,
    ax=ax
)

# mengatur judul, label y dan x, serta tick params untuk subplot tersebut
ax.set_title("Grafik Antar Musim", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)

# Menyimpan subplot kedua
buffer = io.BytesIO()
fig.savefig(buffer, format='png')
buffer.seek(0)

# Inisialisasi aplikasi Streamlit
st.subheader('Information')

# Menampilkan subplot kedua di Streamlit
st.image(buffer)

# Catatan keterangan
st.write("Berdasarkan hasil di atas dapat kita lihat bahwa spring menjadikan musim paling rendah penyewaan")


st.subheader("3. Berapa banyak seseorang yang memilih registered dibandingkan dengan casual?")
# Data contoh
data = {
    'holiday': [0, 0, 1, 1, 0],
    'weekday': [0, 1, 2, 3, 4],
    'casual': [10, 20, 30, 40, 50],
    'registered': [100, 200, 300, 400, 500]
}

# Membuat DataFrame dari data
day_df = pd.DataFrame(data)

# Menggunakan metode groupby() untuk mengelompokkan data berdasarkan 'holiday' dan 'weekday',
# kemudian menjumlahkan kolom 'casual' dan 'registered' untuk setiap kelompok
grouped_data = day_df.groupby(['holiday', 'weekday'])[['casual', 'registered']].sum()

# Mengambil total casual dan registered untuk setiap kelompok
total_casual = grouped_data['casual'].values
total_registered = grouped_data['registered'].values

# Membuat data untuk pie chart
labels = ['Casual', 'Registered']
sizes = [sum(total_casual), sum(total_registered)]

# Membuat plot
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#D3D3D3', '#72BCD4'])
ax.axis('equal')  # Membuat lingkaran menjadi lingkaran

# Membuat donut hole
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig.gca().add_artist(centre_circle)

# Menyimpan plot
buffer = io.BytesIO()
plt.savefig(buffer, format='png')
buffer.seek(0)

# Inisialisasi aplikasi Streamlit
st.subheader('Information')

# Menampilkan plot di Streamlit
st.image(buffer)

# Catatan keterangan
st.write("Dari hasil di atas dapat di gambarkan bahwa data orang yang ter registerd yaitu sebanyak 90,9% sedangkan yang belum melakukan registerd/casual yaitu sebanyak 9,1%.")

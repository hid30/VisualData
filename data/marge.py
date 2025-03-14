import pandas as pd

# Load kedua file CSV
df_day = pd.read_csv("D:/Laskar Ai/Latihan Visualisasi Data/data/day.csv")
df_hour = pd.read_csv("D:/Laskar Ai/Latihan Visualisasi Data/data/hour.csv")

# Gabungkan data
df_combined = pd.concat([df_day, df_hour], ignore_index=True)

# Simpan dalam folder dashboard
output_path = "D:/Laskar Ai/Latihan Visualisasi Data/dashboard/all_data.csv"
df_combined.to_csv(output_path, index=False)

print(f"Gabungan data berhasil disimpan dalam {output_path}")

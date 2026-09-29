import pandas as pd

df = pd.read_csv('data.csv')
print(f"Filas: {len(df)}")
print(f"Track_id únicos: {df['track_id'].nunique()}")

repetdias = df[df['track_id'].duplicated(keep=False)].sort_values("track_id")

columnas_interes = ["track_id", "track_name", "playlist_name", "playlist_genre"]
print(repetdias[columnas_interes].head(10))
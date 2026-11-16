import pandas as pd 
import numpy as np
np.random.seed(42)
nombre=300
echantillons=[
    f"S{i:03d}" for i in range(1,nombre+1)
]
concentrations=np.random.normal(
    loc=10.0,
    scale=0.25,
    size=nombre
)
temperatures=np.random.normal(
    loc=25,
    scale=1.5,
    size=nombre
)
df=pd.DataFrame({
    "Echantillon":echantillons,
    "concentration":concentrations,
    "temperature":temperatures
})
df.to_csv("resultats_300.csv",index=False)
print("Dataset ee avec succes !")
print(df.head())
print("Nombre d'echantillons:",len(df))
import pandas as pd
#charger les donnees
df=pd.read_csv("resultats_300.csv")
#Definir les limites
limite_min=9.5
limite_max=10.5
#verifier la conformite
df["conformite"]=df["concentration"].apply(
    lambda x:"conforme" if limite_min<= x <= limite_max else "Non conforme"
)
#calculer les statistiques
print("Nombre total:",len(df))
print("Nombre conforme:",(df["conformite"]=="conforme").sum())
print("Nombre non conforme:",(df["conformite"]=="Non conforme").sum())
#calculer le pourcentage
pourcentage=(df["conformite"]=="conforme").mean()*100
print("pourcentage de confomite:",round(pourcentage,2),"%")
print("\n----Statistique descriptives---")
print("Moyenne:",df["concentration"].mean())
print("Minimum:",df["concentration"].min())
print("Maximum:",df["concentration"].max())
print("Ecart_type:",df["concentration"].std())
import matplotlib.pyplot as plt
plt.figure(figsize=(8,5))
plt.hist(df["concentration"],bins=20,edgecolor="black")
plt.axvline(limite_min,color="red",linestyle="--",
            label="limite minimale")
plt.axvline(limite_max,color="red",linestyle="--",
            label="limite maximale")
plt.title("Distribution des concentrations")
plt.xlabel("concentration")
plt.ylabel("Nombre d'echantillons")
plt.legend()
plt.tight_layout()
plt.savefig("histogramme_concentrations.png")
plt.show()
# comparson des echantillons conformes et non conformes
comptage=df["conformite"].value_counts()
plt.figure(figsize=(7,5))
comptage.plot(kind="bar",edgecolor="black")
plt.title("Conformite des echantillons")
plt.xlabel("Statut")
plt.ylabel("Nombre d'echantillons")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("comparaison_conformite.png")
plt.show()
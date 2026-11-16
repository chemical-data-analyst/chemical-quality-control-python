import pandas as pd
import numpy as np 
from openpyxl import load_workbook
from openpyxl.styles import Font,PatternFill, Alignment
from openpyxl.chart import BarChart,Reference
# charger les donnes
df=pd.read_csv("resultats_300.csv")
#Definir les limites
limite_min=9.5
limite_max=10.5
#verifier la conformite
df["conformite"]=df["concentration"].apply(
    lambda x :"conforme" if limite_min<= x <= limite_max
    else "Nom conforme"
)
print("Donnees chargees avec succes !")
print(df.head())
#calculer les statistiques
nombre_total=len(df)
nombre_conforme=(df["conformite"]=="conforme").sum()
nombre_non_conforme=nombre_total-nombre_conforme
pourcentage=nombre_conforme/nombre_total*100
statistiques=pd.DataFrame({
    "Indicateur":[
        "Nombre totale",
        "Nombre conforme",
        "Nombre non conforme",
        "Pourcentage de conformite",
        "Moyenne",
        "Minimum",
        "Maximum",
        "Ecart_type"
    ],
    "Valeur":[
        nombre_total,
        nombre_conforme,
        nombre_non_conforme,
        round(pourcentage,2),
        df["concentration"].mean(),
        df["concentration"].min(),
        df["concentration"].max(),
        df["concentration"].std()
    ]
})
#creer le fichier Excel
with pd.ExcelWriter("rappot_qc_300.xlsx",engine="openpyxl")as writer:
    df.to_excel(writer,sheet_name="Resultats",index=False)
    statistiques.to_excel(writer,sheet_name="Statistiques",index=False)
    print("Rapport Excel cree avec succes !")
# ouvrir le fichier Excel
wb=load_workbook("rappot_qc_300.xlsx")
#couleurs
bleu=PatternFill("solid",fgColor="1F4E78")
vert=PatternFill("solid",fgColor="C6EFCE")
rouge=PatternFill("solid",fgColor="FFC7CE")
# Parcourir les feuilles
for ws in wb.worksheets:
    # Formater les titres
    for cell in ws[1]:
        cell.fill=bleu
        cell.font=Font(color="FFFFFF",bold=True)
        cell.alignment=Alignment(horizontal="center")
    #Ajuster les colonnes
    for column in ws.columns:
        ws.column_dimensions[column[0].column_letter].width=25
    #Fixer la premiere ligne
    ws.freeze_panes="A2"
    #colorer les resultats
    ws=wb["Resultats"]
    for row in range(2,ws.max_row+1):
        cell=ws.cell(row=row,column=4)
        if cell.value=="conforme":
            cell.fill=vert
        else:
            cell.fill=rouge
#Enregister
wb.save("rappot_qc_300.xlsx")
#creer un graphique de conformite
ws_stats=wb["Statistiques"]
chart=BarChart()
chart.type="col"
chart.style=10
chart.title="Conformite des echantillons"
chart.y_axis.title="Nombre d'echantillons"
chart.x_axis.title="statut"
data=Reference(ws_stats,min_col=2,min_row=3,max_row=4)
categories=Reference(ws_stats,min_col=1,min_row=3,max_row=4)
chart.add_data(data,from_rows=False)
chart.set_categories(categories)
chart.legend=None
chart.height=8
chart.width=15
ws_stats.add_chart(chart,"J2")
#creer un histogramme des concentration 
ws_resultats=wb["Resultats"]
ws_stats=wb["Statistiques"]
frequences,limites=np.histogram(
    df["concentration"],bins=10
)
#creer le tableau des frequences
ws_stats["G11"]="Intervalle"
ws_stats["H11"]="Frequence"
for i in range(10):
    ligne=i+12
    ws_stats.cell(
        row=ligne,
        column=7,
        value=f"{limites[i]:.2f} - {limites[i+1]:.2f}"
    )
    ws_stats.cell(
        row=ligne,
        column=8,
        value=int(frequences[i])
    )
#creer le graphique
histogramme=BarChart()
histogramme.gapWidth=0
histogramme.type="col"
histogramme.style=10
histogramme.title="Distribution des concentrations"
histogramme.x_axis.title="Concentration"
histogramme.y_axis.title="Nombre d'echantillons"
data=Reference(
    ws_stats,min_col=8,min_row=11,max_row=21
)
categories=Reference(
    ws_stats,min_col=7,min_row=12,max_row=21
)
histogramme.add_data(data,titles_from_data=True)
histogramme.set_categories(categories)
histogramme.legend=None
histogramme.height=8
histogramme.width=15
ws_stats.add_chart(histogramme,"J18")

# enregistrer le fichier
wb.save("rappot_qc_300.xlsx")
print(" les deux graphiques sont ajoutes avec succes!")



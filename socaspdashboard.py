import panel as pn
import pandas as pd
import numpy as np
import hvplot.pandas
import datetime as dt

pn.extension('tabulator', 'echarts')

# ===================== SAMPLE DATA =====================
np.random.seed(42)

dates = pd.date_range(start="2024-01-01", periods=50, freq='15D')
# origines = ['Douala', 'Libreville', 'Pointe-Noire']
# provenances = ['China', 'France', 'Nigeria']
# marketeurs = ['Total', 'Ola Energy', 'Tradex']

df_origine = pd.read_excel("./type/origine_data.xlsx")
df_provenance = pd.read_excel("./type/provenance_data.xlsx")
df_marketeur = pd.read_excel("./type/marketeur_data.xlsx")

origines = list(df_origine['origine_one'].unique())
provenances = list(df_provenance['provenance_one'].unique())
marketeurs = list(df_marketeur['marketeur_one'].unique())


# Importations
# df_importations = pd.DataFrame({
#     'anneemois': np.random.choice(dates, 50),
#     'origine': np.random.choice(origines, 50),
#     'provenance': np.random.choice(provenances, 50),
#     'marketeur': np.random.choice(marketeurs, 50),
#     'jet': np.random.randint(200, 2000, 50)
# })

df_importations = pd.read_excel("./data/importation.xlsx")

df_importations['type'] = 'Importation'

# Distributions
# df_distributions = pd.DataFrame({
#     'anneemois': np.random.choice(dates, 50),
#     'origine': np.random.choice(origines, 50),
#     'provenance': np.random.choice(provenances, 50),
#     'marketeur': np.random.choice(marketeurs, 50),
#     'jet': np.random.randint(100, 1800, 50)
# })

df_distributions = pd.read_excel("./data/distribution.xlsx")

df_distributions['type'] = 'Distribution'

df = pd.concat([df_importations, df_distributions])

# ===================== FILTER WIDGETS =====================
origine_select = pn.widgets.Select(name="Origine", options=['All'] + origines, value='All')
provenance_select = pn.widgets.Select(name="Provenance", options=['All'] + provenances, value='All')
marketeur_select = pn.widgets.Select(name="Marketeur", options=['All'] + marketeurs, value='All')

# ===================== FILTER FUNCTION =====================
@pn.depends(origine_select, provenance_select, marketeur_select)
def filtered_data(origine, provenance, marketeur):
    data = df.copy()
    if origine != 'All':
        data = data[data['origine'] == origine]
    if provenance != 'All':
        data = data[data['provenance'] == provenance]
    if marketeur != 'All':
        data = data[data['marketeur'] == marketeur]
    return data

@pn.depends(marketeur_select)
def filtered_data_marketeur(marketeur):
    data = df.copy()
    if marketeur != 'All':
        data = data[data['marketeur'] == marketeur]
    return data

# ===================== KPI CARDS =====================
@pn.depends(origine_select, provenance_select, marketeur_select)
def kpi_view(origine, provenance, marketeur):
    data = filtered_data(origine, provenance, marketeur)
    if data.empty:
        return pn.pane.Markdown("### ❗Aucune donnée disponible pour ce filtre", style={'color': 'red'})

    total_qte = data['jet'].sum()
    nb_import = len(data[data['type'] == 'Importation'])
    nb_dist = len(data[data['type'] == 'Distribution'])
    avg_qte = data['jet'].mean()

    return pn.Row(
        pn.pane.Markdown(f"### 📦 Total Quantité: **{total_qte:,.0f}**", styles={'background': '#F0F4F8', 'padding': '10px'}),
        pn.pane.Markdown(f"### 🚢 Importations: **{nb_import}**", styles={'background': '#E3F2FD', 'padding': '10px'}),
        pn.pane.Markdown(f"### 🚚 Distributions: **{nb_dist}**", styles={'background': '#FFF3E0', 'padding': '10px'}),
        pn.pane.Markdown(f"### 📊 Quantité Moyenne: **{avg_qte:,.1f}**", styles={'background': '#E8F5E9', 'padding': '10px'}),
        sizing_mode="stretch_width"
    )

# ===================== CHARTS =====================
@pn.depends(origine_select, provenance_select, marketeur_select)
def charts_view(origine, provenance, marketeur):
    data = filtered_data(origine, provenance, marketeur)
    if data.empty:
        return pn.pane.Markdown("### ❗Aucune donnée pour générer les graphiques", style={'color': 'red'})

    bar_chart = data.groupby(['type'])['jet'].sum().hvplot.bar(
        title="Quantité Totale par Type", ylabel="Quantité", xlabel="Type", height=360, width=810
    )

    line_chart = data.groupby(['anneemois', 'type'])['jet'].sum().reset_index().hvplot.line(
        x='anneemois', y='jet', by='type', title="Évolution Temporelle", height=360, width=810
    )

    heatmap = data.groupby(['origine', 'marketeur'])['jet'].sum().reset_index().hvplot.heatmap(
        x='origine', y='marketeur', C='jet', cmap='Blues', title="Chaleur des Quantités", height=360, width=810
    )

    return pn.Row(
        pn.Tabs(
            pn.Row(
                pn.Column(
                    bar_chart,
                ),
            ),

            pn.Row(
                pn.Column(
                    line_chart,
                ),
            ),

            pn.Row(
                pn.Column(
                    heatmap,
                ),
            )
        )
    )

    

# ===================== DATA TABLES =====================
@pn.depends(origine_select, provenance_select, marketeur_select)
def importation_table(origine, provenance, marketeur):
    data = filtered_data(origine, provenance, marketeur)
    return data[data['type'] == 'Importation'][['anneemois','origine','provenance','marketeur', 'essence', 'jet', 'petrole', 'gazoil']].sort_values('anneemois').reset_index(drop=True)

@pn.depends(marketeur_select)
def distribution_table(marketeur):
    data = filtered_data_marketeur(marketeur)
    return data[data['type'] == 'Distribution'][['anneemois','marketeur', 'essence', 'jet', 'petrole', 'gazoil']].sort_values('anneemois').reset_index(drop=True)

# ===================== PAGES =====================
def page_dashboard():
    return pn.Column(kpi_view, charts_view, sizing_mode="stretch_width")

def page_importations():
    return pn.Column("### 📑 Table des Importations", pn.widgets.Tabulator(importation_table, pagination='remote', page_size=13))

def page_distributions():
    return pn.Column("### 📑 Table des Distributions", pn.widgets.Tabulator(distribution_table, pagination='remote', page_size=13))

# ===================== NAVIGATION =====================
main_area = pn.Column()

def show_page(page_func):
    main_area.clear()
    main_area.append(page_func())

nav_buttons = pn.Row(
    pn.widgets.Button(name="🏠 Dashboard", button_type="primary", width=250, height=75),
    pn.widgets.Button(name="📥 Importations", button_type="success", width=250, height=75),
    pn.widgets.Button(name="📤 Distributions", button_type="warning", width=250, height=75),
    sizing_mode="stretch_width"
)

def on_dashboard_click(event): show_page(page_dashboard)
def on_importations_click(event): show_page(page_importations)
def on_distributions_click(event): show_page(page_distributions)

nav_buttons[0].on_click(on_dashboard_click)
nav_buttons[1].on_click(on_importations_click)
nav_buttons[2].on_click(on_distributions_click)

# Default view
show_page(page_dashboard)

# ===================== FINAL LAYOUT =====================
filters = pn.WidgetBox("<h3>🔎 Filtres</h3>", origine_select, provenance_select, marketeur_select, width=320)
layout = pn.Row(filters, pn.Column(nav_buttons, main_area, sizing_mode="stretch_width"))

layout.servable()

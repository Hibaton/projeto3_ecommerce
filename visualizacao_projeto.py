import pandas as pd
import plotly.express as px
from dash import Dash,dcc,html

def cria_graficos(df):

    # Histograma
    fig1 =px.histogram(df, x='Nota', nbins=10)
    fig1.update_layout(
       xaxis_title='Nota',
       yaxis_title='Frequência',
       title='Distribuição das Notas dos Produtos'
    )
    # Remover duplicatas para obter valores únicos por marca
    df_unico = df[["Marca", "Marca_Freq"]].drop_duplicates()
    # Selecionar as 10 marcas mais registradas
    df_top20 = df_unico.nlargest(20, "Marca_Freq")
    explode = [0.05] * len(df_top20)  # Destacar fatias levemente
    fig2 = px.pie(df_top20, names='Marca', values='Marca_Freq', hole=0.2,
                  color_discrete_sequence=px.colors.qualitative.Pastel,title='Marcas Mais Registradas')

    fig3 =px.scatter(df,x='Desconto',y='Qtd_Vendidos_Cod',color='Gênero',color_discrete_sequence=px.colors.qualitative.Pastel)
    fig3.update_layout(
        title='Dispersão de Preço vs Quantidade Vendida e Gênero',
        xaxis_title='Preço',
        yaxis_title='Quantidade Vendida'
    )
    # Grafico da barra
    top_20_marcas = df.groupby("Marca")["Qtd_Vendidos_Cod"].sum().nlargest(20).index

    df_top20 = (
    df[df["Marca"].isin(top_20_marcas)].groupby(["Marca", "Gênero"], as_index=False)
            ["Qtd_Vendidos_Cod"].sum()
        )

    # 3. Criar com nomes das colunas corretas
    fig4 = px.bar(
        df_top20.sort_values(by='Qtd_Vendidos_Cod',ascending=False),
            x="Marca",
            y="Qtd_Vendidos_Cod",  # This should now exist
            color="Gênero",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            opacity=1,
            barmode="group",
            title="Top 20 Marcas Mais Vendidas por Gênero"
        )
    fig4.update_layout(
        yaxis_title='Quantidade Vendida'
    )

    return fig1, fig2, fig3, fig4
def cria_app(df):
        #  cria App
        app = Dash(__name__)
        fig1, fig2, fig3, fig4 = cria_graficos(df)
        app.layout = html.Div([
            html.H1('Graficos de E-commerce',style={'textAlign': 'center'}),
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig4),

        ])
        return app

df = pd.read_csv(r"C:\Users\moha_\Downloads\ecommerce_estatistica.csv")

if __name__ == '__main__':
    app = cria_app(df)
    app.run(debug=True, port=8050)  # Default 8050


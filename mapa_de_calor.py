import pandas as pd
import plotly.express as px
from dash import Dash,html,dcc



def cria_graficos(df):
    # DataFrame usado para correlacao
    df_corr=df[['Preço','Nota_MinMax','N_Avaliações_MinMax','Desconto_MinMax','Qtd_Vendidos_Cod']].corr()
    # renomear os nomes das colunas
    df_renomeado = df_corr.rename(columns={
         "Preco": "Preço",
         "Nota_MinMax": "Nota Normalizada",
         "N_Avaliações_MinMax": "Avaliações",
         "Desconto_MinMax": "Desconto",
         "Qtd_Vendidos_Cod": "Qtd Vendidos"
    }, index={
         "Preco": "Preço",
         "Nota_MinMax": "Nota Normalizada",
         "N_Avaliações_MinMax": "Avaliações",
         "Desconto_MinMax": "Desconto",
         "Qtd_Vendidos_Cod": "Qtd Vendidos"
    })

    # Criacao do mapa de calor
    fig1 = px.imshow(df_renomeado,
                text_auto=True,
                color_continuous_scale='RdBu_r',
                title='Matriz de Correlacao',
                width=800,
                height=600
                )
    # Grafico de regressao (scatter + linha)
    fig2 = px.scatter(
        df,
        x='N_Avaliações',
        y='Qtd_Vendidos_Cod',
        trendline='ols')
    fig2.update_layout(
        title='Regressao de Avaliações por Quantidade Vendida ',
         xaxis_title= 'Numero de Avaliações',
         yaxis_title= 'Quantidade Vendida'
    )
    return fig1, fig2
def cria_app(df):

      app = Dash(__name__)
      fig1, fig2 = cria_graficos(df)
      app.layout = html.Div([
           html.H1('Analise de Correlacao e Regressao ',style={'textAlign': 'center'}),
          html.Div([
           dcc.Graph(figure=fig1,style={'width':'48%','display':'inline-block','verticalAlign':'Top'}),
              html.Div([
           dcc.Graph(figure=fig2,style={'width':'48%','display':'inline-block','verticalAlign':'Top','marginLeft':'4%'})
           ])
          ])
      ])
      return app

# ler os dados no DataFrame
df = pd.read_csv(r"C:\Users\moha_\Downloads\ecommerce_estatistica.csv")

if __name__ == '__main__':
    app = cria_app(df)
    app.run(debug=True, port=8050)  # Default 8050
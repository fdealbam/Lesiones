#Lesiones

import dash
import matplotlib.pyplot as plt 
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
import numpy as np
import dash_table
import sidetable as stb
import datetime
from datetime import datetime, timedelta
from datetime import date
import geopandas as gpd
import flask
import os

yesterday = datetime.now() - timedelta(1)
yea = datetime.strftime(yesterday, '%Y%m%d')

today = date.today()
d2 = today.strftime("Fecha de actualización : %d-%m-%Y")



###############################
# DATABASES
############################### Abre archivos


#os.chdir(r"C:\Users\PRIME\AnacondaProjects\Project_curso\\")

delitos = pd.read_csv("https://raw.githubusercontent.com/fdealbam/Lesiones/main/Lesiones2015_2021.csv")
delitos.drop('Unnamed: 0',1, inplace=True)

delitos.groupby(['Año','Entidad','Tipo de delito'])['Enero', 
                 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
       'Julio', 'Agosto', 'Septiembre', 'Octubre',
       'Noviembre', 'Diciembre'].sum().to_csv("00.csv",  header=True)

fem= pd.read_csv("00.csv")

############################################### separación de años

year15= fem[fem.Año == 2015]
year16= fem[fem.Año == 2016]
year17= fem[fem.Año == 2017]
year18= fem[fem.Año == 2018]
year19= fem[fem.Año == 2019]
year20= fem[fem.Año == 2020]
year21= fem[fem.Año == 2021]

############################################### Agregar suffix de años

y15 = year15.add_suffix('15')
y15.rename(columns ={'Año15': 'Año', 'Tipo de delito15': 'Tipo de delito', 'Unnamed: 015' : 'Unnamed: 0',
                            'Entidad15': 'Entidad'}, inplace = True)

y16 = year16.add_suffix('16')
y16.rename(columns ={'Año16': 'Año', 'Tipo de delito16': 'Tipo de delito', 'Unnamed: 016' : 'Unnamed: 0',
                            'Entidad16': 'Entidad'}, inplace = True)

y17 = year17.add_suffix('17')
y17.rename(columns ={'Año17': 'Año', 'Tipo de delito17': 'Tipo de delito', 'Unnamed: 017' : 'Unnamed: 0',
                            'Entidad17': 'Entidad'}, inplace = True)

y18= year18.add_suffix('18')
y18.rename(columns ={'Año18': 'Año', 'Tipo de delito18': 'Tipo de delito','Unnamed: 018' : 'Unnamed: 0',
                            'Entidad18': 'Entidad'}, inplace = True)

y19= year19.add_suffix('19')
y19.rename(columns ={'Año19': 'Año', 'Tipo de delito19': 'Tipo de delito', 'Unnamed: 019' : 'Unnamed: 0',
                            'Entidad19': 'Entidad'}, inplace = True)

y20= year20.add_suffix('20')
y20.rename(columns ={'Año20': 'Año', 'Tipo de delito20': 'Tipo de delito','Unnamed: 020' : 'Unnamed: 0',
                            'Entidad20': 'Entidad'}, inplace = True)

y21= year21.add_suffix('21')
y21.rename(columns ={'Año21': 'Año', 'Tipo de delito21': 'Tipo de delito','Unnamed: 021' : 'Unnamed: 0',
                            'Entidad21': 'Entidad'}, inplace = True)



############################################### Concat todos los años

fa = y15.merge(y16, on="Entidad",  how="inner")
fb = fa.merge(y17, on="Entidad",  how="inner")
fc = fb.merge(y18, on="Entidad",  how="inner")
fd = fc.merge(y19, on="Entidad",  how="inner")
fe = fd.merge(y20, on="Entidad",  how="inner")
ff = fe.merge(y21, on="Entidad",  how="inner")
                    
femi15_21 = ff[[
 'Entidad','Enero15','Febrero15','Marzo15','Abril15','Mayo15','Junio15',
 'Julio15','Agosto15','Septiembre15','Octubre15','Noviembre15','Diciembre15',
 
 'Enero16','Febrero16','Marzo16','Abril16','Mayo16','Junio16','Julio16',
 'Agosto16','Septiembre16','Octubre16','Noviembre16','Diciembre16',

 'Enero17','Febrero17','Marzo17','Abril17','Mayo17','Junio17','Julio17',
 'Agosto17','Septiembre17','Octubre17','Noviembre17','Diciembre17',
    
 'Enero18','Febrero18','Marzo18','Abril18','Mayo18','Junio18','Julio18',
 'Agosto18','Septiembre18','Octubre18','Noviembre18','Diciembre18',
 
 'Enero19','Febrero19','Marzo19','Abril19','Mayo19','Junio19','Julio19',
 'Agosto19','Septiembre19','Octubre19','Noviembre19','Diciembre19',

 'Enero20','Febrero20','Marzo20','Abril20','Mayo20','Junio20','Julio20',
 'Agosto20','Septiembre20','Octubre20','Noviembre20','Diciembre20',
    
 'Enero21','Febrero21','Marzo21','Abril21','Mayo21','Junio21',#'Julio21',
# 'Agosto21','Septiembre21','Octubre21','Noviembre21','Diciembre21'
             ]]



##CRear columna de TOTAL ANUAL 
femi15_21['Total2015']= femi15_21[[ 'Enero15', 'Febrero15', 'Marzo15', 'Abril15', 'Mayo15',
                               'Junio15', 'Julio15', 'Agosto15', 'Septiembre15', 'Octubre15',
                               'Noviembre15', 'Diciembre15',]].sum(axis=1)
femi15_21['Total2016']= femi15_21[[ 'Enero16', 'Febrero16', 'Marzo16', 'Abril16', 'Mayo16',
                               'Junio16', 'Julio16', 'Agosto16', 'Septiembre16', 'Octubre16',
                               'Noviembre16', 'Diciembre16',]].sum(axis=1)
femi15_21['Total2017']= femi15_21[[ 'Enero17', 'Febrero17', 'Marzo17', 'Abril17', 'Mayo17',
                               'Junio17', 'Julio17', 'Agosto17', 'Septiembre17', 'Octubre17',
                               'Noviembre17', 'Diciembre17',]].sum(axis=1)
femi15_21['Total2018']= femi15_21[[ 'Enero18', 'Febrero18', 'Marzo18', 'Abril18', 'Mayo18',
                               'Junio18', 'Julio18', 'Agosto18', 'Septiembre18', 'Octubre18',
                               'Noviembre18', 'Diciembre18',]].sum(axis=1)
femi15_21['Total2019']= femi15_21[[ 'Enero19', 'Febrero19', 'Marzo19', 'Abril19', 'Mayo19',
                               'Junio19', 'Julio19', 'Agosto19', 'Septiembre19', 'Octubre19',
                               'Noviembre19', 'Diciembre19',]].sum(axis=1)
femi15_21['Total2020']= femi15_21[[ 'Enero20', 'Febrero20', 'Marzo20', 'Abril20', 'Mayo20',
                               'Junio20', 'Julio20', 'Agosto20', 'Septiembre20', 'Octubre20',
                               'Noviembre20', 'Diciembre20',]].sum(axis=1)

femi15_21['Total2021']= femi15_21[[ 'Enero21','Febrero21', 'Marzo21', 'Abril21', 'Mayo21',
                                   'Junio21',#'Julio21','Agosto21','Septiembre21','Octubre21',
                                   #'Noviembre21','Diciembre21'
                                  ]].sum(axis=1)


#identificadores
conf_2015= femi15_21.Total2015.sum().astype(int)
conf_2016= femi15_21.Total2016.sum().astype(int)
conf_2017= femi15_21.Total2017.sum().astype(int)
conf_2018= femi15_21.Total2018.sum().astype(int)
conf_2019= femi15_21.Total2019.sum().astype(int)
conf_2020= femi15_21.Total2020.sum().astype(int)
conf_2021= femi15_21.Total2021.sum().astype(int)



################################################## PREPARA GRAFICA MENSUAL
pagra = ff[[
  'Enero15', 'Febrero15', 'Marzo15', 'Abril15', 'Mayo15', 'Junio15', 'Julio15', 'Agosto15', 
    'Septiembre15', 'Octubre15', 'Noviembre15', 'Diciembre15',
 
 'Enero16', 'Febrero16', 'Marzo16', 'Abril16', 'Mayo16', 'Junio16', 'Julio16', 'Agosto16', 
    'Septiembre16', 'Octubre16', 'Noviembre16', 'Diciembre16',

 'Enero17', 'Febrero17', 'Marzo17', 'Abril17', 'Mayo17', 'Junio17', 'Julio17', 'Agosto17', 
    'Septiembre17', 'Octubre17', 'Noviembre17', 'Diciembre17', 
    'Enero18', 'Febrero18', 'Marzo18',    'Abril18', 'Mayo18', 'Junio18', 'Julio18', 'Agosto18',
    'Septiembre18', 'Octubre18', 'Noviembre18', 'Diciembre18',
 
 'Enero19', 'Febrero19', 'Marzo19', 'Abril19', 'Mayo19', 'Junio19', 'Julio19', 'Agosto19', 
    'Septiembre19', 'Octubre19', 'Noviembre19', 'Diciembre19',

 'Enero20', 'Febrero20', 'Marzo20', 'Abril20', 'Mayo20', 'Junio20', 'Julio20', 'Agosto20',
    'Septiembre20','Octubre20', 'Noviembre20', 'Diciembre20',

 'Enero21', 'Febrero21', 'Marzo21','Abril21', 'Mayo21', 'Junio21',# 'Julio21', 'Agosto21',
  #  'Septiembre21','Octubre21','Noviembre21','Diciembre21'
            ]]


pagrafm = pagra.stb.subtotal()
pagrafm.to_csv("0000procesod.csv")
#Selecciona ultima columna (Totales)
other  = pd.read_csv('0000procesod.csv')
other_s = other.iloc[32]
other_b = pd.DataFrame(other_s)
other_b.to_csv('0000procesodi.csv')
vuelve_a_abrir = pd.read_csv('0000procesodi.csv')
##Elimina filas 0 a 4 
gra_mes = vuelve_a_abrir.drop([0])
#Renombra titulo de columna
gra_mes = gra_mes.rename(columns= {"Unnamed: 0": "Mes"})
gra_mes = gra_mes.rename(columns= {"32": "Total"})
gra_mes['Total'] = pd.to_numeric(gra_mes['Total'])


#Grafica mensual 
graf_meses = go.Figure()
graf_meses.add_trace(go.Bar(x=gra_mes['Mes'],y=gra_mes['Total'],
                marker_color='indianred'  # cambiar nuemeritos de rgb
                ))
graf_meses.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_tickangle=-45,
    template = 'simple_white',
    title='',
    xaxis_tickfont_size= 12,
    yaxis=dict(
        title='Acumulados mensuales',
        titlefont_size=14,
        tickfont_size=12,
        titlefont_family= "Monserrat"),
    #autosize=False,
    #width=1000,
    #height=400
    )





################################################ SUMA TODOS LOS AÑOS ranking de municipios por estado (3edos)

#filtro de feminicidio
delitos.groupby(['Municipio','Entidad',])['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo',
                                             'Junio','Julio', 'Agosto', 'Septiembre', 'Octubre',
                                             'Noviembre', 'Diciembre'].sum().to_csv('0000procesofem.csv')

fem_filter1=pd.read_csv('0000procesofem.csv')
fem_filter1[['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto',
                                 'Septiembre','Octubre','Noviembre','Diciembre']] = fem_filter1[['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto',
                                 'Septiembre','Octubre','Noviembre','Diciembre']].astype(int)
    
fem_filter1['Total']=fem_filter1[['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto',
                                 'Septiembre','Octubre','Noviembre','Diciembre']].sum(1)




#- FILE MUNICIPIOS ------------------------------------------------------------------------------

fem_filter1.fillna(0, inplace=True) 
fem_filter1['Total']=fem_filter1['Total'].astype(int)








######################################################### Graf. Tasas de feminicidios por entidad 2015-2020

junto1 = pd.read_csv('https://raw.githubusercontent.com/fdealbam/feminicidios/main/application/POB_15_21.csv')
fem15_21 = femi15_21[['Entidad', 'Total2015', 'Total2016', 'Total2017',
       'Total2018', 'Total2019', 'Total2020', 'Total2021']]

junto15_21 = fem15_21.merge(junto1,right_on='NOM_ENT',left_on='Entidad')
junto15_21["Entidad"].replace('Veracruz de Ignacio de la Llave','Veracruz' , inplace=True)

junto15_21['Totfem1521']=junto15_21[['Total2015', 'Total2016', 'Total2017', 'Total2018','Total2019', 'Total2020', 'Total2021']].sum(1)
junto15_21['Totpob1521']=junto15_21[['POB15', 'POB16', 'POB17', 'POB18','POB19', 'POB20', 'POB21']].sum(1)
junto15_21['Tasa1521']=((junto15_21.Totfem1521/junto15_21.Totpob1521)*100000).round(2)



######################################################### Grafica tasa POR ENTIDAD
TasasFem15_21index=junto15_21[['Entidad','Totfem1521','Totpob1521','Tasa1521']].sort_values('Tasa1521',ascending=False)

graf_tasafem = go.Figure()
graf_tasafem.add_trace(go.Bar(x=TasasFem15_21index['Entidad'],y=TasasFem15_21index['Tasa1521'],
                marker_color='sandybrown'  # cambiar nuemeritos de rgb
                ))

graf_tasafem.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_tickangle=-45,
    template = 'simple_white',
    #title='Tasa feminicidio periodo 2015-2020',
    xaxis_tickfont_size= 12,
    yaxis=dict(
        title='Totales acumulados por entidad',
        titlefont_size=14,
        tickfont_size=12,
        titlefont_family= "Monserrat"),
    autosize=True,
#    width=2100,
#    height=600
    )


######################################################### Grafica de Totales por entidad 

TasasTot15_21index=junto15_21[['Entidad','Totfem1521','Totpob1521','Tasa1521']].sort_values('Totfem1521',ascending=False)

graf_totfem = go.Figure()
graf_totfem.add_trace(go.Bar(x=TasasTot15_21index['Entidad'],y=TasasTot15_21index['Totfem1521'],
                marker_color='indianred'  # cambiar nuemeritos de rgb
                ))

graf_totfem.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_tickangle=-45,
    template = 'simple_white',
    #title='Tasa feminicidio periodo 2015-2020',
    xaxis_tickfont_size= 12,
    yaxis=dict(
        title='Tasa cada 100 000 habitantes',
        titlefont_size=14,
        tickfont_size=12,
        titlefont_family= "Monserrat"),
    autosize=True,
 #   width=2100,
  #  height=600
    )





####################################

# A P P

####################################

########### Define your variables
mytitle=' '
tabtitle='Aborto'
sourceurl='https://www.gob.mx/sesnsp/acciones-y-programas/datos-abiertos-de-incidencia-delictiva?state=published'


server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes. LUX], server=server)

body = html.Div([
# Cintillo 000
    
   html.Br(),
    
   dbc.Row([
                                    #https://github.com/fdealbam/CamaraDiputados/blob/b11ef31e8e0f73e1a4a06ce60402563e1bd0122e/application/static/logocamara.jfif
           dbc.Col(dbc.CardImg(src="https://github.com/fdealbam/0entrada/blob/ce2cda9ccf7732861b8494b36562ebe9c8c642a6/application/static/logo%20cesopycamara.jpeg?raw=true"),
                        width=5, md={'size': 2,  "offset": 2, }),
            
           dbc.Col(html.H5(" Centro de Estudios Sociales y de Opinión Pública," 
                           " Cámara de Diputados"
                           " México, 2021 "),
                  width={'size': 3, 'offset': 0}),
               ], justify="end",),
            
   
   
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    
    
        dbc.Row(
           [
               dbc.Col(html.P("Lesiones"),
                        style={"font-size": 86, "text-align": "center",
                              "text-shadow": "10px 20px 30px black",}),
           ], justify= "start"),

#Cintillo 00    
    dbc.Row(
           [
               dbc.Col(html.H6(d2),           #Fecha de actualización
               width={'size' : "auto",
                      'offset' : 4}), 
               dbc.Col(html.H6("Fuente: SENSNSP"),
                        width={'size': 3,  "offset":1 }),
            ]),
               
       html.Br(),
       html.Br(),
       html.Br(),
    
       dbc.Row(
            [
                #html.H4("Consideraciones generales "),
                html.P(
                    "Las lesiones son una forma de violencia de género, al igual que en el caso de los homicidios, "
                    "las lesiones pueden ser dolosas (intencionales) o culposas (no intencionales); en el caso de las primeras, "
                    "constituyen otro de los rostros de la violencia que se vive en el país."
                    "Entre los años 2015 y 2021, se ha registrado un promedio anual de (X) víctimas de lesiones dolosas en el país,"
                    " teniendo la cifra más alta en el (año), con (x) víctimas, y la más baja en (año), con (x) víctimas ."
                    " Esas cifras implican, para todo el periodo, un promedio diario de (x) casos por día o prácticamente "
                    "(x) víctimas de lesiones dolosas cada hora. Esto sin considerar todos aquellos casos en que no se presenta "
                    "querella o que no procede la denuncia ante el ministerio público."
                     "" 
                    "además, son problemas aún irresueltos y son tema central de la " 
                    "agenda legislativa, pero hoy alcanzan relevancia en la agenda seguridad pública del país, también. "
                    "Este dashboard analítico se compone de una sección en la cual tratamos las lesiones, observamos "
                    "su gravedad según intervalos anuales o mensuales; incluimos el análisis detallado de cuatro "
                    "entidades con más incidencias de este delito; finalmente, comparamos los rankings por entidad "
                    "según sumas del periódo 2015 al 2021 con las tasas por entidad del mismo intervalo. " 
                    " "                    
                    "Hoy existen cada vez mayor atención institucional para atender la salud social y son fuerte "
                    "preocupación de la sociedad, esto último se evidencia en el hecho que todos seamos más vigilantes al respecto. "
                    "No obstante, aún hace falta más acción social, sobretodo, más intervención institucional "
                    "para diseñar estrategias efectivas de prevención y promover su denuncia. Es imperativo "
                    "acabar con estas violencias de género. "
                    "",
                    style= {"font-size":22,})], 
           
        style= {"margin-left":"100px", "margin-right":"100px", "text-align":"justify"},
       ),
                
       html.Br(),       
    html.Br(),
       html.Br(),
     
    
     html.Br(),
       html.Br(),
        dbc.Row(
           [
               dbc.Col(html.P("Evolución de la incidencia de lesiones" ),
                        style={"font-size": 56, "text-align": "left", "margin-left":"50px",
                              "text-shadow": "10px 20px 30px black",}),
           ], justify= "start"),
    
       html.Br(),
       html.Br(),
#cintillo 0
    
     dbc.Row(
           [
               dbc.Col(html.H1(["Casos ", 
                                dbc.Badge("anuales", color="info", className="mr-1")]),
                        width={'size': 8,  "offset":1 }),
            ]),

       html.Br(),
       html.Br(),
       html.Br(),
    
     dbc.Row(
           [
               dbc.Col(dbc.Button(([html.H5("2015", style={"font-size": 18,"color": "black","background-color": "white"}),
                                    html.H1([str(f"{conf_2015:,d}")],style={"font-size": 40, "color": "black","background-color": "white"}),
                                    dbc.CardImg(src="https://github.com/fdealbam/Lesiones/blob/main/application/static/Mapa%20lesiones%20Total2015.png?raw=true",
                                                               style={"background-color":"white"}),
               ]), style={"background-color":"white",
                         "box-shadow": "10px 20px 30px black",
                         'margin-left': '10px',
                        'width': '210px'
                         }, disabled=True)),
               
               dbc.Col(dbc.Button(([html.H5("2016", style={"font-size": 18,"color": "black","background-color": "white"}),
                                    html.H1([str(f"{conf_2016:,d}")],style={"font-size": 40, "color": "black","background-color": "white"}),
                                    dbc.CardImg(src="https://github.com/fdealbam/Lesiones/blob/main/application/static/Mapa%20lesiones%20Total2016.png?raw=true",
                                                 style={"background-color":"white"}),
               ]), style={"background-color":"white",
                         "box-shadow": "10px 20px 30px black",
                         
                        'width': '210px'
                         }, disabled=True)),
               dbc.Col(dbc.Button(([html.H5("2017", style={"font-size": 18,"color": "black","background-color": "white"}),
                                    html.H1([str(f"{conf_2017:,d}")],style={"font-size": 40, "color": "black","background-color": "white"}),
                                    dbc.CardImg(src="https://github.com/fdealbam/Lesiones/blob/main/application/static/Mapa%20lesiones%20Total2017.png?raw=true",
                                                 style={"background-color":"white"}),
               ]), style={"background-color":"white",
                         "box-shadow": "10px 20px 30px black",
                         
                        'width': '210px'
                         }, disabled=True)),
               dbc.Col(dbc.Button(([html.H5("2018", style={"font-size": 18,"color": "black","background-color": "white"}),
                                    html.H1([str(f"{conf_2018:,d}")],style={"font-size": 40, "color": "black","background-color": "white"}),
                                    dbc.CardImg(src="https://github.com/fdealbam/Lesiones/blob/main/application/static/Mapa%20lesiones%20Total2018.png?raw=true",
                                                 style={"background-color":"white"}),
               ]), style={"background-color":"white",
                         "box-shadow": "10px 20px 30px black",
                         
                        'width': '210px'
                         }, disabled=True)),
               dbc.Col(dbc.Button(([html.H5("2019", style={"font-size": 18,"color": "black","background-color": "white"}),
                                    html.H1([str(f"{conf_2019:,d}")],style={"font-size": 40, "color": "black","background-color": "white"}),
                                    dbc.CardImg(src="https://github.com/fdealbam/Lesiones/blob/main/application/static/Mapa%20lesiones%20Total2019.png?raw=true",
                                                 style={"background-color":"white"}),
               ]), style={"background-color":"white",
                         "box-shadow": "10px 20px 30px black",
                         
                        'width': '210px'
                         }, disabled=True)),
               dbc.Col(dbc.Button(([html.H5("2020", style={"font-size": 18,"color": "black","background-color": "white"}),
                                    html.H1([str(f"{conf_2020:,d}")],style={"font-size": 40, "color": "black","background-color": "white"}),
                                    dbc.CardImg(src="https://github.com/fdealbam/Lesiones/blob/main/application/static/Mapa%20lesiones%20Total2020.png?raw=true",
                                                 style={"background-color":"white"}),
               ]), style={"background-color":"white",
                         "box-shadow": "10px 20px 30px black",
                         
                        'width': '210px'
                         }, disabled=True)),
               dbc.Col(dbc.Button(([html.H5("2021", style={"font-size": 18,"color": "black","background-color": "white"}),
                                    html.H1([str(f"{conf_2021:,d}")],style={"font-size": 40, "color": "black","background-color": "white"}),
                                    dbc.CardImg(src="https://github.com/fdealbam/Lesiones/blob/main/application/static/Mapa%20lesiones%20Total2021.png?raw=true",
                                                 style={"background-color":"white"}),
               ]), style={"background-color":"white",
                         "box-shadow": "10px 20px 30px black",
                         
                        'width': '210px'
                         }, disabled=True)),
                                                        ]),
    

 
       html.Br(),
       html.Br(),
       dbc.Row([
               dbc.Col(html.P("Fuente: SENSNSP"),
                        style={#"margin-left": "90px", 
                               "font-size": 22, "text-align": "right", "margin-right":"50px"}),
           ], justify= "right"),
       html.Br(),
       html.Br(),
       html.Br(),
       html.Br(),
#---------Grafica mensual
     dbc.Row(
           [
               dbc.Col(html.H1(["Casos ", 
                       dbc.Badge("mensuales", color="info", className="mr-1")]), 
                                       width={'size': 11,  "offset":1 })]),
       dbc.Row([        
               dbc.Col(html.H5("(hasta junio 2021)"),
                                       width={ 'size': 3, "offset":1 }),

            ]),
   
    dbc.Row(
        [
            dbc.Col(dcc.Graph(figure=graf_meses, config= "autosize")),
        ]),

      
          html.Br(),
       html.Br(),
       dbc.Row([
               dbc.Col(html.P("Fuente: SENSNSP"),
                        style={#"margin-left": "90px", 
                               "font-size": 22, "text-align": "right", "margin-right":"50px"}),
           ], justify= "right"),
       html.Br(),
       html.Br(),
       html.Br(),
       html.Br(),
    #títulos
     dbc.Row(
           [
               dbc.Col(html.H1([dbc.Badge("Municipios", color="info", className="ml-1"), 
                               " en entidades con más casos acumulados ",]),
                       
                        width={'size': 10,  "offset":1 }),
            ]),

       html.Br(),
       html.Br(),
       html.Br(),
    
     dbc.Row(
           [
               dbc.Col(dbc.Button(([html.P("México", style={"font-size": 30,"color": "black","background-color": "white"}),
                       dbc.CardImg(src="https://github.com/fdealbam/Lesiones/blob/main/application/static/mx.jpeg?raw=true",
                  style={'size': 2,}),
                          html.P(
                          "Los diez municipios con más lesiones fueron: Ecatepec de Morelos (39,422),"
                            "Toluca (28,680), Nezahualcóyotl (21,792), Naucalpan de Juárez (21,297), "
                            "Tlalnepantla de Baz (17,222), Chimalhuacán (12,112), Cuautitlán Izcalli (11,950),"
                            "Atizapán de Zaragoza (11,869), Chalco (11,294), y Ixtapaluca (10,709).",
                     style={'font-size': 14, "font-family":"Arial", "text-align":"justify" }),
               ]), style={"background-color":"white",
                         "box-shadow": "10px 20px 30px black",
                         'margin-left': '300px',
                        'width': '550px',
                         
                         }, disabled=True)),
               
               dbc.Col(dbc.Button(([html.P("Guanajuato", style={"font-size": 30,"color": "black","background-color": "white"}),
                       dbc.CardImg(src="https://github.com/fdealbam/Lesiones/blob/main/application/static/guanajuato.jpeg?raw=true",
                                    style={'size': 2,}),
                       html.P(
                           "Los diez municipios con más lesiones fueron: León (18,283), Irapuato (9,255), Celaya (8,065), Salamanca (4,739), Guanajuato (4,647), San Miguel de Allende (3,831), Dolores Hidalgo Cuna de la Independencia Nacional (2,201), San Francisco del Rincón (1,883), Valle de Santiago (1,724), y Pénjamo (1,466).",
                              style={'font-size': 14, "font-family":"Arial", "text-align":"justify" }),
                       ]), style={"background-color":"white",
                         "box-shadow": "10px 20px 30px black",
                        # 'margin-left': '10px',
                        'width': '550px',
                                  
                         }, disabled=True)),
     ]),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    
                dbc.Row([
          dbc.Col(dbc.Button(([html.P("Jalisco", style={"font-size": 30,"color": "black","background-color": "white"}),
                       dbc.CardImg(src="https://github.com/fdealbam/Lesiones/blob/main/application/static/jal.jpeg?raw=true"),
    
                       html.P(
                           "Los diez municipios con más lesiones fueron: Guadalajara (17,813), Zapopan (11,560), Tlajomulco de Zúñiga (6,009), Tonalá (5,213), Puerto Vallarta (3,286), El Salto (2,012), Lagos de Moreno (1,894), Tepatitlán de Morelos (1,541), Ocotlán (1,201), y Zapotlán el Grande (1,160).",
                           style={'font-size': 14, "font-family":"Arial", "text-align":"justify" }),
               ]), style={"background-color":"white",
                         "box-shadow": "10px 20px 30px black",
                         'margin-left': '300px',
                        'width': '550px',
                         
                         }, disabled=True)),
                       
               dbc.Col(dbc.Button(([html.P("Baja California", style={"font-size": 30,"color": "black","background-color": "white"}),
                       dbc.CardImg(src="https://github.com/fdealbam/Lesiones/blob/main/application/static/bc.jpeg?raw=true"),
                     html.Br(),
                                     html.Br(),
                                     html.Br(),
                                   
                        html.P(
                          "Los cinco municipios con más lesiones fueron: Tijuana (32,735), Mexicali (23,315), Ensenada (7,392), Playas de Rosarito (1,977), Tecate (1,975)",
                           style={'font-size': 14, "font-family":"Arial", "text-align":"justify" }),
               ]), style={"background-color":"white",
                         "box-shadow": "10px 20px 30px black",
                        # 'margin-left': '10px',
                        'width': '550px',
                        
                         }, disabled=True)),
                     html.Br(),
          ]),
  

    #################################################################  MUNICIPIOS ranking    


  
         html.Br(),
       html.Br(),
       dbc.Row([
               dbc.Col(html.P("Fuente: SENSNSP"),
                        style={#"margin-left": "90px", 
                               "font-size": 22, "text-align": "right", "margin-right":"400px"}),
           ], justify= "right"),
       html.Br(),
       html.Br(),
       html.Br(),
       html.Br(),
   
       
#---------Grafica por entidad
     dbc.Row(
           [
               dbc.Col(html.H1([dbc.Badge("Comparativo", color="info", className="mr-1"),
                               " entre casos acumulados & tasas "]),
                       width={'size': 10,  "offset":1 }),
            ]),

       html.Br(),
    html.Br(),
       html.Br(),
    
    dbc.Row(
           [
               dbc.Col(html.H4("Total acumulado por entidad"),
                        width=2,lg={'size': 4,  "offset": 1, }),

               dbc.Col(html.H4("Tasa por entidad"),
                       width=1, lg={'size': 3,  "offset": 4, }),                     #size=12
               
            ], justify="end",),
   
    dbc.Row(
        [
            dbc.Col(dcc.Graph(figure=graf_totfem , config= "autosize")),
                   #lg={'size': 5,  "offset": 0,}),
            
            dbc.Col(dcc.Graph(figure= graf_tasafem, config= "autosize")),
                   #lg={'size': 5,  "offset": 1,}),
        ], justify="end", no_gutters=True,),

             html.Br(),
       html.Br(),
       dbc.Row([
               dbc.Col(html.P("Fuente: SENSNSP"),
                        style={#"margin-left": "90px", 
                               "font-size": 22, "text-align": "right", "margin-right":"50px"}),
           ], justify= "right"),
       html.Br(),
       html.Br(),
       html.Br(),
       html.Br(),
    

# nuevo
    
    #dbc.Jumbotron(
    #[
        dbc.Row([

                html.Br(),
                html.H4("Metodología "),
                html.P(
                    "El presente dashboard es un ejercicio institucional con el objeto de "
                    "informar a las diputadas y diputados y público interesado sobre un tema "
                    "de vital importancia en la vida política. "
                    "La metodología que hemos empleado para analizar los datos la detallamos enseguida. "
                    "Como se indica en cada caso, la información sobre el delito aborto "
                    "fue obtenida del Secretariado Ejecutivo Nacional del Sistema Nacional de Seguridad Pública (SENSNSP) (2015-2021); "
                    " "
                    "Este dashboard seguramente será completado progresivamente con otras fuentes de información "
                    "tanto gubernamental, como aquella proveniente de organizaciones civiles que " 
                    "dan seguimiento al tema. "
                    "En ningún caso, este contenido representa algún "
                    "posicionamiento partidista, personal o institucional, mucho menos opinión o postura alguna "
                    "sobre el fenómeno." 
                    "En los aspectos técnicos, esta información fue tratada con el lenguaje de programación Python "
                    "y varias de las librerías más comunes (Dash, Choropleth, Pandas, Numpy, Geopandas, etc.), "
                    "que nos ayudan a automatizar la recurrencia (request) a la fuente de información en tiempo real "
                    "y las operaciones necesarias para crear graficas y mapas interactivos. "
                    "El volumen de información manejado fue de 230 megabytes en de la base de datos del SENSNSP. "
                    " ",
                    style= {"font-size":22,})], 
           
        style= {"margin-left":"100px", "margin-right":"100px", "text-align":"justify"},
       ),

                html.Br(),
    
        
    
    
    
   html.Br(),
   html.Br(),
   html.Br(),
   html.Br(),
   html.Br(),
    
   dbc.Row([
                                    #https://github.com/fdealbam/CamaraDiputados/blob/b11ef31e8e0f73e1a4a06ce60402563e1bd0122e/application/static/logocamara.jfif
           dbc.Col(dbc.CardImg(src="https://github.com/fdealbam/0entrada/blob/ce2cda9ccf7732861b8494b36562ebe9c8c642a6/application/static/logo%20cesopycamara.jpeg?raw=true"),
                        width=5, md={'size': 2,  "offset": 2, }),
            
           dbc.Col(html.H5(" Centro de Estudios Sociales y de Opinión Pública," 
                           " Cámara de Diputados"
                           " México, 2021 "),
                  width={'size': 3, 'offset': 0}),
               ], justify="start",),
            
   
   
    html.Br(),

    
    
    dbc.Row([    
           dbc.Col(html.P([dbc.Badge("Equipo responsable", style={"font-size":20},
                          href="https://innovation-learning.herokuapp.com/",
                                     )]),
                  width={'size': 3,  "offset": 4}),
                       ], justify="start",),
        
            ])


app.layout = html.Div([body],
                              style={'width': '1850px',
                                    "background-color": "lightgray"}
                                    )

from application.dash import app
from settings import config

if __name__ == "__main__":
    app.run_server()

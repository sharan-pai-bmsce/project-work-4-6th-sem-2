# If you prefer to run the code online instead of on your computer click:
# https://github.com/Coding-with-Adam/Dash-by-Plotly#execute-code-in-browser

from dash import Dash, dcc, Output, Input, dash_table  # pip install dash
import dash_bootstrap_components as dbc
# from dash_extensions import Output, DashProxy, Input, MultiplexerTransform
import plotly.express as px
import pandas as pd 
import json

def name_list():
    li=['India']
    df=pd.read_csv('./crime-data/india.csv')
    li=li+list(df['STATE/UT'])
    # print(li)
    return li

fig=px.choropleth_mapbox
                       # pip install pandas
city_list={
    'India': [
        './india-state-1.geojson',
        './crime-data/india.csv',
    ]
}
file=None
crime=[]
allPoints=[]
figure=[]
df=None
columns=[]
gcity=None
gage=None
columns2=[]
centroids=None
# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=name_list(),
                        value='India',  # initial value displayed when page first loads
                        clearable=False)
age = dcc.Input(placeholder='Enter Age',
                type='number',value=None)
subheading1=dcc.Markdown(children="Preinct-wise crime table")
table = dash_table.DataTable(data=None,columns=columns)
subheading2=dcc.Markdown(children="Points Table")
pointstable = dash_table.DataTable(data=None,columns=columns2)

# Customize your own Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([dropdown], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=12)
    ]),
    dbc.Row([
        dbc.Col([age], width=3)
    ], justify='center'),
    dbc.Row([
        dbc.Col([subheading1],width=10)
    ],justify='left'),
    dbc.Row([
        dbc.Col([table],width=10)
    ],justify='center'),
    dbc.Row([
        dbc.Col([subheading2],width=8)
    ],justify='left'),
    dbc.Row([
        dbc.Col([pointstable],width=10)
    ],justify='center')
], fluid=True)

def helper1(file):
    global centroids
    if file != None:
        return file
    fileArr=[
        './Crime data-age-related/Accident.csv',
        './Crime data-age-related/Arson.csv',
        './Crime data-age-related/Fraud.csv',
        './Crime data-age-related/Gun Violence.csv',
        './Crime data-age-related/Harrassment.csv',
        './Crime data-age-related/Human Trafficking.csv',
        './Crime data-age-related/Missing.csv',
        './Crime data-age-related/Murder.csv',
        './Crime data-age-related/Others.csv',
        './Crime data-age-related/Public Nuisance.csv',
        './Crime data-age-related/Robbery.csv',
        './Crime data-age-related/Sex Crime.csv',
        './Crime data-age-related/Theft.csv'
    ]
    file=[]
    centroids=json.load(open('./centroids.json'))
    for path in fileArr:
        file.append(pd.read_csv(path))
    return file

# Callback allows components to interact
def driver(city,age):
    
    global file
    if file is None:
        file=helper1(file)
    if city=='India':
        crime_data = pd.read_csv(city_list[city][1])
    else:
        crime_data = pd.read_csv('./crime-data/'+city+'.csv')
    # crime_data = crime_data.iloc[:, 1:]
    crimes = crime_data.columns
    li = []

    for df in file:
        df=pd.DataFrame(df)
        for _, row in df.iterrows():
            key = row.keys()[0]
            if key in crimes:
                if age >= row['Low'] and age <= row['Up']:
                    # if key == 'Robbery':
                    #     li.append({'Theft': row['Points']})
                    #     crime_data['Theft'] = crime_data['Theft']*row['Points']
                    li.append({key: row['Points']})
                    crime_data[key] = crime_data[key]*row['Points']
                    # print(crime_data.head(1))
                    break
            else:
                break
    # if 'Others' in crimes:
    #     crime_data['Others'] = crime_data['Others']*2.5
    #     li.append({'Others': 2.5})
    # if 'Public Nuisance' in crimes:
    #     crime_data['Public Nuisance'] = crime_data['Public Nuisance']*2.5
    #     li.append({'Public Nuisance': 2.5})
    # print(li)
    li1 = []
    crime_data = crime_data.fillna(0)
    for index, row in crime_data.iterrows():
        if row[0]!='TOTAL':
            li1.append(sum([float(x) for x in row[2:].values]))
        else:
            li1.append(0)
    crime_data['total'] = li1
    return crime_data,li

@app.callback(
    Output(mygraph, 'figure'),
    Output(mytitle, 'children'),
    Output(table,'data'),
    Output(table,'columns'),
    Output(pointstable,'data'),
    Output(pointstable,'columns'),
    Input(dropdown, 'value'),
    Input(age, 'value'),
    Input(mygraph,'clickData')
)

def update_graph(city, age,clickData):
    global df
    global crime
    global figure
    global columns
    global gcity
    global gage
    global allPoints
    global columns2
    if gage==age and gcity==city and clickData!=None:
        val=None
        if city=='India':
            val='STATE/UT'
        else:
            val='DISTRICT'
        # print(clickData['points'][0]['location'])
        for index,row in crime.iterrows():
            if row[val]==clickData['points'][0]['location']:
                data=pd.DataFrame(row).transpose()
                df=pd.DataFrame(row).transpose()
                break
        # print(pd.DataFrame(allPoints).to_dict('records'))
        columns2=[]
        res2={}
        for point in allPoints:
            for (key,value) in point.items():
                df[key]/=value
                res2[key]=value
                columns2.append({"name":key,"id":key})
        df=df.to_dict('records')
        columns=[{"name": i,"id":i} for i in data.columns]
        allPoints=[res2]
    else:
        df=None
        columns=[]
      # function arguments come from the component property of the Input
        if age==None:
            age=18
        crime_data,points=driver(city,age)
        # print(city)
        # print(type(city))
        # data=json.load(open(city_list[city][2]))
        crime=crime_data
        allPoints=points
        # lat=data['latitude']
        # long=data['longitude']
        precincts=None
        # https://plotly.com/python/choropleth-maps/
        val1=None
        val2=None
        zoom=None
        coord=None
        if city=='India':
            precincts=json.load(open(city_list[city][0],'r'))
            val1='STATE/UT'
            val2='properties.state_name'
            zoom=3
            coord=centroids[city]
        else:
            precincts=json.load(open('./india-state-district.geojson','r'))[city]
            val1='DISTRICT'
            val2='properties.district'
            coord=centroids[city]
            zoom=5
        fig=px.choropleth_mapbox(crime_data,locations=val1,featureidkey=val2,geojson=precincts,color='total',color_continuous_scale='ylorrd')
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(mapbox_style="carto-positron", 
                        mapbox_zoom=zoom,
                        mapbox_center={"lat": coord[1], "lon": coord[0]},
                        margin={"r":0,"t":0,"l":0,"b":0},
                        uirevision='constant',transition_duration=600,transition_easing='linear')
        figure=fig
        gcity=city
        gage=age
        columns2=[]
            # returned objects are assigned to the component property of the Output
    return figure,'# '+city,df,columns,allPoints,columns2

# Run app
if __name__ == '__main__':
    app.run_server(debug=True, port=8054)

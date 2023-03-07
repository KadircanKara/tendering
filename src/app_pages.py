import html
import dash_bootstrap_components as dbc
from dash.dash_table import FormatTemplate
from dash import html, dcc, dash_table
from objects import *
from functions import *

df_fiyat, df_packages, wb = load_all_sources()
df_fiyat_copy, df_packages_copy = df_fiyat.copy(), df_packages.copy()

column_type = ['text','numeric']
column_format = [None , FormatTemplate.percentage(2)]

fiyat_table_columns = [{'id':i, 'name':i, 'color':'red', 'type':column_type[int(i=='Iskontosuz Fiyat' or i=='Iskonto')], 'editable':(i=='Iskontosuz Fiyat' or i=='Iskonto')} for i in df_fiyat.columns]
package_table_columns = [{'id':i, 'name':i, 'editable':(i in packages)} for i in df_packages['Retail'].columns]

login_page = html.Div(id='main', children=[
        # html.Br(),
        # dbc.Row([
        #     dbc.Col(html.Img(src='/assets/faradai_logo_nobg.png', height="60px"), width={'size':1,'offset':4}),
        #     dbc.Col(html.H3('Faradai Tekliflendirme Modulü'), align='center', style={'color':'white'})
        #     ], align='center', justify='center'
        # ),

        html.Div(
            html.Img(src="/assets/faradai_brand.png" , style={'margin':'auto','width':'30rem'}),
            style={"margin": "auto", 'width': '28.125rem', 'height': '2.813rem', 'padding': '0.625rem',
                    'margin-top': '1rem', 'font-size': '1rem', 'border-width': '0.188rem'}
                    ),
        html.Br(),
        html.Div(
            html.H3('Tekliflendirme Modulü', style={'color':'white', 'outline-color':'white', 'margin':'auto'}), style={'text-align':'center','margin-top':'6rem'}
                    ),
        html.Div(dbc.FormFloating([
                        dbc.Input(type="username", placeholder="username", id='user'),
                        dbc.Label("Username")
                            ],
                        #    style={"margin": "auto", 'width': '28.125rem', 'height': '2.813rem', 'padding': '0.625rem',
                        #           'margin-top': '4.375rem', 'font-size': '1rem', 'border-width': '0.188rem'}
                           style={"margin": "auto", 'width': '20rem', 'height': '2.813rem', 'padding': '0.625rem',
                                  'margin-top': '4.375rem', 'font-size': '1rem', 'border-width': '0.188rem'})),
        html.Br(),
        html.Div(dbc.FormFloating([
                        dbc.Input(type="password", placeholder="password", id='passw'),
                        dbc.Label("Password")
                            ],
                           style={"margin": "auto", 'width': '20rem', 'height': '2.813rem', 'padding': '0.625rem',
                                  'margin-top': '0rem', 'font-size': '1rem', 'border-width': '0.188rem'})),
        html.Br(),                                  
        html.Div(submit_button,
                 style={'margin-left': '45%', 'padding-top': '1.88rem'}),
        
    ], style={"background-image": 'url(/assets/faradai_login_2.jpg)', 'background-repeat': 'no-repeat', 'background-size': '100%',
              'position':'fixed', 'width':'100%', 'verticalAlign':'middle',
              'background-position': 'center', "height": "100%"})

def offer_page() :

    layout = html.Div([

            html.Hr(),

            dbc.Container([

                dbc.Row([

                    dbc.Col([
                        dbc.Alert([
                            html.Div([html.H5("Dolar Kuru", style={'color':'#44d9e8','font-weight':'bold'}) , html.Label(f"{tcmb_data()}₺")],
                            )
                        ] , color='dark' )
                    ] , style={'color':'white','font-weight':'bold','width':'33.3%','text-align':'center'}, width=1 ),


                    dbc.Col([
                        dbc.Alert([
                            html.Div([html.H5("Euro Kuru", style={'color':'#44d9e8','font-weight':'bold'}) , html.Label(f"{tcmb_data('EUR')}₺")],
                            )
                        ] , color='dark' )
                    ] , style={'color':'white','font-weight':'bold','width':'33.3%','text-align':'center'}, width=1 ),


                    dbc.Col([
                        dbc.Alert([
                            html.Div([html.H5("Sterlin Kuru", style={'color':'#44d9e8','font-weight':'bold'}) , html.Label(f"{tcmb_data('GBP')}₺")],
                            )
                        ] , color='dark' )
                    ] , style={'color':'white','font-weight':'bold','width':'33.3%','text-align':'center'}, width=1 ),

                ], style={'margin-top':'20px'}),


                dbc.Row(children=[

                    dbc.Col(

                        dbc.InputGroup(
                            [dbc.InputGroupText("Proje Adı" , style=input_style),
                                dbc.Input(id='proje_adi', placeholder="", invalid=True, disabled=False)],
                            className="mb-3",
                        ), width=4,  style={'width':'33.3%'}),

                    dbc.Col(

                        dbc.InputGroup(
                            [dbc.InputGroupText("Müşteri Adı" , style={'background-color':'transparent','color':'white'}),
                                dbc.Input(id='musteri_adi', placeholder="", invalid=True, disabled=False, style={'margin-left':'0px'})],
                            className="mb-3", size=2
                        ), width=4, style={'width':'33.3%'}),

                    dbc.Col(

                        dbc.InputGroup(
                            [dbc.InputGroupText("Teklifi Hazırlayan" , style=input_style),
                                dbc.Input(id='teklifi_hazirlayan', placeholder="", invalid=True, disabled=False)],
                            className="mb-3"#, size=3
                        ), width=3, style={'width':'33.3%'}),

                ], style={'margin-top':'20px'}),

                dbc.Row([

                    dbc.Col(

                        dbc.InputGroup(
                            [dbc.InputGroupText("Kategori" , style={'background-color':'transparent','color':'white','width':'24.5%','margin-left':'0px'}),
                                dbc.Select(id='kategori', placeholder="", invalid=False, disabled=False,
                                        options=[
                                            {'label': 'Retail', 'value': 'Retail'},
                                            {'label': 'Banking', 'value': 'Banking'},
                                            {'label': 'Hospital', 'value': 'Hospital'},
                                            {'label': 'Supermarkets', 'value': 'Supermarkets'},
                                            {'label': 'Industry', 'value': 'Industry'},
                                            {'label': '-', 'value': '-'}
                                        ], style={}
                                        )],
                            className="mb-3"
                        ), style={'width':'33.3%'}, width=4),

                    dbc.Col(

                        dbc.InputGroup(
                            [dbc.InputGroupText("Paket" , style={'background-color':'transparent','width':'107.5px'}),
                                dbc.Select(id='paket', placeholder="", invalid=False, disabled=False,
                                        options=[
                                            {'label': 'Access', 'value': 'Access'},
                                            {'label': 'Starter', 'value': 'Starter'},
                                            {'label': 'Standard', 'value': 'Standard'},
                                            {'label': 'Full-stack', 'value': 'Full-stack'},
                                            {'label': '-', 'value': '-'}
                                        ], style={'width':'5%'}
                                        )],
                            className="mb-3"
                        ), style={'width':'33.3%'}, width=4),


                ], style={'margin-top':'0px'}),

                dbc.Row([
         
                    dbc.Col(

                        dbc.InputGroup(
                            [dbc.InputGroupText("Şehir İçi" , style={'background-color':'transparent','width':'86px','margin-left':'2.5px'}),
                                dbc.Input(id='sehir_ici', placeholder="", invalid=True, disabled=False, type='number',style={'width':'120px','margin-left':'0px'},
                                        step=1, min=0)],
                            className="mb-3",
                        ), width=6, style={'width':'240px'}
                    ),

                    dbc.Col(

                        dbc.InputGroup(
                            [dbc.InputGroupText("Şehir Dışı" , style={'background-color':'transparent','width':'107.5px'}),
                                dbc.Input(id='sehir_disi', placeholder="", invalid=True, disabled=False, type='number',style={'width':'120px','margin-left':'0px'},
                                        step=1, min=0)],
                            className="mb-3",
                        ), width=6, style={'width':'260px','margin-left':'145px'}
                    )

            ]),


                dbc.Row(children=[

                        dbc.Col(
                            dbc.Alert(id='display-selected-package', children='Lütfen kategori-paket seçimi yapınız.', color="primary"),
                            style={'color':'white'}

                        ),

                    ], style={'margin-top':'20px'}),

                    dbc.Row(style={'margin-top':'5px'}),

                    cihaz_row('Gateway'),
                    cihaz_row('Trifaz Analizör'),
                    cihaz_row('Akım Trafosu'),
                    cihaz_row('Sıcaklık Sensörü'),
                    cihaz_row('Su Sayacı'),
                    cihaz_row('Akıllı Klima Kontrol'),

                    cihaz_row('Modbus Converter'),
                    cihaz_row('Güç Kaynağı'),
                    cihaz_row('Jeneratör Kartı'),
                    cihaz_row('Monofaz Analizör'),
                    cihaz_row('Pulse Okuyucu'),
                    cihaz_row('UPS'),

                    dbc.Row(children=[

                            dbc.Col(myButton, width=2, align='center'), 

                            dbc.Col([
                            dbc.Spinner(id="loading-text",
                                        # style={'margin-left': '15px', 'width': '10px', 'height':'5px'},
                                        children=dbc.Alert(id="Output-Status", dismissable=True, is_open=False,
                                                           duration=2000,
                                                           style={'margin-top': '10px', 'margin-left': '5px', 'align':'center', 'vertical-align':'center'}))
                        ],width={'offset':1}, align='top', style={'text-align':'center'}),


                        dbc.Col([
                            dcc.Download(id="download-file-xlsx")
                        ]),
                        
                    ], align='center', justify='center'

                    ),

                    html.Br(),

            ], style={'margin-top':'0px','padding': '5px','backgroundColor':'##1a0933','background-size': '100%','width':'100%'})          


                ], style={'background-image': 'linear-gradient(#17082e 0%, #1a0933 7%, #1a0933 80%, #0c1f4c 100%)','background-size': '100%','width':'100%'})

    return layout

def resources_page():

     df_fiyat, df_packages, wb = load_all_sources()
     print(list(df_fiyat.columns))
     if 'Net Fiyat' in list(df_fiyat.columns):
          df_fiyat.drop(columns=['Net Fiyat'], inplace=True)
     column_type = ['text','numeric']
     column_format = [None , FormatTemplate.percentage(2)]
     fiyat_table_columns = [{'id':i, 'name':i, 'type':column_type[int(i=='Iskontosuz Fiyat' or i=='Iskonto')], 'editable':(i=='Iskontosuz Fiyat' or i=='Iskonto'), 'format':column_format[int(i=='Iskonto')]} for i in df_fiyat.columns]
     package_table_columns = [{'id':i, 'name':i, 'type':column_type[int(i in packages)], 'editable':(i in packages)} for i in df_packages['Retail'].columns]
    
     return ( html.Div([
          
        html.Hr(),

        dbc.Container([

            dbc.Row([

                dbc.Col([
                    dbc.Alert([
                        html.Div([html.H5("Dolar Kuru", style={'color':'#44d9e8','font-weight':'bold'}) , html.Label(f"{tcmb_data()}₺")],
                        )
                    ] , color='dark' )
                ] , style={'color':'white','font-weight':'bold','width':'33.3%','text-align':'center'}, width=1 ),


                dbc.Col([
                    dbc.Alert([
                        html.Div([html.H5("Euro Kuru", style={'color':'#44d9e8','font-weight':'bold'}) , html.Label(f"{tcmb_data('EUR')}₺")],
                        )
                    ] , color='dark' )
                ] , style={'color':'white','font-weight':'bold','width':'33.3%','text-align':'center'}, width=1 ),


                dbc.Col([
                    dbc.Alert([
                        html.Div([html.H5("Sterlin Kuru",style={'color':'#44d9e8','font-weight':'bold'}) , html.Label(f"{tcmb_data('GBP')}₺")],
                        )
                    ] , color='dark' )
                ] , style={'color':'white','font-weight':'bold','width':'33.3%','text-align':'center'}, width=1 ),

            ], style={'margin-top':'40px'}, justify='center'),

            dbc.Row([

                dbc.Col( [dbc.Button(html.Img(src="/assets/download.svg"), download='FiyatListesi.xlsx', href='/static/FiyatListesi.xlsx', external_link=True, color='transparent', size='lg', outline=False, style={'color':'#ea39b8'}), dbc.Button('Fiyat Dosyasını İndir', download='FiyatListesi.xlsx', href='/static/FiyatListesi.xlsx', external_link=True, color='transparent', size='lg', outline=False, style={'color':'#ea39b8'})],  width={'offset':0} ),

                dbc.Col( [dbc.Button(html.Img(src="/assets/download.svg"), download='Packages.xlsx', href='/static/Packages.xlsx', external_link=True, color='transparent', size='lg', outline=False, style={'color':'#ea39b8'}), dbc.Button('Paket Dosyasını İndir', download='Packages.xlsx', href='/static/Packages.xlsx', external_link=True, color='transparent', size='lg', outline=False, style={'color':'#ea39b8'})],  width={'offset':0} ),

            ], style={'text-align':'center'}, justify='center'),

            dbc.Row([
                dbc.Col([
                    dcc.Upload(
                        id='upload_fiyat',
                        children='Fiyat Dosyası Yükle',
                        multiple=False,
                        style=uploadStyle
                    )
                ], ),
                dbc.Col([
                    dcc.Upload(
                        id='upload_paket',
                        children='Paket Dosyası Yükle',
                        multiple=False,
                        style=uploadStyle
                    )
                ], )

            ], style={'text-align':'center','margin':'auto'}, justify='center'),

        html.Br(),

            dbc.Row([
                dbc.Col(
                    dbc.Alert( id='alert_fiyat', dismissable=True, is_open=False, duration=10000, color='secondary', children='', style={'width':'100%','margin-left':'0px'} ) , style={'text-align':'center'}
                ),
                dbc.Col(
                    dbc.Alert( id='alert_paket', dismissable=True, is_open=False, duration=10000, color='secondary', children='', style={'width':'100%'}), style={'text-align':'center','margin-left':'0px'}
                )

            ], align='center', justify='center', style={'margin':'auto', 'text-align':'center'}),


        dbc.Row(children=[

            dbc.Col( dbc.Button( id='fiyat_button', children='Fiyat Tablosu', n_clicks=0, outline=True, color='transparent', size='lg'), style={'color':'#6f42c1', 'margin-left':'15px'}, width=2),
            dbc.Col( dbc.Popover('Fiyat Tablosunu Kaydetmek için Tıklayın !', target="fiyat_button", body=True, trigger="hover", hide_arrow=True, style={'backgroundColor':'transparent', 'border': '0.2px solid', 'outline-color':'#1ba2f6'}) ),
            dbc.Col( html.Div(id='fiyat_dummy'), width=1 ),
            dbc.Col( dbc.Popover('Fiyat Tablosunu Varsayılana Çevirmek için Tıklayın !', target="fiyat_reset_button", body=True, trigger="hover", hide_arrow=True, placement='left', style={'backgroundColor':'transparent', 'border': '0.2px solid', 'outline-color':'#1ba2f6'}) ),
            dbc.Col( dbc.Button( id='fiyat_reset_button', children='Varsayılana Çevir', n_clicks=0, outline=False, color='transparent', size='lg', style={'color':'#ea39b8'} ), style={'color':'#ea39b8','text-align':'right'}, width={'offset':0} ),

        ]),

        html.Br(),

        dbc.Row(

            dbc.Col( dbc.Alert(id='fiyat_table_alert', dismissable=True, duration=5000, color='success', is_open=False, style={'width':'40%','text-align':'center'}), style={'margin-left':'15px'} ),

        ),

        html.Br(),

        dbc.Row(

            dbc.Col(

                dash_table.DataTable(id='fiyat_table', editable=False, style_data={'color':'white', 'backgroundColor':'transparent'} , 
                                                                    style_header={'backgroundColor':'rgb(30, 30, 30)' , 'color':'#44d9e8','textAlign':'center','fontWeight':'bold','outline':'1px solid #ea39b8'} , 
                                                                    style_as_list_view=False,
                                                                    style_cell={'width':'50px', 'padding':'5px','border':'1px solid white'},
                                                                    filter_action='native',
                                                                    filter_options={'case':'insensitive','placeholder_text':'filter','text-align':'center','fontColor':'white'},
                                                                    style_filter={'backgroundColor':'rgb(30, 30, 30)','color':'white','text-align':'center','border':'1px solid #ea39b8'},
                                                                    
                                                                    columns=fiyat_table_columns,
                                                                    data=df_fiyat.to_dict('records'),
                                                                    #fill_width=False
                                                                    )

            ),

            style={'margin-left':'0px'}

        ),

        html.Br(),

        dbc.Row(children=[

            dbc.Col( dbc.Button( id='paket_button', children='Paket Tablosu', n_clicks=0, outline=False, color='Info', size='lg' ), style={'color':'#6f42c1','margin-left':'15px'} ),
            dbc.Col( dbc.Popover('Paket Tablosunu Kaydetmek için Tıklayın !', target="paket_button", body=True, trigger="hover", hide_arrow=True, style={'backgroundColor':'transparent', 'border': '0.2px solid', 'outline-color':'#1ba2f6'}) ),
            dbc.Col( html.Div(id='paket_dummy'), width=1 ),
            dbc.Col( dbc.Popover('Paket Tablosunu Varsayılana Çevirmek için Tıklayın !', target="paket_reset_button", body=True, trigger="hover", hide_arrow=True, placement='left', style={'backgroundColor':'transparent', 'border': '0.2px solid', 'outline-color':'#1ba2f6'}, ) ),
            dbc.Col( dbc.Button( id='paket_reset_button', children='Varsayılana Çevir', n_clicks=0, outline=False, color='transparent', size='lg', style={'color':'#ea39b8'} ), style={'color':'#ea39b8','text-align':'right'}, width={'offset':0} ),

        ]),

        html.Br(),

        dbc.Row(
                dbc.Col( dbc.Alert(id='paket_table_alert', dismissable=True, duration=5000, color='success', is_open=False, style={'width':'auto','margin-left':'15px','text-align':'center'}), width=5 ),
        ),


        dbc.Row([
            dbc.Col(
                dbc.Tabs([
                                        dbc.Tab(label='Retail' , tab_id='Retail'),
                                        dbc.Tab(label='Banking' , tab_id='Banking'),
                                        dbc.Tab(label='Hospital' , tab_id='Hospital'),
                                        dbc.Tab(label='Supermarkets' , tab_id='Supermarkets'),
                                        dbc.Tab(label='Industry' , tab_id='Industry'),

                            ] , id='tabs' , active_tab='Retail'), style={'margin-left':'14px'}

            )
                    
        ]),

        dbc.Row(

            dbc.Col(

                dash_table.DataTable(id='paket_table', editable=False, style_data={'color':'white', 'backgroundColor':'transparent'} , 
                                                                    style_header={'backgroundColor':'rgb(30, 30, 30)' , 'color':'#44d9e8','textAlign':'center','fontWeight':'bold','border':'1px solid #ea39b8'}, 
                                                                    style_as_list_view=False,
                                                                    style_cell={'width':'50px', 'padding':'5px','border':'1px solid white'},
                                                                    
                                                                    columns=package_table_columns,
                                                                    data=df_packages['Retail'].to_dict('records'),
                                                                    fill_width=True
                                                                    ),

            style={'margin-left':'15px'})

        ),

        dbc.Row(dcc.Location(id='url' , refresh=True))

        ], style={'margin':'auto', 'background-image':'linear-gradient(#17082e 0%, #1a0933 7%, #1a0933 80%, #0c1f4c 100%)'})


    ], style={'margin':'auto','background-image':'linear-gradient(#17082e 0%, #1a0933 7%, #1a0933 80%, #0c1f4c 100%)'})
    
)

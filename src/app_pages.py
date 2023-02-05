import html
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from objects import *
from functions import *

fiyat_table_columns = [{'id':i, 'name':i, 'editable':(i=='Iskontosuz Fiyat' or i=='Iskonto')} for i in df_fiyat.columns]
package_table_columns = [{'id':i, 'name':i, 'editable':(i in packages)} for i in df_retail.columns]


navbar = html.Div([
    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(children=[
                        dbc.Col(html.Img(src='/assets/faradai_logo_nobg.png', height="60px") , align='center'),
                        dbc.Col(dbc.NavbarBrand("Faradai", className="me-auto",
                                                style={'color': 'white', 'font-family': 'Sansation', 'left-margin':'35px',
                                                    'font-size': '2rem'}), align='center'),
                        dbc.Col(
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(dbc.ModalTitle("Döviz Kurları")),
                                    dbc.ModalBody([
                                                html.Div("Dolar Kuru : {}".format(tcmb_data())),
                                                html.Div("Euro Kuru : {}".format(tcmb_data("EUR"))),
                                                html.Div("Sterlin Kuru : {}".format(tcmb_data("GBP")))
                                            ]),
                                ],
                                id="modal-sm",
                                size="sm",
                                is_open=False,
                            ),
                        )],
                        align="center",
                        className="g-0",
                    ),
                    #href="/",
                    style={"textDecoration": "none"},
                ),
                dbc.Row(
                    [
                        dbc.NavbarToggler(id="navbar-toggler"),
                        dbc.Collapse(
                            dbc.Nav(
                                [
                                    dbc.NavItem(
                                        className="me-auto",
                                    ),
                                    dbc.Button("Döviz Kurları", id="open-sm", className="me-auto", n_clicks=0 , color='success', style={'width':'15vw'}),
                                    html.A(dbc.NavItem(dbc.NavLink("Teklif")) , style={"textDecoration": "none"}, href="/Teklif"),
                                    html.A(dbc.NavItem(dbc.NavLink("Kaynaklar")) , style={"textDecoration": "none"}, href="/Kaynaklar"),
                                ],
                                className="w-100",
                            ),
                            id="navbar-collapse",
                            is_open=False,
                            navbar=True,
                        ),
                    ],
                    className="flex-grow-1",
                ),
            ],
            fluid=True,
        ),
        dark=True,
        color="secondary",
        sticky='top'
    ),
] , style={'width':'100%'}),

login_page = html.Div([
        html.Div(html.Img(src="/assets/faradai_brand.png" , style={'left-margin':'200px'}) , style={"margin": "auto", 'width': '28.125rem', 'height': '2.813rem', 'padding': '0.625rem',
                                  'margin-top': '4.375rem', 'font-size': '1rem', 'border-width': '0.188rem'}),    
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div(dbc.FormFloating([
                        dbc.Input(type="username", placeholder="username", id='user'),
                        dbc.Label("Username")
                            ],
                           style={"margin": "auto", 'width': '28.125rem', 'height': '2.813rem', 'padding': '0.625rem',
                                  'margin-top': '4.375rem', 'font-size': '1rem', 'border-width': '0.188rem'})),
        html.Br(),
        html.Div(dbc.FormFloating([
                        dbc.Input(type="password", placeholder="password", id='passw'),
                        dbc.Label("Password")
                            ],
                           style={"margin": "auto", 'width': '28.125rem', 'height': '2.813rem', 'padding': '0.625rem',
                                  'margin-top': '0.625rem', 'font-size': '1rem', 'border-width': '0.188rem'})),
        html.Br(),                                  
        html.Div(submit_button,
                 style={'margin-left': '45%', 'padding-top': '1.88rem'}),
        html.Div(dcc.Store(id='session', storage_type='session')),
        html.Div(dcc.Location(id='url' , refresh=False))
        
    ], style={"background-image": 'url(/assets/faradai_login_2.jpg)', 'background-repeat': 'no-repeat', 'background-size': '100%',
              'position':'fixed', 'width':'100%', 'verticalAlign':'middle',
              'background-position': 'center', "height": "100%"})

offer_page = html.Div([
                html.Div([
                    dbc.Navbar(
                        dbc.Container(
                            [
                                html.A(
                                    dbc.Row(children=[
                                        dbc.Col(html.Img(src='/assets/faradai_logo_nobg.png', height="60px") , align='center'),
                                        dbc.Col(dbc.NavbarBrand("Faradai", className="me-auto",
                                                                style={'color': 'white', 'font-family': 'Sansation', 'left-margin':'35px',
                                                                    'font-size': '2rem'}), align='center'),
                                        dbc.Col(
                                            dbc.Modal(
                                                [
                                                    dbc.ModalHeader(dbc.ModalTitle("Döviz Kurları")),
                                                    dbc.ModalBody([
                                                                html.Div("Dolar Kuru : {}".format(tcmb_data())),
                                                                html.Div("Euro Kuru : {}".format(tcmb_data("EUR"))),
                                                                html.Div("Sterlin Kuru : {}".format(tcmb_data("GBP")))
                                                            ]),
                                                ],
                                                id="modal-sm",
                                                size="sm",
                                                is_open=False,
                                            ),
                                        )],
                                        align="center",
                                        className="g-0",
                                    ),
                                    style={"textDecoration": "none"},
                                ),
                                dbc.Row(
                                    [
                                        dbc.NavbarToggler(id="navbar-toggler"),
                                        dbc.Collapse(
                                            dbc.Nav(
                                                [
                                                    dbc.NavItem(
                                                        className="me-auto",
                                                    ),
                                                    dbc.Button("Döviz Kurları", id="open-sm", className="me-auto", n_clicks=0 , color='success', style={'width':'15vw'}),
                                                    html.A(dbc.NavItem(dbc.NavLink("Teklif")) , style={"textDecoration": "none"}, href="/Teklif"),
                                                    html.A(dbc.NavItem(dbc.NavLink("Kaynaklar")) , style={"textDecoration": "none"}, href="/Kaynaklar"),
                                                ],
                                                className="w-100",
                                            ),
                                            id="navbar-collapse",
                                            is_open=False,
                                            navbar=True,
                                        ),
                                    ],
                                    className="flex-grow-1",
                                ),
                            ],
                            fluid=True,
                        ),
                        dark=True,
                        color="secondary",
                        sticky='top'
                    ),
                ] , style={'width':'100%'}),

                html.Br(),

                dbc.Row([
                    dbc.Col([
                        dbc.Alert([
                            html.Div(["Dolar Kuru : {} | Euro Kuru : {} | Sterlin Kuru : {}".format(tcmb_data() , tcmb_data("EUR") , tcmb_data("GBP"))],
                            )
                        ] , color='primary' , style={'display':'None'})
                    ] , style={'margin':'auto','color':'white'}, width=5)
                ]),


                html.Br(),

                dbc.Row(children=[

                    dbc.Col(

                        dbc.InputGroup(
                            [dbc.InputGroupText("Proje Adı" , style=input_style),
                                dbc.Input(id='proje_adi', placeholder="", invalid=True, disabled=False , style=input_style)],
                            className="mb-3",
                        ), width=5, style={'margin-left': '55px'}),

                    dbc.Col(

                        dbc.InputGroup(
                            [dbc.InputGroupText("Şehir İçi Şube Sayısı" , style=input_style),
                                dbc.Input(id='sehir_ici', placeholder="", invalid=True, disabled=False, type='number', style=input_style,
                                        step=1, min=0)],
                            className="mb-3",
                        ), width=3
                    ),

                    dbc.Col(

                        dbc.InputGroup(
                            [dbc.InputGroupText("Şehir Dışı Şube Sayısı" , style=input_style),
                                dbc.Input(id='sehir_disi', placeholder="", invalid=True, disabled=False, type='number', style=input_style,
                                        step=1, min=0)],
                            className="mb-3",
                        ), width=3
                    ),

                ]),

                dbc.Row(children=[
                    dbc.Col(

                        dbc.InputGroup(
                            [dbc.InputGroupText("Müşteri Adı" , style=input_style),
                                dbc.Input(id='musteri_adi', placeholder="", invalid=True, disabled=False, style=input_style)],
                            className="mb-3", size=2
                        ), style={'margin-left': '55px'}, width=5),

                    dbc.Col(

                        dbc.InputGroup(
                            [dbc.InputGroupText("Teklifi Hazırlayan" , style=input_style),
                                dbc.Input(id='teklifi_hazirlayan', placeholder="", invalid=True, disabled=False , style=input_style)],
                            className="mb-3", size=2
                        ), width=6),
                ]),

                dbc.Row(children=[

                    dbc.Col(

                        dbc.InputGroup(
                            [dbc.InputGroupText("Kategori" , style=input_style),
                                dbc.Select(id='kategori', placeholder="", invalid=False, disabled=False,
                                        options=[
                                            {'label': 'Retail', 'value': 'Retail'},
                                            {'label': 'Banking', 'value': 'Banking'},
                                            {'label': 'Hospital', 'value': 'Hospital'},
                                            {'label': 'Supermarkets', 'value': 'Supermarkets'},
                                            {'label': 'Industry', 'value': 'Industry'},
                                            {'label': '-', 'value': '-'}
                                        ],
                                        )],
                            className="mb-3", size=2
                        ), style={'margin-left': '55px'}, width=3),

                    dbc.Col(

                        dbc.InputGroup(
                            [dbc.InputGroupText("Paket" , style=input_style),
                                dbc.Select(id='paket', placeholder="", invalid=False, disabled=False,
                                        options=[
                                            {'label': 'Access', 'value': 'Access'},
                                            {'label': 'Starter', 'value': 'Starter'},
                                            {'label': 'Standard', 'value': 'Standard'},
                                            {'label': 'Full-stack', 'value': 'Full-stack'},
                                            {'label': '-', 'value': '-'}
                                        ],
                                        )],
                            className="mb-3", size=4
                        ), width={'size': 3, 'offset': 2})
                ]),

                dbc.Row(children=[

                        dbc.Col(
                            dbc.Alert(id='display-selected-package', children='Lütfen kategori-paket seçimi yapınız.', color="primary"),
                            style={'margin-left': '55px' , 'color':'white'}, width=11

                        ),

                    ]),

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
                        dbc.Col(
                            myButton, style={'margin-left': '40px', 'width': '20%'}
                        ),
                        dbc.Col(
                            dcc.Loading(id="loading-text",
                                        style={'margin-top': '50px', 'margin-left': '15px', 'width': '20%'},
                                        children=dbc.Alert(id="Output-Status", dismissable=True, is_open=True,
                                                           duration=4000,
                                                           style={'margin-top': '50px', 'margin-left': '15px',
                                                                  'width': '20%', 'display': 'none'})),
                        ),
                        dbc.Col(
                            dcc.Download(id="download-file-xlsx")
                        )
                    ]

                    ),

                    html.Br(),

                    html.Div(dcc.Store(id='session', data=[0], storage_type='session')),
                    html.Div(dcc.Location(id='url' , refresh=False))
               


                ])

resources_page = html.Div([

html.Div(children=navbar),

dbc.Row(
    dbc.Col(
        dbc.Alert(id='alert_upload', dismissable=True, is_open=False, duration=10000, color='secondary') , style={'text-align':'center'}, width={'size':3, 'offset':9}
    ) 
    ),

html.Br(),
html.Br(),

dbc.Container([

    dbc.Row([

        dbc.Col( [html.Img(src="/assets/download.svg", style={'margin-left':'15px'}), dbc.Button('Örnek Fiyat Dosyası İndir', download='FiyatListesi.xlsx', href='/static/FiyatListesi.xlsx', external_link=True, color='transparent', size='lg', outline=False, style={'color':'#ea39b8'})],  width={'offset':1} ),

        dbc.Col( [html.Img(src="/assets/download.svg", style={'margin-left':'15px'}), dbc.Button('Örnek Paket Dosyası İndir', download='Packages.xlsx', href='/static/Packages.xlsx', external_link=True, color='transparent', size='lg', outline=False, style={'color':'#ea39b8'})], width={'offset':3} ),

    ]),

    dbc.Row([
        dbc.Col([
            dcc.Upload(
                id='upload_fiyat',
                children='Fiyat Dosyası Yükleyebilirsiniz',
                multiple=False,
                style=uploadStyle
            )
        ]),
        dbc.Col([
            dcc.Upload(
                id='upload_paket',
                children='Paket Dosyası Yükleyebilirsiniz',
                multiple=False,
                style=uploadStyle
            )
        ], width={'offset':2})

    ]),

html.Br(),


dbc.Row(children=[

    dbc.Col( dbc.Button( id='fiyat_button', children='Fiyat Tablosu', n_clicks=0, outline=True, color='transparent', size='lg'), style={'color':'#6f42c1'}, width=2),
    dbc.Col( dbc.Popover('Fiyat Tablosunu Kaydetmek için Tıklayın !', target="fiyat_button", body=True, trigger="hover", hide_arrow=True, style={'backgroundColor':'transparent', 'border': '0.2px solid', 'outline-color':'#1ba2f6'}) ),
    dbc.Col( html.Div(id='fiyat_dummy'), width=1 ),
    dbc.Col( dbc.Popover('Fiyat Tablosunu Varsayılana Çevirmek için Tıklayın !', target="fiyat_reset_button", body=True, trigger="hover", hide_arrow=True, style={'backgroundColor':'transparent', 'border': '0.2px solid', 'outline-color':'#1ba2f6'}) ),
    dbc.Col( dbc.Button( id='fiyat_reset_button', children='Varsayılana Çevir', n_clicks=0, outline=False, color='transparent', size='lg', style={'color':'#ea39b8'} ), style={'color':'#ea39b8'}, width={'offset':2} ),

]),

html.Br(),

dbc.Row(

    dbc.Col( dbc.Alert(id='fiyat_table_alert', dismissable=True, duration=5000, color='success', is_open=False) ),

),

html.Br(),

dbc.Row(

    dbc.Col(

        dash_table.DataTable(id='fiyat_table', editable=False, style_data={'color':'white', 'backgroundColor':'transparent'} , 
                                                            style_header={'backgroundColor':'rgb(30, 30, 30)' , 'color':'white','textAlign':'center','font-weight':'bold'} , 
                                                            style_as_list_view=False,
                                                            style_cell={'width':'50px', 'padding':'5px'},
                                                            
                                                            columns=fiyat_table_columns,
                                                            data=df_fiyat.to_dict('records'),
                                                            fill_width=True
                                                            )

    ),

    style={'margin-left':'5px'}

),

html.Br(),

dbc.Row(children=[

    dbc.Col( dbc.Button( id='paket_button', children='Paket Tablosu', n_clicks=0, outline=False, color='Info', size='lg' ), style={'color':'#6f42c1'} ),
    dbc.Col( dbc.Popover('Paket Tablosunu Kaydetmek için Tıklayın !', target="paket_button", body=True, trigger="hover", hide_arrow=True, style={'backgroundColor':'transparent', 'border': '0.2px solid', 'outline-color':'#1ba2f6'}) ),
    dbc.Col( html.Div(id='paket_dummy'), width=1 ),
    dbc.Col( dbc.Popover('Paket Tablosunu Varsayılana Çevirmek için Tıklayın !', target="paket_reset_button", body=True, trigger="hover", hide_arrow=True, style={'backgroundColor':'transparent', 'border': '0.2px solid', 'outline-color':'#1ba2f6'}) ),
    dbc.Col( dbc.Button( id='paket_reset_button', children='Varsayılana Çevir', n_clicks=0, outline=False, color='transparent', size='lg', style={'color':'#ea39b8'} ), style={'color':'#ea39b8'}, width={'offset':2} ),

]),

html.Br(),

dbc.Row(
        dbc.Col( dbc.Alert(id='paket_table_alert', dismissable=True, duration=5000, color='success', is_open=False), width=5 ),
),


dbc.Row([
    dbc.Col(
        dbc.Tabs([
                                dbc.Tab(label='Retail' , tab_id='Retail'),
                                dbc.Tab(label='Banking' , tab_id='Banking'),
                                dbc.Tab(label='Hospital' , tab_id='Hospital'),
                                dbc.Tab(label='Supermarkets' , tab_id='Supermarkets'),
                                dbc.Tab(label='Industry' , tab_id='Industry'),

                    ] , id='tabs' , active_tab='Retail'),

    )
            
]),

dbc.Row(

    dbc.Col(

        dash_table.DataTable(id='paket_table', editable=False, style_data={'color':'white', 'backgroundColor':'transparent'} , 
                                                            style_header={'backgroundColor':'rgb(30, 30, 30)' , 'color':'white','textAlign':'center','font-weight':'bold'} , 
                                                            style_as_list_view=False,
                                                            style_cell={'width':'50px', 'padding':'5px'},
                                                            
                                                            columns=package_table_columns,
                                                            data=df_retail.to_dict('records'),
                                                            fill_width=True
                                                            ),

    style={'margin-left':'15px'})

)

])


], style={'margin':'auto'})

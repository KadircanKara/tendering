import dash
from dash_iconify import DashIconify
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from openpyxl.styles import Alignment
from dash_bootstrap_components._components.Container import Container
from functions import *
from objects import *
from app_pages import *
from git import Repo
import os

df_fiyat, df_packages, wb = load_all_sources()
df_fiyat_copy, df_packages_copy = df_fiyat.copy(), df_packages.copy()

LOCAL_PATH = os.getcwd()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR], suppress_callback_exceptions=True, meta_tags=[{'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
                )
server = app.server

app.title = 'Faradai Tendering Process'

app.layout = html.Div(id="main" , children=[

    html.Div([
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
            html.Div(dcc.Store(id='session', data=[0], storage_type='session')),
            html.Div(dcc.Location(id='url' , refresh=False))
        ], style={"background-image": 'url(/assets/faradai_login_2.jpg)', 'background-repeat': 'no-repeat', 'background-size': '100%',
                'position':'fixed', 'width':'100%', 'verticalAlign':'middle',
                'background-position': 'center', "height": "100%"}) # 56.25rem

] , style={"width": "100%", "height": "56.25rem"})

@app.callback(

    Output('paket_table','data'),
    Input('paket_reset_button','n_clicks'),
    Input('tabs','active_tab')

)

def reset_paket_table(nclicks, tab):

    if nclicks > 0 :
        return df_packages_copy[tab].to_dict('records')

    if tab :
        return load_specific_packages(tab).to_dict('records')


@app.callback(

    Output('fiyat_table','data'),
    Input('fiyat_reset_button','n_clicks')

)

def reset_fiyat_table(nclicks):

    if nclicks > 0 :
        return df_fiyat_copy.to_dict('records')
    else :
        raise PreventUpdate


@app.callback(

    Output('fiyat_table_alert','children'),
    Output('fiyat_table_alert','is_open'),
    Output('fiyat_dummy','children'),
    Input('fiyat_button','n_clicks'),
    State('fiyat_table','data'),

)

def update_fiyat(nclicks, data):

    if nclicks > 0 :

        df = pd.DataFrame.from_dict(data)
        book = xl.load_workbook('Sources/FiyatListesi.xlsx')
        ws = book.active
        column_data = [df['Iskontosuz Fiyat'], df['Iskonto']]
        current_row = 2
        current_col = 3
        for column in column_data :
            current_col += 1
            current_row = 2
            for r in range(len(column)):
                if column[r]:
                    ws.cell(row=current_row, column=current_col).value = float(column[r])
                current_row += 1
        book.save('Sources/FiyatListesi.xlsx')
        # git_push(LOCAL_PATH)


        return html.Div( "Fiyat Bilgileri Güncellendi !"), True, dash.no_update,


    else :
        raise PreventUpdate


@app.callback(

    Output('paket_table_alert','children'),
    Output('paket_table_alert','is_open'),
    Output('paket_dummy','children'),
    Input('paket_button','n_clicks'),
    State('tabs','active_tab'),
    State('paket_table','data'),

)

def update_paket(nclicks, tab, data):

    if nclicks > 0 :

        df = pd.DataFrame.from_dict(data)
        book = xl.load_workbook('Sources/Packages.xlsx')
        ws = book[tab]
        column_data = [df['Access'], df['Starter'], df['Standard'], df['Full-stack']]
        current_row = 2
        current_col = -1
        for column in column_data :
            current_col += 2
            current_row = 2
            for r in range(len(column)):
                print(column[r])
                if column[r]:
                    ws.cell(row=current_row, column=current_col).value = float(column[r])
                current_row += 1
        book.save('Sources/Packages.xlsx')
        # git_push(LOCAL_PATH)

        return html.Div(tab + " Paketi Bilgileri Güncellendi !"), True, dash.no_update,

    else :
        raise PreventUpdate


@app.callback(

    Output('alert_upload','children'),
    Output('alert_upload','is_open'),
    Output('alert_upload','color'),
    Input('upload_fiyat' , 'contents'),
    Input('upload_paket' , 'contents'),
    State('tabs','active_tab')

)


def upload_msg(fiyat_contents , paket_contents, tab):

    if fiyat_contents :
        msg , color = check_upload(fiyat_contents)
        return msg, True, color
    elif paket_contents :
        msg, color = check_upload(paket_contents)
        return msg, True, color
    else:
        raise PreventUpdate


app.callback(
    Output("modal-sm", "is_open"),
    Input("open-sm", "n_clicks"),
    State("modal-sm", "is_open"),
)(toggle_modal)

@app.callback(

    Output('main','children'),
    Input('verify','n_clicks'),
    State('user','value'),
    State('passw','value'),
    State('url','pathname')

)

def show_page(nclicks,user,passw,url):

    if url=='/Teklif' or url=='/':
        if nclicks > 0 and user=='reengen' and passw=='rngn2021!':
            
            return offer_page
        else:
            return login_page

    elif url=='/Kaynaklar':
        if nclicks > 0 and user=='reengen' and passw=='rngn2021!':
            
            return resources_page
        else:
            return login_page

@app.callback(
    Output("display-selected-package", "style"),
    Output("display-selected-package", "children"),
    Input("paket", "value"),
    Input("kategori", "value"),

    prevent_initial_call=True,
)
def func(paket, kat):

    if paket is not None and paket != '-' and kat is not None and kat != '-':

        fiyat, df = df_fiyat, df_packages[kat]

        df = df[[paket, '{} Cihaz'.format(paket)]]
        df.dropna(inplace=True)
        df.reset_index(inplace=True)

        df.dropna(inplace=True)

        df_device_and_count = df

        contents = '{} - {}  : '.format(kat, paket)

        for index, row in df.iterrows():
            contents = contents + '({}) {} '.format(str(int(row[paket])), row['{} Cihaz'.format(paket)])

        contents = contents[:-1] + ''

        return {'display': 'block'}, contents
    else:
        return None, 'Lütfen kategori-paket seçimi yapınız.'


def cihaz_options(device, type):
    if type == 'standard':
        id = device
    elif type == 'ek':
        id = 'ek_' + device

    @app.callback(
        Output(id, "options"),
        Input("paket", "value"),
        Input("kategori", "value"),

        prevent_initial_call=False,
    )
    def func(paket, kat):

            df, df_cihaz_list = get_adapters(df_fiyat, device)
            options = [{'label': i, 'value': i} for i in df_cihaz_list['cihaz'].unique()]
            return options


cihaz_options('Gateway', 'standard')
cihaz_options('Trifaz Analizör', 'standard')
cihaz_options('Akım Trafosu', 'standard')
cihaz_options('Sıcaklık Sensörü', 'standard')
cihaz_options('Su Sayacı', 'standard')
cihaz_options('Akıllı Klima Kontrol', 'standard')
cihaz_options('Modbus Converter', 'standard')
cihaz_options('Güç Kaynağı', 'standard')
cihaz_options('Jeneratör Kartı', 'standard')
cihaz_options('Monofaz Analizör', 'standard')
cihaz_options('Pulse Okuyucu', 'standard')
cihaz_options('UPS', 'standard')

cihaz_options('Gateway', 'ek')
cihaz_options('Trifaz Analizör', 'ek')
cihaz_options('Akım Trafosu', 'ek')
cihaz_options('Sıcaklık Sensörü', 'ek')
cihaz_options('Su Sayacı', 'ek')
cihaz_options('Akıllı Klima Kontrol', 'ek')
cihaz_options('Modbus Converter', 'ek')
cihaz_options('Güç Kaynağı', 'ek')
cihaz_options('Jeneratör Kartı', 'ek')
cihaz_options('Monofaz Analizör', 'ek')
cihaz_options('Pulse Okuyucu', 'ek')
cihaz_options('UPS', 'ek')


def cihaz_num_state(device):

    @app.callback(

        Output(device+'_num','disabled'),
        Output(device+'_num','value'),
        Input('kategori','value'),
        Input('paket','value')

    )

    def return_cihaz_num_state(kat, paket):

        if (paket is not None and paket != '-') and (kat is not None and kat != '-'):
            return True, None
        else:
            return False, dash.no_update

cihaz_num_state('Gateway')
cihaz_num_state('Trifaz Analizör')
cihaz_num_state('Akım Trafosu')
cihaz_num_state('Sıcaklık Sensörü')
cihaz_num_state('Su Sayacı')
cihaz_num_state('Akıllı Klima Kontrol')
cihaz_num_state('Modbus Converter')
cihaz_num_state('Güç Kaynağı')
cihaz_num_state('Jeneratör Kartı')
cihaz_num_state('Monofaz Analizör')
cihaz_num_state('Pulse Okuyucu')
cihaz_num_state('UPS')


@app.callback(
    Output("proje_adi", "valid"),
    Output("sehir_ici", "valid"),
    Output("sehir_disi", "valid"),
    Output("musteri_adi", "valid"),
    Output("teklifi_hazirlayan", "valid"),
    Output("kategori", "valid"),
    Output("paket", "valid"),

    Input("proje_adi", "value"),
    Input("sehir_ici", "value"),
    Input("sehir_disi", "value"),
    Input("musteri_adi", "value"),
    Input("teklifi_hazirlayan", "value"),
    Input("kategori", "value"),
    Input("paket", "value"),

    prevent_initial_call=True,
)
def validate1_params(proje, ic, dis, musteri, teklif, kategori, paket):
    params = [proje, ic, dis, musteri, teklif, kategori, paket]

    valid = []

    for param in params:
        if param is not None and param != '-' and param != '':
            valid.append(True)
        else:
            valid.append(False)

    return valid


@app.callback(
    Output("proje_adi", "invalid"),
    Output("sehir_ici", "invalid"),
    Output("sehir_disi", "invalid"),
    Output("musteri_adi", "invalid"),
    Output("teklifi_hazirlayan", "invalid"),

    Input("proje_adi", "value"),
    Input("sehir_ici", "value"),
    Input("sehir_disi", "value"),
    Input("musteri_adi", "value"),
    Input("teklifi_hazirlayan", "value"),

    prevent_initial_call=True,
)
def validate2_params(proje, ic, dis, musteri, teklif):
    params = [proje, ic, dis, musteri, teklif]

    invalid = []

    for param in params:
        if param is not None and param != '-' and param != '':
            invalid.append(False)
        else:
            invalid.append(True)

    return invalid


@app.callback(
    Output("submit", "disabled"),
    Output("submit", "color"),
    Input('proje_adi', 'invalid'),
    Input('musteri_adi', 'invalid'),
    Input('teklifi_hazirlayan', 'invalid'),
    Input('sehir_ici', 'invalid'),
    Input('sehir_disi', 'invalid'),
)

def enable_button(proje, musteri, teklif, ic, dis):
    params = [proje, musteri, teklif, ic, dis]

    if True in params:
        return True, 'danger'
    else:
        return False, 'secondary'


@app.callback(

    Output("Output-Status", "children"),
    Output("Output-Status", "style"),
    Output("Output-Status", "dismissable"),
    Output("Output-Status", "is_open"),
    Output("Output-Status", "duration"),
    Output('download-file-xlsx', 'data'),

    Input("submit", "n_clicks"),
    State("proje_adi", "value"),
    State("musteri_adi", "value"),
    State("teklifi_hazirlayan", "value"),
    State("sehir_ici", "value"),
    State("sehir_disi", "value"),
    State("kategori", "value"),
    State("paket", "value"),

    State("Gateway", "value"),
    State("Gateway_num", "value"),
    State("ek_Gateway", "value"),
    State("ek_Gateway_ic", "value"),
    State("ek_Gateway_dis", "value"),

    State("Trifaz Analizör", "value"),
    State("Trifaz Analizör_num", "value"),
    State("ek_Trifaz Analizör", "value"),
    State("ek_Trifaz Analizör_ic", "value"),
    State("ek_Trifaz Analizör_dis", "value"),

    State("Akım Trafosu", "value"),
    State("Akım Trafosu_num", "value"),
    State("ek_Akım Trafosu", "value"),
    State("ek_Akım Trafosu_ic", "value"),
    State("ek_Akım Trafosu_dis", "value"),

    State("Sıcaklık Sensörü", "value"),
    State("Sıcaklık Sensörü_num", "value"),
    State("ek_Sıcaklık Sensörü", "value"),
    State("ek_Sıcaklık Sensörü_ic", "value"),
    State("ek_Sıcaklık Sensörü_dis", "value"),

    State("Su Sayacı", "value"),
    State("Su Sayacı_num", "value"),
    State("ek_Su Sayacı", "value"),
    State("ek_Su Sayacı_ic", "value"),
    State("ek_Su Sayacı_dis", "value"),

    State("Akıllı Klima Kontrol", "value"),
    State("Akıllı Klima Kontrol_num", "value"),
    State("ek_Akıllı Klima Kontrol", "value"),
    State("ek_Akıllı Klima Kontrol_ic", "value"),
    State("ek_Akıllı Klima Kontrol_dis", "value"),

    State("Modbus Converter", "value"),
    State("Modbus Converter_num", "value"),
    State("ek_Modbus Converter", "value"),
    State("ek_Modbus Converter_ic", "value"),
    State("ek_Modbus Converter_dis", "value"),

    State("Güç Kaynağı", "value"),
    State("Güç Kaynağı_num", "value"),
    State("ek_Güç Kaynağı", "value"),
    State("ek_Güç Kaynağı_ic", "value"),
    State("ek_Güç Kaynağı_dis", "value"),

    State("Jeneratör Kartı", "value"),
    State("Jeneratör Kartı_num", "value"),
    State("ek_Jeneratör Kartı", "value"),
    State("ek_Jeneratör Kartı_ic", "value"),
    State("ek_Jeneratör Kartı_dis", "value"),

    State("Monofaz Analizör", "value"),
    State("Monofaz Analizör_num", "value"),
    State("ek_Monofaz Analizör", "value"),
    State("ek_Monofaz Analizör_ic", "value"),
    State("ek_Monofaz Analizör_dis", "value"),

    State("Pulse Okuyucu", "value"),
    State("Pulse Okuyucu_num", "value"),
    State("ek_Pulse Okuyucu", "value"),
    State("ek_Pulse Okuyucu_ic", "value"),
    State("ek_Pulse Okuyucu_dis", "value"),

    State("UPS", "value"),
    State("UPS_num", "value"),
    State("ek_UPS", "value"),
    State("ek_UPS_ic", "value"),
    State("ek_UPS_dis", "value"),

    prevent_initial_call=True

)
def write_to_excel(nclicks, proje, musteri, teklif, ic, dis, kategori, paket, gateway, gateway_num, ek_gateway, gateway_ic,
                   gateway_dis,
                   trifaz, trifaz_num,  ek_trifaz, trifaz_ic, trifaz_dis, akim, akim_num, ek_akim, akim_ic, akim_dis, sicaklik, sicaklik_num, ek_sicaklik,
                   sicaklik_ic, sicaklik_dis,
                   su, su_num, ek_su, su_ic, su_dis, klima, klima_num, ek_klima, klima_ic, klima_dis, modbus, modbus_num, ek_modbus, modbus_ic,
                   modbus_dis,
                   guc, guc_num, ek_guc, guc_ic, guc_dis, jenerator, jenerator_num, ek_jenerator, jenerator_ic, jenerator_dis, monofaz, monofaz_num,
                   ek_monofaz, monofaz_ic, monofaz_dis,
                   pulse, pulse_num, ek_pulse, pulse_ic, pulse_dis, ups, ups_num, ek_ups, ups_ic, ups_dis):

    
    df_fiyat, df_packages, wb = load_all_sources()

    if ic is None : ic = 0
    if dis is None : dis = 0
    wb['TeklifÇalışması']['C6'] = ic + dis

    donanimlar = [gateway, trifaz, akim, sicaklik, su, klima, modbus, guc, jenerator, monofaz, pulse, ups]
    donanimlar_adet = [gateway_num, trifaz_num, akim_num, sicaklik_num, su_num, klima_num, modbus_num, guc_num, jenerator_num, monofaz_num, pulse_num, ups_num]
    cihazlar = ['Gateway', 'Trifaz', 'Akım Trafosu', 'Sıcaklık Sensörü', 'Su Sayacı', 'Akıllı Klima Kontrol',
                'Modbus Converter',
                'Güç Kaynağı', 'Jeneratör Kartı', 'Monofaz Analizör', 'Pulse Okuyucu', 'UPS']

    ek_donanimlar = [ek_gateway, ek_trifaz, ek_akim, ek_sicaklik, ek_su, ek_klima, ek_modbus, ek_guc,
                     ek_jenerator, ek_monofaz, ek_pulse, ek_ups]


    ek_donanim_ic = [gateway_ic, trifaz_ic, akim_ic, sicaklik_ic, su_ic, klima_ic, modbus_ic, guc_ic, jenerator_ic,
                     monofaz_ic, pulse_ic, ups_ic]
    ek_donanim_dis = [gateway_dis, trifaz_dis, akim_dis, sicaklik_dis, su_dis, klima_dis, modbus_dis, guc_dis,
                      jenerator_dis, monofaz_dis, pulse_dis, ups_dis]

    ek_donanim_ic_toplam, ek_donanim_dis_toplam = 0, 0

    for i in range(len(ek_donanimlar)):
        if ek_donanimlar[i] is not None and ek_donanimlar[i] != '-':
            if ek_donanim_ic[i] is not None:
                ek_donanim_ic_toplam += ek_donanim_ic[i]
            if ek_donanim_dis[i] is not None:
                ek_donanim_dis_toplam += ek_donanim_dis[i]


# -----------------------------------------------   START EXCEL OPERATIONS  -----------------------------------------

    ws = wb['YatırımMaliyeti']

    ws['G3'] = tcmb_data()
    ws['G4'] = tcmb_data('EUR')
    ws['G5'] = tcmb_data('GBP')

    ws.cell(row=4, column=3).value = musteri
    ws.cell(row=5, column=3).value = proje
    ws.cell(row=6, column=3).value = teklif

    ws['C8'] = paket

    ws['H9'] = 'Şehir İçi : ' + str(ic)
    ws['I9'] = 'Şehir Dışı : ' + str(dis)

    for i in range(len(donanimlar)):

        print(ek_donanimlar[i],ek_donanim_ic[i])

        if donanimlar[i] is not None and donanimlar[i] != '-':

            ws['B{}'.format(i + 15)] = donanimlar[i]

            cihaz = cihazlar[i]

            if (paket is not None and paket != '-') and (kategori is not None and kategori != '-'):
                df = df_packages[kategori]
                df = df[[paket, '{} Cihaz'.format(paket)]]
                df.dropna(inplace=True)
                df.reset_index(inplace=True)
                df.dropna(inplace=True)
                df_kurulumsuz = df[df['{} Cihaz'.format(paket)].str.contains("Kurulum") == False]
                ws['E{}'.format(i + 15)] = df_kurulumsuz.loc[df_kurulumsuz['{} Cihaz'.format(paket)] == cihaz][paket].sum()
            else:
                if donanimlar_adet[i] is not None:
                    ws['E{}'.format(i + 15)] = donanimlar_adet[i]
                else:
                    ws['E{}'.format(i + 15)] = 0

            ws['G{}'.format(i + 15)] = df_fiyat.loc[df_fiyat['Adaptör'] == donanimlar[i]]['Iskontosuz Fiyat'].values[0] * (1 - df_fiyat.loc[df_fiyat['Adaptör'] == donanimlar[i]]['Iskonto'].values[0])
            ws['F{}'.format(i + 15)] = df_fiyat.loc[df_fiyat['Adaptör'] == donanimlar[i]]['Para Birimi'].values[0]

            ws['E{}'.format(i+15)].alignment = Alignment(horizontal='center')
            ws['F{}'.format(i+15)].alignment = Alignment(horizontal='center')
            ws['G{}'.format(i+15)].alignment = Alignment(horizontal='center')
            ws['H{}'.format(i+15)].alignment = Alignment(horizontal='center')

        else:
            ws['B{}'.format(i + 15)], ws['E{}'.format(i + 15)], ws['G{}'.format(i + 15)], ws[
                'F{}'.format(i + 15)] = "", "", "", ""

        if (ek_donanimlar[i] is not None and ek_donanimlar[i] != '-') and (
                ek_donanim_ic[i] is not None or ek_donanim_dis[i] is not None) and (
                int(bool(ek_donanim_ic[i])) + int(bool(ek_donanim_dis[i]))) != 0:

            ws['B{}'.format(i + 73)] = ek_donanimlar[i]
            cihaz = cihazlar[i]
            ic_dis_donanim_sayisi = 0
            ek_donanim_aciklama = ''
            if ek_donanim_ic[i]:
                ic_dis_donanim_sayisi += ek_donanim_ic[i]
                ek_donanim_aciklama += ('İç : ' + str(ek_donanim_ic[i]) + ' ')
            if ek_donanim_dis[i]:
                ic_dis_donanim_sayisi += ek_donanim_dis[i]
                ek_donanim_aciklama += ('Dış : ' + str(ek_donanim_dis[i]))
            ws['E{}'.format(i + 73)] = ic_dis_donanim_sayisi
            ws['I{}'.format(i + 73)] = ek_donanim_aciklama
            ws['G{}'.format(i + 73)] = df_fiyat.loc[df_fiyat['Adaptör'] == ek_donanimlar[i]]['Iskontosuz Fiyat'].values[0] * (1 - df_fiyat.loc[df_fiyat['Adaptör'] == ek_donanimlar[i]]['Iskonto'].values[0])
            ws['F{}'.format(i + 73)] = df_fiyat.loc[df_fiyat['Adaptör'] == ek_donanimlar[i]]['Para Birimi'].values[0]

        else:
            ws['B{}'.format(i + 73)], ws['E{}'.format(i + 73)], ws['I{}'.format(i + 73)], ws['G{}'.format(i + 73)], ws[
                'F{}'.format(i + 73)] = "", "", "", "", ""

    if ic is not None or ic != 0:
        ws['B33'] = 'Paket Kurulum (Şehir İçi)'
        ws['G33'] = df_fiyat.loc[df_fiyat['Adaptör'] == 'Paket Kurulum (Şehir içi)']['Iskontosuz Fiyat'].values[0] * (1 - df_fiyat.loc[df_fiyat['Adaptör'] == 'Paket Kurulum (Şehir içi)']['Iskonto'].values[0])
        ws['E33'] = ic
        ws['F33'] = df_fiyat.loc[df_fiyat['Adaptör'] == 'Paket Kurulum (Şehir içi)']['Para Birimi'].values[0]
        ws['B35'] = 'Cihaz Başı Kurulum (Şehir içi)'
        ws['G35'] = df_fiyat.loc[df_fiyat['Adaptör'] == 'Cihaz Başı Kurulum (Şehir içi)']['Iskontosuz Fiyat'].values[0] * (1 - df_fiyat.loc[df_fiyat['Adaptör'] == 'Cihaz Başı Kurulum (Şehir içi)']['Iskonto'].values[0])
        ws['E35'] = "={}+(SUM(E17:E26)*{})".format(ek_donanim_ic_toplam, ic)
        ws['F35'] = df_fiyat.loc[df_fiyat['Adaptör'] == 'Cihaz Başı Kurulum (Şehir içi)']['Para Birimi'].values[0]

    if dis is not None or dis != 0:
        ws['B34'] = 'Paket Kurulum (Şehir Dışı)'
        ws['G34'] = df_fiyat.loc[df_fiyat['Adaptör'] == 'Paket Kurulum (Şehir dışı)']['Iskontosuz Fiyat'].values[0] * (1 - df_fiyat.loc[df_fiyat['Adaptör'] == 'Paket Kurulum (Şehir dışı)']['Iskonto'].values[0])
        ws['E34'] = dis
        ws['F34'] = df_fiyat.loc[df_fiyat['Adaptör'] == 'Paket Kurulum (Şehir dışı)']['Para Birimi'].values[0]
        ws['B36'] = 'Cihaz Başı Kurulum (Şehir dışı)'
        ws['G36'] = df_fiyat.loc[df_fiyat['Adaptör'] == 'Cihaz Başı Kurulum (Şehir dışı)']['Iskontosuz Fiyat'].values[0] * (1 - df_fiyat.loc[df_fiyat['Adaptör'] == 'Cihaz Başı Kurulum (Şehir dışı)']['Iskonto'].values[0])
        ws['E36'] = "={}+(SUM(E17:E26)*{})".format(ek_donanim_dis_toplam, dis)
        ws['F36'] = df_fiyat.loc[df_fiyat['Adaptör'] == 'Cihaz Başı Kurulum (Şehir dışı)']['Para Birimi'].values[0]

    ws['F33'].alignment = Alignment(horizontal='center')
    ws['F34'].alignment = Alignment(horizontal='center')
    ws['F35'].alignment = Alignment(horizontal='center')

    name_of_file = musteri + " - " + proje
    wb.save('Outputs/' + name_of_file + '.xlsx')

    return name_of_file + " adlı dosyanız hazır.", {'margin-top': '50px',
                                                    'margin-left': '15px'}, True, True, 4000, dcc.send_file(
        'Outputs/' + name_of_file + '.xlsx')


@app.callback(

    Output('Gateway', 'disabled'),
    Output('Trifaz Analizör', 'disabled'),
    Output('Akım Trafosu', 'disabled'),
    Output('Sıcaklık Sensörü', 'disabled'),
    Output('Su Sayacı', 'disabled'),
    Output('Akıllı Klima Kontrol', 'disabled'),
    Output('Modbus Converter', 'disabled'),
    Output('Güç Kaynağı', 'disabled'),
    Output('Jeneratör Kartı', 'disabled'),
    Output('Monofaz Analizör', 'disabled'),
    Output('Pulse Okuyucu', 'disabled'),
    Output('UPS', 'disabled'),

    Output('Gateway', 'value'),
    Output('Trifaz Analizör', 'value'),
    Output('Akım Trafosu', 'value'),
    Output('Sıcaklık Sensörü', 'value'),
    Output('Su Sayacı', 'value'),
    Output('Akıllı Klima Kontrol', 'value'),
    Output('Modbus Converter', 'value'),
    Output('Güç Kaynağı', 'value'),
    Output('Jeneratör Kartı', 'value'),
    Output('Monofaz Analizör', 'value'),
    Output('Pulse Okuyucu', 'value'),
    Output('UPS', 'value'),

    Input("kategori", "value"),
    Input("paket", "value"),
    Input('Gateway', 'value'),
    Input('Trifaz Analizör', 'value'),
    Input('Akım Trafosu', 'value'),
    Input('Sıcaklık Sensörü', 'value'),
    Input('Su Sayacı', 'value'),
    Input('Akıllı Klima Kontrol', 'value'),
    Input('Modbus Converter', 'value'),
    Input('Güç Kaynağı', 'value'),
    Input('Jeneratör Kartı', 'value'),
    Input('Monofaz Analizör', 'value'),
    Input('Pulse Okuyucu', 'value'),
    Input('UPS', 'value'),

    prevent_initial_call=False

)
def required_devices_border(kategori, paket, gateway, trifaz, akim, sicaklik, su, klima, modbus, guc, jenerator,
                            monofaz, pulse, ups):
    all_contents = []
    filenames = []
    parsed_contents = []

    all_inputs = [gateway, trifaz, akim, sicaklik, su, klima, modbus, guc, jenerator, monofaz, pulse, ups]
    required_inputs = []

    DISABLED = [True] * len(all_inputs)
    VALUE = all_inputs

    DISABLED = [True] * len(all_inputs)
    VALUE = all_inputs

    if (kategori is not None and kategori != '-') and (paket is not None and paket != '-'):

        df = df_packages[kategori]

        df = df[[paket, '{} Cihaz'.format(paket)]]
        df.dropna(inplace=True)
        df.reset_index(drop=True)

        df.dropna(inplace=True)

        tum_cihazlar = ['Gateway', 'Trifaz', 'Akım Trafosu', 'Sıcaklık Sensörü', 'Su Sayacı', 'Akıllı Klima Kontrol',
                        'Modbus Converter',
                        'Güç Kaynağı', 'Jeneratör Kartı', 'Monofaz Analizör', 'Pulse Okuyucu', 'UPS']
        
        if kategori == '-' or paket == '-':
            gereken_cihazlar = tum_cihazlar
        else:
            gereken_cihazlar = df.loc[df['{} Cihaz'.format(paket)] != "Kurulum"]['{} Cihaz'.format(paket)].unique().tolist()

        girilen_cihazlar = [gateway, trifaz, akim, sicaklik, su, klima, modbus, guc, jenerator, monofaz, pulse, ups]

        for i in range(len(tum_cihazlar)):
            if tum_cihazlar[i] in gereken_cihazlar:
                DISABLED[i] = False
            else:
                VALUE[i] = None

        return DISABLED + VALUE


    else:

        DISABLED = [False] * len(all_inputs)
        return DISABLED + VALUE


if __name__ == "__main__":
    app.run_server(debug=True , port=8012)
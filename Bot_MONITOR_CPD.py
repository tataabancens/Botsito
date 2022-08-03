import pandas as pd
import numpy as np
from fpdf import FPDF

#INPUTS
dia_reporte = input("Insertar dia del reporte: ")
mes_reporte = input("Insertar mes del reporte: ")
numero_proxima_edicion = int(input("Insertar próxima edición: "))

#DEFINIR FECHAS
hoy = np.datetime64(f'2022-{mes_reporte}-{dia_reporte}')

una_semana_atras = hoy - np.timedelta64(7, 'D')
hace_una_semana = np.arange (una_semana_atras,hoy,dtype='datetime64[D]')

hoy_2= hoy + np.timedelta64(4, 'D')
fin_hoy_2= hoy_2 + np.timedelta64(7, 'D')
proxima_semana = np.arange (hoy_2,fin_hoy_2,dtype='datetime64[D]')


#LEER EXCEL
file_loc = "/Users/valentinvedda/Dropbox/CPD - 2020/CPD - 2022/Agenda/AGENDA TRABAJO CPD 20220725.xlsx"
ExcelAgenda = pd.read_excel(file_loc, usecols = "A, B, C, H, K", skiprows=lambda x: x in [0, 1])
ExcelAgenda["Fecha Cierre"] = pd.to_datetime (ExcelAgenda["Fecha Cierre"])

#LEER SHEET
sheet_url = "https://docs.google.com/spreadsheets/d/17Z0Gvxqx1LcXKnEDNLY-buH96Dahc44_0ZG_H4sTWCA/edit#gid=944768101"
csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
Sheet_Comunicacion = pd.read_csv(csv_export_url, skiprows=lambda x: x in [0], usecols = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
Sheet_Comunicacion["Fecha"] = pd.to_datetime(Sheet_Comunicacion["Fecha"])

#INFO COMUNICACION
fila_comunicacion = Sheet_Comunicacion.loc[Sheet_Comunicacion["Fecha"] == hoy]
info_comunicacion = fila_comunicacion.values[0]
suscriptores = info_comunicacion[1]
visitas = info_comunicacion[2]
mails_enviados= info_comunicacion[3]
mails_abiertos= info_comunicacion[4]
publicaciones = info_comunicacion[5]
likes_facebook= info_comunicacion[6]
likes_twitter = info_comunicacion[7]
likes_instagram = info_comunicacion[8]
likes_linkedin = info_comunicacion[9]
comentarios = info_comunicacion[10]

#FECHAS
filtro_cierrecontenido = ((ExcelAgenda["TAREA"] == "Cierre de recopilación de información: Trabajo III (noticias e indicadores)") & (ExcelAgenda["EDICION"] == numero_proxima_edicion))
fecha_cierre_de_contenido = ExcelAgenda.loc[filtro_cierrecontenido, "Fecha Cierre"]
fecha_cierre_de_contenido.values[0]

filtro_publicacionproximaedicion = ((ExcelAgenda["TAREA"] == "Publicación Informe (medios GEO)") & (ExcelAgenda["EDICION"] == numero_proxima_edicion))
fecha_publicacion_proxima_edicion = ExcelAgenda.loc[filtro_publicacionproximaedicion, "Fecha Cierre"]
fecha_publicacion_proxima_edicion.values[0]


#HITOS CUMPLIDOS A LA FECHA
filtro_hitoscumplidos = (ExcelAgenda["Fecha Cierre"].isin(hace_una_semana) & (ExcelAgenda["TIPO"]== "MONITOR") & (ExcelAgenda["% AVANCE"] == 100))
hitos_cumplidos_ultima_semana = ExcelAgenda.loc[filtro_hitoscumplidos, "TAREA"]
hitos_cumplidos_ultima_semana.values

#ESTADO DE CUMPLIMIENTO DE LA AGENDA
filtro_ultimomonitor = ((ExcelAgenda["TAREA"] == "Publicación Informe (medios GEO)") & (ExcelAgenda["EDICION"] == numero_proxima_edicion-1))
fecha_ultimo_monitor = ExcelAgenda.loc[filtro_ultimomonitor, "Fecha Cierre"]
contar_fecha_ultimo_monitor = fecha_ultimo_monitor.values[0] + np.timedelta64(1, 'D')

filtro_hitos_cumplidos_desde_ultimo_monitor = (ExcelAgenda["Fecha Cierre"].isin(np.arange (contar_fecha_ultimo_monitor,hoy,dtype='datetime64[D]')) & (ExcelAgenda["TIPO"]== "MONITOR") & (ExcelAgenda["% AVANCE"] == 100))
hitos_cumplidos_desde_ultimo_monitor = ExcelAgenda.loc[filtro_hitos_cumplidos_desde_ultimo_monitor, "TAREA"]

filtro_hitos_no_cumplidos_desde_ultimo_monitor = (ExcelAgenda["Fecha Cierre"].isin(np.arange (contar_fecha_ultimo_monitor,hoy,dtype='datetime64[D]')) & (ExcelAgenda["TIPO"]== "MONITOR") & (ExcelAgenda["% AVANCE"] < 100))
hitos_no_cumplidos_desde_ultimo_monitor = ExcelAgenda.loc[filtro_hitos_no_cumplidos_desde_ultimo_monitor, "TAREA"]

filtro_hitos_no_cumplidos_desde_ultimo_monitor_PROXIMO_MONITOR = (ExcelAgenda["Fecha Cierre"].isin(np.arange (contar_fecha_ultimo_monitor,hoy,dtype='datetime64[D]')) & (ExcelAgenda["TIPO"]== "MONITOR") & (ExcelAgenda["% AVANCE"] < 100) & (ExcelAgenda["EDICION"] == numero_proxima_edicion))
hitos_no_cumplidos_desde_ultimo_monitor_PROXIMO_MONITOR = ExcelAgenda.loc[filtro_hitos_no_cumplidos_desde_ultimo_monitor_PROXIMO_MONITOR, "TAREA"]

filtro_hitos_no_cumplidos_desde_ultimo_monitor_ANTERIOR_MONITOR = (ExcelAgenda["Fecha Cierre"].isin(np.arange (contar_fecha_ultimo_monitor,hoy,dtype='datetime64[D]')) & (ExcelAgenda["TIPO"]== "MONITOR") & (ExcelAgenda["% AVANCE"] < 100) & (ExcelAgenda["EDICION"] == numero_proxima_edicion-1))
hitos_no_cumplidos_desde_ultimo_monitor_ANTERIOR_MONITOR = ExcelAgenda.loc[filtro_hitos_no_cumplidos_desde_ultimo_monitor_ANTERIOR_MONITOR, "TAREA"]

filtro_hitos_desde_ultimo_monitor = (ExcelAgenda["Fecha Cierre"].isin(np.arange (contar_fecha_ultimo_monitor,hoy,dtype='datetime64[D]')) & (ExcelAgenda["TIPO"]== "MONITOR"))
hitos_desde_ultimo_monitor = ExcelAgenda.loc[filtro_hitos_desde_ultimo_monitor, "TAREA"]
len(hitos_desde_ultimo_monitor)

porcentaje_de_hitos_realizados = (len(hitos_cumplidos_desde_ultimo_monitor)/len(hitos_desde_ultimo_monitor))*100


#PROXIMOS TEMAS A TRABAJAR
filtro_ediciones_a_trabajar = (ExcelAgenda["Fecha Cierre"].isin(proxima_semana)& (ExcelAgenda["TIPO"]== "MONITOR"))
ediciones_a_trabajar = ExcelAgenda.loc[filtro_ediciones_a_trabajar, "EDICION"]
np.unique(ediciones_a_trabajar)

filtro_temas_a_trabajar = (ExcelAgenda["Fecha Cierre"].isin(proxima_semana) & (ExcelAgenda["TIPO"]== "MONITOR"))
temas_a_trabajar = ExcelAgenda.loc[filtro_temas_a_trabajar, "TAREA"]
temas_a_trabajar.values

#CREAR PDF

pdf = FPDF ("P", "mm", "A4")
pdf.add_page()
pdf.set_auto_page_break(auto=True)

pdf.image("/Users/valentinvedda/Desktop/Robotitos/GEO/GEO_logo.png", 157, 12, 40)

pdf.set_font("helvetica", "B", 18,)
pdf.cell(40,12,f" ", ln=True)
pdf.cell(40,8,f"REPORTE MONITOR GEO  -  {dia_reporte}/{mes_reporte}/2022", ln=True)
pdf.cell(40,10,f"", ln=True)

pdf.set_font("helvetica", "B", 11,)
pdf.cell(40,8,f"FECHA DE CIERRE DE CONTENIDO:", ln=True)
pdf.set_font("helvetica", "", 11,)
fecha_cierre = pd.to_datetime(str(fecha_cierre_de_contenido.values[0]))
pdf.cell(40,8,f"             {fecha_cierre.strftime('%d/%m/%Y')}", ln=True)

pdf.set_font("helvetica", "B", 11,)
pdf.cell(40,8,f"FECHA PUBLICACIÓN PRÓXIMA EDICIÓN:", ln=True)
pdf.set_font("helvetica", "", 11,)
fecha_proximo = pd.to_datetime(str(fecha_publicacion_proxima_edicion.values[0]))
pdf.cell(40,8,f"             {fecha_proximo.strftime('%d/%m/%Y')}", ln=True)

pdf.set_font("helvetica", "B", 11,)
pdf.cell(40,8,f"EDICIÓN DEL PRÓXIMO MONITOR:", ln=True)
pdf.set_font("helvetica", "", 11,)
pdf.cell(40,8,f"             {numero_proxima_edicion}", ln=True)
pdf.cell(40,6,f" ", ln=True)

pdf.set_font("helvetica", "B", 11,)
pdf.cell(40,8,f"HITOS CUMPLIDOS A LA FECHA:", ln=True)
pdf.set_font("helvetica", "", 11,)
if len(hitos_cumplidos_ultima_semana) == 0:
    pdf.cell(40,12,f"Durante la última semana no se han cumplido hitos, según agenda", ln=True)
else:
    for h0 in hitos_cumplidos_ultima_semana.values:
        pdf.cell(40,8,f"                      {h0}", ln=True)  

pdf.cell(40,5,f" ", ln=True)

pdf.set_font("helvetica", "B", 11,)
pdf.cell(40,8,f"REGISTRO DE IMPACTO (acceso a serie):", ln=True)
pdf.set_font("helvetica", "I", 11,)
pdf.cell(40,10,f"        Cantidad de suscriptores en 2022:",ln=True)
pdf.set_font("helvetica", "", 11,)
pdf.cell(40,8,f"                      {int(suscriptores)} ({round(int(suscriptores)/1000,2)}% cumplimiento del objetivo anual de 1000 suscriptores).", ln=True)
pdf.set_font("helvetica", "I", 11,)
pdf.cell(40,8,f"        Reporte de accesos a la web en 2022:",ln=True)
pdf.set_font("helvetica", "", 11,)
pdf.cell(40,10,f"                      {visitas} ({round((visitas*1000)/5000,2)}% del cumplimiento anual de 5000 visitas).", ln=True)
pdf.set_font("helvetica", "I", 11,)
pdf.cell(40,8,f"        Mails enviados y abiertos:",ln=True)
pdf.set_font("helvetica", "", 11,)
pdf.cell(40,10,f"                      {mails_enviados} enviados - {mails_abiertos} abiertos. El ratio es de {round(mails_abiertos/mails_enviados,2)}%",ln=True)
pdf.set_font("helvetica", "I", 11,)
pdf.cell(40,8,f"        Publicaciones a la fecha por red social:",ln=True)
pdf.set_font("helvetica", "", 11,)
pdf.cell(40,10,f"                      {int(publicaciones)} en Facebook, Twitter, Instagram y Linkedin",ln=True)
pdf.set_font("helvetica", "I", 11,)
pdf.cell(40,8,f"        Likes a la fecha:",ln=True)
pdf.set_font("helvetica", "", 11,)
pdf.cell(40,10,f"                      {int(likes_facebook)} en Facebook, {int(likes_twitter)} en Twitter, {int(likes_instagram)} en Instagram y {int(likes_linkedin)} en Linkedin",ln=True)
pdf.cell(40,12,f" ", ln=True)

pdf.set_font("helvetica", "B", 11,)
pdf.cell(40,8,f"ESTADO DE CUMPLIMIENTO DE LA AGENDA:",ln=True)
pdf.set_font("helvetica", "", 11,)
fecha_ultimo = pd.to_datetime(str(fecha_ultimo_monitor.values[0]))
pdf.multi_cell(190, 6.5,f"             A la fecha, se han presupuestado {len(hitos_desde_ultimo_monitor)} tareas a realizar, contando a partir de la supuesta fecha de publicación del último monitor ({numero_proxima_edicion-1}) ({fecha_ultimo.strftime('%d/%m/%Y')}), de las cuales se han realizado y completado un {round(porcentaje_de_hitos_realizados,2)}%.",ln=True)
pdf.cell(40,3,f" ", ln=True)
pdf.set_font("helvetica", "I", 11,)
pdf.cell(40,8,f"        Los pendientes del {numero_proxima_edicion-1}:", ln=True)
pdf.set_font("helvetica", "", 11,)
for h in hitos_no_cumplidos_desde_ultimo_monitor_ANTERIOR_MONITOR.values:
    pdf.cell(40,10,f"                      {h}", ln=True)
pdf.set_font("helvetica", "I", 11,)
pdf.cell(40,8,f"        Los pendientes del {numero_proxima_edicion}:", ln=True)
pdf.set_font("helvetica", "", 11,)
for h2 in hitos_no_cumplidos_desde_ultimo_monitor_PROXIMO_MONITOR.values:
    pdf.cell(40,10,f"                      {h2}", ln=True) 
pdf.cell(40,12,f" ", ln=True)

pdf.set_font("helvetica", "B", 11,)
pdf.cell(40,8,f"PRÓXIMOS TEMAS A TRABAJAR, sobre las ediciones {np.unique(ediciones_a_trabajar)}:", ln=True)
pdf.set_font("helvetica", "", 11,)
for h3 in temas_a_trabajar.values:
    pdf.cell(40,8,f"                      {h3}", ln=True) 
pdf.cell(40,16,f" ", ln=True)

pdf.set_font("helvetica", "", 8,)

pdf.multi_cell(190, 6.5,f"             * La información expuesta en el reporte se basa estrictamente en el contenido de la agenda ",ln=True)

pdf.cell(40,8,f" ", ln=True)
pdf.cell(40,8,f"        CONFECCIONADO POR: VALENTIN VEDDA", ln=True)
pdf.cell(40,8,f"        REVISADO POR: JOSÉ LEZAMA", ln=True)

pdf.output(f"Reporte Monitor {hoy}.pdf")

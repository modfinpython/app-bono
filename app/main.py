# Importamos Librerías Requieren Instalación
import pandas as pd
from nicegui import ui
import plotly.graph_objects as go
from bono import CuponCero, CuponFijo, CuponVariable


def app_bono():
    calendario = pd.DataFrame()
    datos_grafica = pd.DataFrame()
    figura = go.Figure()
    medidas = pd.DataFrame()
    # Función para actualizar el ag-Grid con el DataFrame

    figura.update_layout(width=480, height=480)

    def actualizar():
        valor_nominal = valor_nominal_input.value
        tasa_cupon = tasa_cupon_input.value
        tasa_rendimiento = tasa_rendimiento_input.value
        sobre_tasa = sobre_tasa_input.value
        periodo_cupon = periodo_cupon_input.value
        dias_vencimiento = dias_vencimiento_input.value
        dias_por_año = dias_por_año_input.value
        
        valor_seleccionado = opciones_radio.value

        if valor_seleccionado == 'Cero':
            bono = CuponCero(valor_nominal, tasa_cupon, tasa_rendimiento, sobre_tasa, periodo_cupon, dias_vencimiento, dias_por_año)
        elif valor_seleccionado == 'Fijo':
            bono = CuponFijo(valor_nominal, tasa_cupon, tasa_rendimiento, sobre_tasa, periodo_cupon, dias_vencimiento, dias_por_año)
        elif valor_seleccionado == 'Variable':
            bono = CuponVariable(valor_nominal, tasa_cupon, tasa_rendimiento, sobre_tasa, periodo_cupon, dias_vencimiento, dias_por_año)

        calendario = bono.obtener_calendario_pagos()
        datos_grafica = bono.obtener_grafico_precio_ytm(0.25,0.001,60)
        medidas = bono.obtener_medidas()

        
        medidas_reset = medidas.reset_index()

        medidas_tabla.columns = [{'name': col, 'label': col, 'field': col} for col in medidas_reset.columns]
        medidas_tabla.rows = medidas_reset.to_dict('records')

        calendario_reset = calendario.reset_index()
        calendario_tabla.columns = [{'name': col, 'label': col, 'field': col} for col in calendario_reset.columns]
        calendario_tabla.rows = calendario_reset.to_dict('records')
        
        figura.update_traces(overwrite=True, x=datos_grafica['Tasa'], y=datos_grafica['Precio'])
        #figura.add_trace(go.Scatter(x=[tasa_rendimiento], y=[bono.precio_sucio], mode='markers', name='Punto Específico'))
        plot.update()


    with ui.card().classes('no-shadow border-[1px]'):
        with ui.row():
            ui.label('Modelo Bono').style('color: #6E93D6; font-size: 200%; font-weight: 400')
        with ui.row():
            with ui.card().style('width: 280px; height: 665px;'):
                ui.label('Variables de Entrada').style('color: #6E93D6; font-size: 100%; font-weight: 400')
                # Creación de la interfaz de usuario con entradas
                valor_nominal_input = ui.number(label='Valor Nominal', value=100).props('clearable')
                tasa_cupon_input = ui.number(label='Tasa Cupón', value=0.05).props('clearable')
                tasa_rendimiento_input = ui.number(label='Tasa Rendimiento', value=0.1007).props('clearable')
                sobre_tasa_input = ui.number(label='Sobre Tasa', value=0).props('clearable')
                periodo_cupon_input = ui.number(label='Periodo', value=182).props('clearable')
                dias_vencimiento_input = ui.number(label='Plazo', value=366).props('clearable')
                dias_por_año_input = ui.number(label='Días Año', value=360).props('clearable')

                bono = CuponFijo(valor_nominal_input.value,tasa_cupon_input.value, tasa_rendimiento_input.value, sobre_tasa_input.value, periodo_cupon_input.value,dias_vencimiento_input.value,dias_por_año_input.value )
                calendario = bono.obtener_calendario_pagos()
                medidas = bono.obtener_medidas()


                datos_grafica = bono.obtener_grafico_precio_ytm(0.25,0.001,60)
                figura.add_trace(go.Scatter(x=datos_grafica['Tasa'], y=datos_grafica['Precio']))
                figura.update_layout(margin=dict(l=0, r=0, t=0, b=0))

                opciones_radio = ui.radio(['Cero', 'Fijo', 'Variable'], value='Fijo').props('inline').style('font-size: 0.8em;')


            # Botón para actualizar el ag-Grid con nuevos datos
                ui.button('Actualizar', on_click=actualizar).style('font-size: 0.8em;')

            with ui.card().style('width: 500px; height: 665px;'):
                ui.label('Gráfica Precio vs Tasa').style('color: #6E93D6; font-size: 100%; font-weight: 400')
                plot = ui.plotly(figura).classes('width: 50%; height: auto;')

            with ui.card().style('width: 300px; height: 665px;'):
                ui.label('Medidas').style('color: #6E93D6; font-size: 100%; font-weight: 400')
                medidas_reset = medidas.reset_index()
                medidas_tabla = ui.table.from_pandas(medidas).style("width:100%;height:100%;").classes("text-left")
                medidas_tabla.columns = [{'name': col, 'label': col, 'field': col} for col in medidas_reset.columns]
                medidas_tabla.rows = medidas_reset.to_dict('records')

        with ui.row():
            with ui.card().style('width: 1160px'):
                ui.label('Calendario de Pagos').style('color: #6E93D6; font-size: 100%; font-weight: 400')
                calendario_reset = calendario.reset_index()
                calendario_tabla = ui.table.from_pandas(calendario).style("width:100%;height:100%;")
                calendario_tabla.columns = [{'name': col, 'label': col, 'field': col} for col in calendario_reset.columns]
                calendario_tabla.rows = calendario_reset.to_dict('records')


app_bono()
ui.run()
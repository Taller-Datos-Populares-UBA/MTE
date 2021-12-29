from datetime import datetime

import plotly.graph_objs as go

from mte_dataframe import MTEDataFrame
from utils.utils import crear_df_filtrado
from utils.utils_panel import pesos_historico_promedio, torta, pesos_historico_predios, datos_tabla


class DashPanelControlHandler:

    def __init__(self, tabla_resumen):
        self.fig_hist = go.Figure()
        self.fig_torta = go.Figure()
        self.fig_barras = go.Figure()
        self.tabla_resumen = tabla_resumen
        self.open_sininfopanel_modal = False

    def panel_control(self, trigger, clasificador, predios, rutas, materiales, cartonere, fecha_inicio, fecha_fin):

        if trigger["prop_id"] in ['.', "btn-filtro.n_clicks"] or trigger["prop_id"].split('.')[0] == "dropdown_clasificador_vistas":
            df = MTEDataFrame.get_instance()
            df_filtrado = crear_df_filtrado(df, predios, rutas, datetime.fromisoformat(fecha_inicio),
                                            datetime.fromisoformat(fecha_fin), materiales, cartonere)
            if df_filtrado.empty:
                self.open_sininfopanel_modal = True
            else:
                self.fig_hist = pesos_historico_promedio(df_filtrado, clasificador)
                self.fig_torta = torta(df_filtrado, clasificador)
                self.fig_barras = pesos_historico_predios(df_filtrado, clasificador)
                self.tabla_resumen = datos_tabla(df_filtrado, clasificador)
                self.tabla_resumen = self.tabla_resumen.to_dict('records')

        elif trigger["prop_id"] in ['.', "close-modal-sininfopanel-button.n_clicks"]:
            self.open_sininfopanel_modal = False

        return self.fig_hist, self.fig_torta, self.fig_barras, self.open_sininfopanel_modal, self.tabla_resumen

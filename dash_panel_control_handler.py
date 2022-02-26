from datetime import datetime

import plotly.graph_objs as go

from dash_handler import DashHandler
from mte_dataframe import MTEDataFrame
from utils.utils import crear_df_filtrado
from utils.utils_panel import pesos_historico_promedio, torta, pesos_historico_predios, datos_tabla

from exceptions import *

class DashPanelControlHandler(DashHandler):

    def __init__(self, tabla_resumen):
        super().__init__()
        self.fig_hist = go.Figure()
        self.fig_torta = go.Figure()
        self.fig_barras = go.Figure()
        self.tabla_resumen = tabla_resumen

    def _execute_callback(self, trigger, clasificador, predios, rutas, materiales, cartonere, fecha_inicio, fecha_fin):
        fig_hist, fig_torta, fig_barras, show_modal, title_modal, descr_modal, tabla_resumen = self._get_response()

        if trigger["prop_id"] == "btn-filtro.n_clicks" or trigger["prop_id"].split('.')[
            0] == "dropdown_clasificador_vistas":
            df = MTEDataFrame.get_instance()
            print("aguante boca")
            print(df)
            df_filtrado = crear_df_filtrado(df, predios, rutas, datetime.fromisoformat(fecha_inicio),
                                            datetime.fromisoformat(fecha_fin), materiales, cartonere)
            print("el fantasma de la b")
            print(df_filtrado)
            if df_filtrado.empty:
                raise EmptyDataFrameError
            else:
                fig_hist = pesos_historico_promedio(df_filtrado, clasificador)
                fig_torta = torta(df_filtrado, clasificador)
                fig_barras = pesos_historico_predios(df_filtrado, clasificador)
                tabla_resumen = datos_tabla(df_filtrado, clasificador)
                tabla_resumen = tabla_resumen.to_dict('records')

        self._save_response(fig_hist, fig_torta, fig_barras, show_modal, title_modal, descr_modal, tabla_resumen)

    def _get_response(self):
        return [self.fig_hist,
                self.fig_torta,
                self.fig_barras,
                self.show_modal,
                self.title_modal,
                self.descr_modal,
                self.tabla_resumen]

    def _save_response(self, fig_hist, fig_torta, fig_barras, show_modal, title_modal, descr_modal, tabla_resumen):
        self.fig_hist = fig_hist
        self.fig_torta = fig_torta
        self.fig_barras = fig_barras
        self.show_modal = show_modal
        self.title_modal = title_modal
        self.descr_modal = descr_modal
        self.tabla_resumen = tabla_resumen

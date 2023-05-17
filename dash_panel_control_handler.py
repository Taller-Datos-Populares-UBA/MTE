from datetime import datetime

import plotly.graph_objs as go

from dash_handler import DashHandler
from exceptions import *
from mte_dataframe import MTEDataFrame
from utils.utils import crear_df_filtrado, crear_tabla
from utils.utils_panel import pesos_historico_promedio, crear_tabla_resumen, torta, pesos_historico_predios, datos_tabla, crear_titulos

class DashPanelControlHandler(DashHandler):

    def __init__(self):
        super().__init__()
        self.fig_hist = go.Figure()
        self.fig_torta = go.Figure()
        self.fig_barras = go.Figure()
        self.tabla_resumen = crear_tabla(id="tabla-Resumen",
                                         titulos_columnas=crear_titulos([]),
                                         tipos={"peso": "numeric"},
                                         dimensiones=("auto", "200px"))


    def _execute_callback(self, trigger, clasificador, predios, rutas, materiales, cartonere, fecha_inicio, fecha_fin, columnas_resumen):
        fig_hist, fig_torta, fig_barras, show_modal, title_modal, descr_modal, tabla_resumen = self._get_response()
        if (trigger["prop_id"] in ["btn-filtro.n_clicks",
                                   "dropdown_clasificador_vistas.value",
                                   "dropdown-resumen.value"]):
            df = MTEDataFrame.get_instance()
            df_filtrado = crear_df_filtrado(df, predios, rutas, datetime.fromisoformat(fecha_inicio),
                                            datetime.fromisoformat(fecha_fin), materiales, cartonere)

            if df_filtrado.empty:
                raise EmptyDataFrameError()
            else:
                fig_hist = pesos_historico_promedio(df_filtrado, clasificador)
                fig_torta = torta(df_filtrado, clasificador)
                fig_barras = pesos_historico_predios(df_filtrado, clasificador)
                tabla_resumen = crear_tabla_resumen(df_filtrado,
                                                    columnas_resumen)

        self._save_response(fig_hist, fig_torta, fig_barras, show_modal, title_modal, descr_modal, tabla_resumen)


    def _get_response(self):
        return [self.fig_hist,
                self.fig_torta,
                self.fig_barras,
                self.show_modal,
                self.title_modal,
                self.descr_modal,
                self.tabla_resumen,
                ]

    def _save_response(self, fig_hist, fig_torta, fig_barras, show_modal, title_modal, descr_modal, tabla_resumen):
        self.fig_hist = fig_hist
        self.fig_torta = fig_torta
        self.fig_barras = fig_barras
        self.show_modal = show_modal
        self.title_modal = title_modal
        self.descr_modal = descr_modal
        self.tabla_resumen = tabla_resumen

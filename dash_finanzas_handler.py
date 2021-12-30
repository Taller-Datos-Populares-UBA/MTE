from datetime import datetime

import pandas as pd
import plotly.graph_objs as go

from dash_handler import DashHandler
from mte_dataframe import MTEDataFrame
from utils.utils import crear_df_filtrado
from utils.utils_finanzas import grafico_torta, pago_por_predio, pago_individual


class DashFinanzasHandler(DashHandler):

    def __init__(self, tabla_resumen, tabla_todos):
        super().__init__()
        self.fig_recolectado = go.Figure()
        self.tabla_resumen = tabla_resumen
        self.tabla_todos = tabla_todos
        self.total_a_pagar_por_usuario = "$ 0"

    def _execute_callback(self, trigger, tab, refresh_n_clicks, predios, fecha_inicio, fecha_fin, legacy_id, data,
                          rutas,
                          materiales, cartonere):

        show_modal, title_modal, descr_modal, fig_recolectado, total_a_pagar_por_usuario, tabla_resumen, tabla_todos = self._get_response()
        df_pagos = pd.DataFrame()

        df = MTEDataFrame.get_instance()
        df_filtrado = crear_df_filtrado(df, predios, rutas, datetime.fromisoformat(fecha_inicio),
                                        datetime.fromisoformat(fecha_fin), materiales, cartonere)

        df_precios = pd.DataFrame(data)

        if (trigger["prop_id"] == "refresh-button.n_clicks") or (tab == "todxs"):

            try:
                df_pagos = pago_por_predio(df_filtrado, df_precios)
            except Exception as e:
                print("No pude calcular el pago, error:", e)

        elif trigger["prop_id"] == "search-button.n_clicks":
            df_is_empty = df_filtrado.empty
            legacy_not_found = legacy_id not in list(df_filtrado["legacyId"])

            if (not df_is_empty) and (not legacy_not_found):

                if trigger["prop_id"] == "search-button.n_clicks":
                    fig_recolectado = grafico_torta(legacy_id, df_filtrado)
                    pago = pago_individual(df_filtrado, df_precios, legacy_id)
                    total_a_pagar_por_usuario = "$ " + str(pago)

                    ultimos_movimientos = df_filtrado[df_filtrado.legacyId == legacy_id]
                    ultimos_movimientos = ultimos_movimientos.sort_values("fecha", ascending=False)
                    ultimos_movimientos["fecha"] = ultimos_movimientos["fecha"].dt.strftime("%d/%m/%Y")
                    tabla_resumen = ultimos_movimientos.to_dict('records')

            elif df_is_empty:
                show_modal = True
                title_modal = "No se encontró información"
                descr_modal = "Revisá si estan correctamente seleccionados los filtros"

            elif legacy_not_found:
                show_modal = True
                title_modal = "No se encontró información"
                descr_modal = "Revisá si pusiste bien el número de legajo"

        tabla_todos = df_pagos.reset_index().to_dict('records')

        self._save_response(show_modal, title_modal, descr_modal, fig_recolectado, total_a_pagar_por_usuario,
                            tabla_resumen, tabla_todos)

    def _get_response(self):
        return [self.show_modal,
                self.title_modal,
                self.descr_modal,
                self.fig_recolectado,
                self.total_a_pagar_por_usuario,
                self.tabla_resumen,
                self.tabla_todos]

    def _save_response(self, show_modal, title_modal, descr_modal, fig_recolectado, total_a_pagar_por_usuario,
                       tabla_resumen, tabla_todos):
        self.show_modal = show_modal
        self.title_modal = title_modal
        self.descr_modal = descr_modal
        self.fig_recolectado = fig_recolectado
        self.total_a_pagar_por_usuario = total_a_pagar_por_usuario
        self.tabla_resumen = tabla_resumen
        self.tabla_todos = tabla_todos

import pandas as pd
from datetime import datetime
from mte_dataframe import MTEDataFrame
from utils.utils import crear_df_filtrado
from utils.utils_finanzas import grafico_torta, parse_contents, pago_por_predio, pago_individual
import plotly.graph_objs as go

class DashFinanzasHandler:

	def __init__(self,tabla_resumen,tabla_todos):
		self.fig_recolectado = go.Figure()
		self.tabla_resumen = tabla_resumen
		self.tabla_todos = tabla_todos
		self.total_a_pagar_por_usuario = "$ 0"
		self.open_sininfopanel_modal = False
		self.legacy_id_no_encontrado_is_open = False
		self.errorpago_is_open = False

	def filtrar(self, trigger, tab, refresh_n_clicks, predios,fecha_inicio, fecha_fin, legacy_id, data, rutas, materiales, cartonere):

		if "Todas" in rutas:
			rutas = None
		
		df_pagos = pd.DataFrame()

		df = MTEDataFrame.get_instance()
		df_filtrado = crear_df_filtrado(df, predios, rutas, datetime.fromisoformat(fecha_inicio),
                                    datetime.fromisoformat(fecha_fin), materiales, cartonere)

		df_precios = pd.DataFrame(data)

	    # Si llame a la funcion apretando el boton de refrescar, buscar, o cambie a la tab de Todxs:
		if (trigger["prop_id"] in ["refresh-button.n_clicks"]) or (tab == "todxs"):  # REVISAR
			
			try:
				df_pagos = pago_por_predio(df_filtrado, df_precios)
			except Exception as e:
				print("No pude calcular el pago, error:", e)

		elif trigger["prop_id"] in ["search-button.n_clicks"]:
			df_is_empty = df_filtrado.empty
			legacy_not_found = legacy_id not in list(df_filtrado["legacyId"])

			if (not df_is_empty) and (not legacy_not_found):  # Si se cumplen las dos condiciones, muestra todo lo que tiene que mostrar

				if trigger["prop_id"] == "search-button.n_clicks":
					self.fig_recolectado = grafico_torta(legacy_id, df_filtrado)
					try:
						pago = pago_individual(df_filtrado, df_precios, legacy_id)
					except Exception as e:
						pass
					if pago == "Error":  # Del hecho de que la tabla de precios esta vacio
						self.errorpago_is_open = True
					else:  # Modificamos el formato del pago
						self.total_a_pagar_por_usuario = "$ " + str(pago)

					ultimos_movimientos = df_filtrado[df_filtrado.legacyId == legacy_id]
					ultimos_movimientos = ultimos_movimientos.sort_values("fecha", ascending=False)
					ultimos_movimientos["fecha"] = ultimos_movimientos["fecha"].dt.strftime("%d/%m/%Y")
					#self.tabla_resumen = [ultimos_movimientos.iloc[i].to_dict() for i in
											#range(len(ultimos_movimientos.index))]
					self.tabla_resumen = ultimos_movimientos.to_dict('records')

			elif df_is_empty:  # Si el df esta vacio, te avisa con el modal de que esta vacio
				self.open_sininfopanel_modal = True

			elif legacy_not_found:  # Si la persona no esta en el df, te avisa con el modal
				self.legacy_id_no_encontrado_is_open = True

	    # Los siguientes 3 elif son para cerrar los modals
		elif trigger["prop_id"] == "close-modal-sininfo-button.n_clicks":
			self.open_sininfopanel_modal = False

		elif trigger["prop_id"] == "close-modal-legacy_id-button.n_clicks":
			self.legacy_id_no_encontrado_is_open = False

		elif trigger["prop_id"] == "close-modal-errorpago-button.n_clicks":
			self.errorpago_is_open = False

		self.tabla_todos = df_pagos.reset_index().to_dict('records')

		return self.open_sininfopanel_modal, self.fig_recolectado, self.total_a_pagar_por_usuario, self.legacy_id_no_encontrado_is_open, self.tabla_resumen, self.errorpago_is_open, self.tabla_todos



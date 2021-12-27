from datetime import datetime
from mte_dataframe import MTEDataFrame
from utils.utils import crear_df_filtrado
from utils.utils_panel import pesos_historico_promedio, torta, pesos_historico_predios, datos_tabla
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

	def filtrar(self,trigger,tab, refresh_n_clicks, predios,fecha_inicio, fecha_fin, legacy_id, data, rutas, materiales, cartonere):

		if "Todas" in rutas:
			rutas = None

		df = MTEDataFrame.get_instance()
		trigger = callback_context.triggered[0]
		df_pagos = pd.DataFrame()

	    # Si llame a la funcion apretando el boton de refrescar, buscar, o cambie a la tab de Todxs:
		if trigger["prop_id"] in ["refresh-button.n_clicks"] and tab == "todxs":  # REVISAR
			df_precios = pd.DataFrame(data)
			df_filtrado = crear_df_filtrado(df, predios, rutas, datetime.fromisoformat(fecha_inicio),
											datetime.fromisoformat(fecha_fin), materiales, cartonere)
			try:
				df_pagos = pago_por_predio(df_filtrado, df_precios)
			except Exception as e:
				print("No pude calcular el pago, error:", e)

		elif trigger["prop_id"] in ["search-button.n_clicks"]:
	        # Solo en este caso va a buscar el df, filtrar, y realizar todos estos procesos que llevan tiempo.
			df_precios = pd.DataFrame(data)
			df_filtrado = crear_df_filtrado(df, predios, rutas, datetime.fromisoformat(fecha_inicio),
	                                        datetime.fromisoformat(fecha_fin), materiales, cartonere)

	        # Chequea que el df_filtrado no este vacio, y que la persona que buscamos este en el df.
			cond1 = not df_filtrado.empty
			cond2 = legacy_id in list(df_filtrado["legacyId"])

			if cond1 and cond2:  # Si se cumplen las dos condiciones, muestra todo lo que tiene que mostrar

				if trigger["prop_id"] == "search-button.n_clicks":
					figure = grafico_torta(legacy_id, df_filtrado)
					try:
						pago = pago_individual(df_filtrado, df_precios, legacy_id)
					except Exception as e:
						ultimos_movimientos = df_filtrado[df_filtrado.legacyId == legacy_id]
					if pago == "Error":  # Del hecho de que la tabla de precios esta vacio
						errorpago_is_open = not errorpago_is_open
					else:  # Modificamos el formato del pago
						pago = "$ " + str(pago)

					ultimos_movimientos = ultimos_movimientos.sort_values("fecha", ascending=False)
					ultimos_movimientos["fecha"] = ultimos_movimientos["fecha"].dt.strftime("%d/%m/%Y")
					ultimos_movimientos = [ultimos_movimientos.iloc[i].to_dict() for i in
											range(len(ultimos_movimientos.index))]

			elif not cond1:  # Si el df esta vacio, te avisa con el modal de que esta vacio
				sininfo_is_open = not sininfo_is_open

			elif not cond2:  # Si la persona no esta en el df, te avisa con el modal
				legacy_id_no_encontrado_is_open = not legacy_id_no_encontrado_is_open

	    # Los siguientes 3 elif son para cerrar los modals
		elif trigger["prop_id"] == "close-modal-sininfo-button.n_clicks":
			sininfo_is_open = not sininfo_is_open

		elif trigger["prop_id"] == "close-modal-legacy_id-button.n_clicks":
			legacy_id_no_encontrado_is_open = not legacy_id_no_encontrado_is_open

		elif trigger["prop_id"] == "close-modal-errorpago-button.n_clicks":
			errorpago_is_open = not errorpago_is_open

		df_pagos = df_pagos.reset_index().to_dict('records')



import base64
import io

from apps import panel_control, finanzas, error404
from dash_handler import DashHandler
from mte_dataframe import MTEDataFrame

from exceptions import *

class DashIndexHandler(DashHandler):

    def __init__(self):
        super().__init__()
        self.layout = None
        self.panelcontrol_navbar = "link-active"
        self.finanzas_navbar = ""

    def _execute_callback(self, trigger, pathname, list_of_contents, list_of_names, list_of_dates):
        if trigger["prop_id"] == "upload-comp-base.contents":
            if list_of_contents is not None:
                files_list = [
                    self.parse_contents(c, n, d) for c, n, d in
                    zip(list_of_contents, list_of_names, list_of_dates)]
                print("-------------")
                print(f"{files_list}")
                print("-------------")
                MTEDataFrame.reset_with_files(files_list)

        if MTEDataFrame.FILES_TO_LOAD:
            predios, rutas, materiales, cartoneres = MTEDataFrame.create_features()
        else:
            predios, rutas, materiales, cartoneres = [], [], [], []

        if pathname == '/panel_control' or pathname == '/':
            layout = panel_control.layout(predios, rutas, materiales, cartoneres)
            panelcontrol_navbar = "link-active"
            finanzas_navbar = ""
        elif pathname == '/finanzas':
            layout = finanzas.layout(predios, rutas, materiales, cartoneres)
            panelcontrol_navbar = ""
            finanzas_navbar = "link-active"
        else:
            layout = error404.layout
            panelcontrol_navbar = ""
            finanzas_navbar = ""

        self._save_response(layout, panelcontrol_navbar, finanzas_navbar)

    def _save_response(self, layout, panelcontrol_navbar, finanzas_navbar):
        self.layout = layout
        self.panelcontrol_navbar = panelcontrol_navbar
        self.finanzas_navbar = finanzas_navbar

    def _get_response(self):
        return [self.layout,
                self.panelcontrol_navbar,
                self.finanzas_navbar,
                self.show_modal,
                self.title_modal,
                self.descr_modal]

    def parse_contents(self, contents, filename, date):
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)

        if filename.endswith(".csv"):
            return io.StringIO(decoded.decode('utf-8'))
        elif filename.endswith(".xls") or filename.endswith(".xlsx"):
            return io.BytesIO(decoded)

        return None  # TODO It should raise an exception

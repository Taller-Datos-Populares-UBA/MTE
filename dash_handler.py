class DashHandler:

    def __init__(self):
        self.show_modal = False
        self.title_modal = ''
        self.descr_modal = ''

    def callback(self, *args):
        try:
            self._execute_callback(*args)
        except Exception as e:
            self.show_modal = True
            self.title_modal = 'Error inesperadisimo rey'
            self.descr_modal = e

        return self._create_response()

    def _execute_callback(self, *args):
        raise Exception("subclass responsiblity")

    def _create_response(self):
        raise Exception("subclass responsiblity")

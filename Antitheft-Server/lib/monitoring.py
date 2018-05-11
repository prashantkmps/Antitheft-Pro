from flask import *


class Monitoring:
    def __init__(self):
        pass

    @staticmethod
    def show_monitoringpage(app):
        return render_template(
            'monitoring.html',
            title="Monitoring",
            app=app
        )

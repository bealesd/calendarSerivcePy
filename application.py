from flask import Flask
from flask import make_response
from flask import request
from flask import Response

import calendarController
import calendarRepo
import validationHelper

import config
configInstance = config.Config()


class AppServer(object):
    def __init__(self):
        self.acl_origin = configInstance.ACL_ORIGIN
        self.calendarRepoInstance = calendarRepo.CalendarRepo()
        self.calendarControllerInstance = calendarController.CalendarController(
            self.calendarRepoInstance)

    def allow_all_origins(self, response):
        if request.method == 'OPTIONS':
            response.headers.remove('Access-Control-Allow-Headers')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'POST, PUT, DELETE')

        response.headers.remove(self.acl_origin)
        response.headers.add(self.acl_origin, "*")

        return response

    def run(self, debug: bool):
        self.app = Flask(__name__)

        self.app.add_url_rule('/events', view_func=self.calendarControllerInstance.main, methods=["GET", "POST"])
        self.app.add_url_rule('/events/<string:guid>', view_func=self.calendarControllerInstance.main, methods=["GET", "POST", "PUT", "DELETE"])

        self.app.teardown_appcontext(self.calendarRepoInstance._del)

        self.app.after_request(self.allow_all_origins)

        self.app.register_error_handler(
            404, f=self.calendarControllerInstance.unknown_route)

        print('\nUrl routes:')
        for rule in self.app.url_map.iter_rules():
            methods = ','.join(rule.methods)
            print("\t{:40s} {:20s}".format(methods, rule.rule))
        print()

        self.app.run(debug=debug, use_debugger=False, use_reloader=False, passthrough_errors=True)


if __name__ == '__main__':
    AppServer().run(True)
else:
    AppServer().run(True)

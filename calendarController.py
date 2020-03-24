import validationHelper
import html

from flask import Response
from flask import request
from flask import json
from flask import make_response

import config
configInstance = config.Config()

validationHelperInstance = validationHelper.ValidationHelper()


class CalendarController(object):
    def __init__(self, calendarRepo):
        self.guid = configInstance.GUID
        self.title = configInstance.TITLE
        self.year = configInstance.YEAR
        self.month = configInstance.MONTH
        self.day = configInstance.DAY
        self.hour = configInstance.HOUR
        self.minute = configInstance.MINUTE

        self.acl_origin = configInstance.ACL_ORIGIN

        self.calendarRepo = calendarRepo

    def post_event(self):
        '''
        post api:
            {"title": "bday", "year": "1986", "month": "7",
                "day": "14", "hour": "19", "minute": "30"}
        '''
        request.get_json()

        kwargs = {
            self.title: html.escape(request.json[self.title]),
            self.year: request.json[self.year],
            self.month: request.json[self.month],
            self.day: request.json[self.day],
            self.hour: request.json[self.hour],
            self.minute: request.json[self.minute]
        }

        validated_args = validationHelperInstance.get_validated_args(**kwargs)

        guid = self.calendarRepo.insertRow(validated_args[self.title],
                                           validated_args[self.year],
                                           validated_args[self.month],
                                           validated_args[self.day],
                                           validated_args[self.hour],
                                           validated_args[self.minute])

        return Response(json.dumps({'guid': guid}),
                        mimetype='application/json')

    def update_event(self, guid):
        '''
        update api:
            {"guid": "0be37e56-bf01-4493-a7bf-5425d4ea5954","title": "bday",
                "year": "1986", "month": "7", "day": "14", "hour": "19", "minute": "30"}
        '''
        request.get_json()

        kwargs = {
            self.guid: guid,
            self.title: html.escape(request.json[self.title]),
            self.year: request.json[self.year],
            self.month: request.json[self.month],
            self.day: request.json[self.day],
            self.hour: request.json[self.hour],
            self.minute: request.json[self.minute]
        }

        validated_args = validationHelperInstance.get_validated_args(**kwargs)

        self.calendarRepo.updateRow(validated_args[self.guid],
                                           validated_args[self.title],
                                           validated_args[self.year],
                                           validated_args[self.month],
                                           validated_args[self.day],
                                           validated_args[self.hour],
                                           validated_args[self.minute])

        return Response(json.dumps({'Updated guid': guid}),
                        mimetype='application/json')

    def delete_event(self, guid):
        kwargs = {
            self.guid: guid
        }

        validated_args = validationHelperInstance.get_validated_args(**kwargs)

        self.calendarRepo.deleteRow(validated_args[self.guid])

        return Response(response=json.dumps({'Deleted guid': validated_args[self.guid]}),
                        mimetype='application/json',
                        status=200)

    def unknown_route(self, error):
        response = make_response('Route "%s" does not exist.' %
                                 request.base_url, 404)
        return response

    def route_get_events(self):
        year = request.args.get(self.year)
        month = request.args.get(self.month)

        getAllEvents = year == None or month == None

        if getAllEvents:
            response = self.get_all_events()
        else:
            response = self.get_events_by_year_and_month(year, month)
        return response

    def get_all_events(self):
        result = self.calendarRepo.getAll()
        response = Response(json.dumps(result), mimetype='application/json')
        return response

    def get_events_by_year_and_month(self, year, month):
        kwargs = {
            self.year: year,
            self.month: month
        }

        validated_args = validationHelperInstance.get_validated_args(**kwargs)

        result = self.calendarRepo.getRecordsByYearAndMonth(
            validated_args[self.year], validated_args[self.month])

        return Response(json.dumps(result),
                        mimetype='application/json')

    def get_event_by_id(self, guid):
        kwargs = {
            self.guid: guid
        }
        validated_args = validationHelperInstance.get_validated_args(**kwargs)

        result = self.calendarRepo.getRecordById(validated_args[self.guid])
        response = Response(json.dumps(result), mimetype='application/json')
        return response

    def route_events(self):
        if request.method == 'GET':
            response = self.route_get_events()
        elif request.method == 'POST':
            response = self.post_event()
        return response

    def route_events_with_id(self, guid):
        if request.method == 'GET':
            response = self.get_event_by_id(guid)
        elif request.method == 'PUT':
            response = self.update_event(guid)
        elif request.method == 'DELETE':
            response = self.delete_event(guid)
        else:
            raise ValueError('Request method: {0}, is not supported for route: {1}.'.format(
                request.method, request.path))
        return response

    def main(self, guid=None):
        try:
            response = None

            self.calendarRepo._init()
            if guid:
                response = self.route_events_with_id(guid)
            else:
                response = self.route_events()

        except TypeError as e:
            message = e.args[0]
            response = make_response(message, 400)
            response.headers['X-Error'] = 'Type Error.'

        except ValueError as e:
            message = e.args[0]
            response = make_response(message, 400)
            response.headers['X-Error'] = 'Value error.'

        except Exception as e:
            message = e.args[0]
            response = make_response(message, 500)
            response.headers['X-Error'] = 'Data access error.'

        finally:
            if response == None:
                response = make_response(
                    'Data access error. No response was returned.', 500)
            return response

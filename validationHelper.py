from flask import make_response

import re
import uuid

import config
configInstance = config.Config()

class ValidationHelper(object):
    def __init__(self):
        self.paramenter_validation_dict = configInstance.PARAMETER_VALIDATION_DICT

    def error_helper(self, error_name, *args):
        if error_name == 'arg_value_error':
            raise TypeError('Argument name: {0}.Required argument as no value.'.format(args[0]))
        elif error_name == 'invalid_arg_name':
            raise KeyError('Argument name: {0}.\nValue: {1}.\nArgument not in config dicitonary.'.format(args[0], args[1]))
        elif error_name == 'invalid_value':
            raise KeyError('Argument name: {0}.\nValue: {1}.\nArgument not in config dicitonary.'.format(args[0], args[1]))
        

    def get_validated_args(self, **kwarg):
        validated_args = {}
        for arg_name, arg_value in kwarg.items():
            if arg_value == None:
                raise TypeError('Argument name: {0}.Required argument as no value.'.format(arg_name))

            if arg_name not in self.paramenter_validation_dict:
                raise KeyError('Argument name: {0}.\nValue: {1}.\nArgument not in config dicitonary.'.format(
                    arg_name, arg_value))

            static_arg = self.paramenter_validation_dict[arg_name]
            static_type = static_arg['type']
            static_regex = static_arg['regex']

            if re.search(static_regex, arg_value) == None:
                raise ValueError('Argument name: {0}.\nValue: {1}.\nType: {2}.\nOut of range.'.format(
                    arg_name, arg_value, static_type))

            if static_type == 'int':
                validated_arg_value = self.parse_int(arg_value)
            elif static_type == 'guid':
                validated_arg_value = self.parse_uuid_v4(arg_value)
            elif static_type == 'string':
                validated_arg_value = arg_value

            if validated_arg_value == None:
                raise TypeError('Argument name: {0}.\nValue: {1}.\nCould not be cast to {}.'.format(
                    arg_name, arg_value, static_type))

            validated_args[arg_name] = validated_arg_value

        return validated_args

    def parse_int(self, value):
        try:
            return int(value)
        except:
            return None

    def parse_bool(self, value):
        try:
            return bool(value)
        except:
            return None

    def parse_uuid_v4(self, value):
        try:
            uuid_v4 = uuid.UUID(value)
            if uuid_v4.version != 4:
                raise ValueError('{} is not version 4'.format(value))
            return value
        except:
            return None


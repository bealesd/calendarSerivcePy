class Config(object):
    TABLE_NAME = 'calendar'
    DATABASE_NAME = 'calendar.db'

    ACL_ORIGIN = 'Access-Control-Allow-Origin'
    
    # DICT OF PARAMAS
    TITLE = 'title'
    YEAR = 'year'
    MONTH = 'month'
    DAY = 'day'
    HOUR = 'hour'
    MINUTE = 'minute'
    GUID = 'guid'

    PARAMETER_VALIDATION_DICT = {
        TITLE: {
            'type': 'string',
            'regex': r'^.{1,100}$'
            },
        YEAR: {
            'type': 'int',
            'regex': r'^(20[0-9]{2}|19[0-9]{2})$'
            },
        MONTH: {
            'type': 'int',
            'regex': r'^(0?[0-9]|1[0-1])$'
            },
        DAY: {#TODO: do an dditional check later to see if date can exist
            'type': 'int',
            'regex': r'^(0?[1-9]|[12][0-9]|3[01])'
            },
        HOUR: {
            'type': 'int',
            'regex': r'^([01][0-9]|2[0-3])$'
            },
        MINUTE: {
            'type': 'int',
            'regex': r'^([0-5]?[0-9])$'
            },
        GUID: {
            'type': 'guid',
            'regex': r'^(\{{0,1}([0-9a-fA-F]){8}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){12}\}{0,1})$'
            },
        }
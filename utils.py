import datetime


def parse_timestamp(full_timestamp):
    """
    Split a timestamp in the format 2013-07-19 08:48:00.000187703
    into a datetime.datetime object and the original nanoseconds
    """
    timestamp, nanoseconds = full_timestamp.split('.')
    timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return timestamp, int(nanoseconds)


def parse_date(input_date):
    """
    Takes a date in the format 20130719 and returns the associated
    datetime.Date object
    """
    date = datetime.datetime.strptime(input_date, '%Y%m%d').date()
    return date

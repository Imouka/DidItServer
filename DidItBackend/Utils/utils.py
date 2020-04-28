import datetime

DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def datetime_to_pretty_date(myDict):
    for key in myDict:
        if isinstance(myDict[key], datetime.datetime):
            myDict[key] = myDict[key].strftime(DATE_FORMAT)

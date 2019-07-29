#!/usr/bin/env python
#
# 
# Nicholas Leader
# 7.29.2019
# POC Summary:
#
#    Leveraging Splunk SDK to query for bad search head logins 1 week from today.
#    Calling Python example script via Python 'subprocess.'
#
#    Outputting as a CSV to render nicely on the terminal - also makes for easy export / import.
#
#    Only grabbing the 'timestamp user status src' fields
#    'timestamp' is leveraging some special formatting to manipulate the built-in  '_time' field
#    Also noting that the escape character  /" was used to escape the double quote, as the Python interpreter thought
#    that was the closing quote.
#    'src' is renamed from the 'clientIP field
#
#    To search *remote* non-local search heads, you could just edit the '.splunkrc' file
#    This is the config file for the SDK.
#    You could also take host values as parameter to the script to dynamically update the config file.
#
#    References:
#        time parsing: https://docs.splunk.com/Documentation/Splunk/7.3.0/SearchReference/DateandTimeFunctions
#                      https://answers.splunk.com/answers/6971/how-to-format-time-field-in-results-email.html
#                      https://docs.splunk.com/Documentation/Splunk/7.3.0/SearchReference/Commontimeformatvariables
#        CSV output:   https://docs.splunk.com/Documentation/Splunk/7.3.0/SearchReference/Outputcsv
#
#        Rename field: https://docs.splunk.com/Documentation/Splunk/7.3.0/SearchReference/Rename
#
#       Qoute escaping (needed as 'strftime' require double quotes):
#                      https://stackoverflow.com/questions/6717435/how-to-escape-backslash-and-single-quote-or-double-quote-in-python
#
#       Subprocess calling with arguments:
#                      https://stackoverflow.com/questions/5788891/execute-a-file-with-arguments-in-python-shell

import subprocess
import sys
# subprocess is looking in the relative path - meaning this script would need to be located in the same path
# as the 'search.py'

# also noting that I'm passing the CLI parameters to the script file
subprocess.call([sys.executable, "./search.py",
"--output=csv",
"search index=_internal status=failure earliest=-7d | rename clientip as src | eval timestamp=strftime(_time, \"%m-%d-%Y %H:%M:%S\" ) | fields timestamp user status src | fields - _bkt _cd _kv _raw _serial _si _sourcetype _indextime _subsecond _time"])

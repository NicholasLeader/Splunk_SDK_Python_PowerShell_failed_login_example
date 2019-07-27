<# 
Nicholas Leader
7.27.2019
POC Summary:

    Leveraging Splunk SDK to query for bad search head logins 1 week from today.
    Calling Python via PowerShell - this could also be natively run in Python

    Outputting as a CSV to render nicely on the terminal - also makes for easy export / import.

    Only grabbing the 'timestamp user status src' fields
    'timestamp' is leveraging some special formatting to manipulate the built-in  '_time' field
    Also noting that the escape character  /" was used to escape the double quote, as the Python interpreter thought
    that was the closing quote.
    'src' is renamed from the 'clientIP field

    To search *remote* non-local search heads, you could just edit the '.splunkrc' file
    This is the config file for the SDK.
    You could also take host values as parameter to the script to dynamically update the config file.

    References:
        time parsing: https://docs.splunk.com/Documentation/Splunk/7.3.0/SearchReference/DateandTimeFunctions
                      https://answers.splunk.com/answers/6971/how-to-format-time-field-in-results-email.html
                      https://docs.splunk.com/Documentation/Splunk/7.3.0/SearchReference/Commontimeformatvariables
        CSV output:   https://docs.splunk.com/Documentation/Splunk/7.3.0/SearchReference/Outputcsv

        Rename field: https://docs.splunk.com/Documentation/Splunk/7.3.0/SearchReference/Rename

        Qoute escaping (needed as 'strftime' require double quotes):
                      https://stackoverflow.com/questions/6717435/how-to-escape-backslash-and-single-quote-or-double-quote-in-python
#>

#edit this to your path, where you downloaded the SDK
$path_to_python_script = "C:\Users\User\Documents\Scripts\splunk-sdk-python-1.6.6\examples\search.py"

# just writing a new line
 write-host ""
 python $path_to_python_script --output=csv "search index=_internal status=failure earliest=-7d | 
   rename clientip as src | 
    eval timestamp=strftime(_time, \""%m-%d-%Y %H:%M:%S\"" ) | 
    fields timestamp user status src | 
    fields - _bkt _cd _kv _raw _serial _si _sourcetype _indextime _subsecond _time"

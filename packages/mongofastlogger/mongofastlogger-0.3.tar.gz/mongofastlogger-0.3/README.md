# Logger
A simple and fask logging library that uses the power of mongodb to save and query logs (with built in cli)

## Cli
### search
`search <tag> <logger_name>`<br>
`python3 runner.py search Info`<br>
### clear
`clear <logger_name>`<br>
`python3 runner.py clear`<br>
### log
`log <tag> <message> <logger_name>`<br>
`python3 runner.py log Info "This is a log message"`<br>
### view
`view <logger_name>`<br>
`python3 runner.py view`<br>
### export
`export <filename> <logger_name>`<br>
`python3 runner.py export filename.log`<br>
### last
`last <metric> <amount> <logger_name>`<br>
`python3 runner.py last hours 3`<br>
### help
find commands<br>
`python3 runner.py`<br>
help with specific commands<br>
`python3 runner.py command --help`<br>
### other info
`<logger_name>` is optional and is `logs` by default


## Library
```py
from mongofastlogger.logger import LogViewer, Logger


# Make logger
logger = Logger()
# Log message with tag of "Something"
logger.log("Something", "This is bad as well i guess but i dont actually know")
# Log message with tag of "Something" and display log in console
logger.log("Something", "This is a message", display=True)

# Make Viewer
viewer = LogViewer()
# Print all logs
viewer.view_log()

# Search logs that have the tag "Something"
viewer.search_logs_by_tag("Something")
# Search logs in the last 3 days
viewer.check_by_time("days", 3)
# Export logs to example.log
viewer.export_log("example.log")

print("Production")

# Make logger with name
production_logger = Logger("Production")
production_logger.log("Error", "Critical error in production")

# Make viewer with name
production_viewer = LogViewer("Production")
production_viewer.view_log()
```

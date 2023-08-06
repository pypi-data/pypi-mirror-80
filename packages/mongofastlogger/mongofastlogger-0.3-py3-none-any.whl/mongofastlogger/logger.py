from inspect import currentframe, getframeinfo
from pymongo import MongoClient
from datetime import datetime
from termcolor import colored
import arrow


class Database:
    def __init__(self, name: str, location: str = "localhost", port: int = 27017):
        """Set default location and port"""
        self.location = location
        self.port = port
        self.collection_name = name
        self.connect()

    def connect(self):
        """Nake client, database, and collection"""
        self.client = MongoClient(self.location, self.port)
        self.database = self.client.logging_test_db
        self.collection = self.database[self.collection_name]


class Logger:
    def __init__(self, collection: str = "logs"):
        """Setup database"""
        self.db = Database(collection)

    def time(self):
        """Get data and time"""
        return datetime.utcnow()

    def log(self, tag: str, message: str, display: bool = False):
        """Add item to log"""
        cf = currentframe()
        linenum = cf.f_back.f_lineno
        filename = getframeinfo(cf.f_back).filename
        # Make document with time, tag, and message
        document = {
            "tag": tag,
            "time": self.time(),
            "message": message,
            "line": linenum,
            "file": filename
        }
        # Insert doc into collection
        self.db.collection.insert_one(document)
        if display:
            print(self.display_logged_message(tag, message))

    def display_logged_message(self, tag: str, message: str):
        ctag = colored(tag, 'yellow')
        return f"Logged: {ctag} {message}"


class LogViewer:
    def __init__(self, collection: str = "logs"):
        """Setup database"""
        self.db = Database(collection)

    def generate_log_line(self, document: dict, color: bool = False):
        """Make log view"""
        # Gets filename of logged file
        filename = document["file"]
        # Gets line number of log
        linenum = document["line"]
        # Get message
        message = document["message"]
        # Get time and convert it to arrow
        time = arrow.get(document['time'])
        # Get time with full format
        full = time.format('HH:mm:ss MM-DD-YY')
        # Return items with color if color is selected
        if color:
            tag = colored(document["tag"], "yellow")
            short = colored(time.humanize(), "green")
            location = colored(f"{filename}::{linenum}", 'blue')
        else:
            # Returns items without colors
            tag = document["tag"]
            short = time.humanize()
            location = f"{filename}::{linenum}"
        # Return string in readable format
        return f"{tag}\t{full} {location} {short} {message}"

    def check_by_time(self, metric: str, amount: int):
        """Check item by time"""
        print(f"Viewing logs in the last {amount} {metric}")
        now = arrow.utcnow()
        if metric == "minutes":
            then = now.shift(minutes=-amount)
        elif metric == "hours":
            then = now.shift(hours=-amount)
        elif metric == "days":
            then = now.shift(days=-amount)
        logs = self.db.collection.find({})
        for log in logs:
            if then < arrow.get(log["time"]):
                print(self.generate_log_line(log, True))

    def search_logs_by_tag(self, tag: str):
        """Search log by tag name"""
        logs = self.db.collection.find({"tag": tag})
        print(f"Logs with tag: {tag}")
        for log in logs:
            print(self.generate_log_line(log, True))

    def clear_data(self, ask=True):
        """Clear data"""
        if ask:
            clear = input("Clear all logs? [Y/n]: ")
            if clear.upper() == "Y":
                self.db.database.drop_collection(self.db.collection)
                print("All logs cleared")
            else:
                print("No data cleared")
        else:
            self.db.database.drop_collection(self.db.collection)

    def export_log(self, filename: str):
        """Export log to file"""
        with open(filename, 'w') as file:
            for x in self.db.collection.find({}):
                # Write lines of will without color
                file.write(self.generate_log_line(x) + "\n")
        print(f"File written to {filename}")

    def view_log(self):
        """View each log item"""
        for x in self.db.collection.find({}):
            # Printes lines with color
            print(self.generate_log_line(x, True))

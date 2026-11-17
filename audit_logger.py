
from datetime import datetime


class AuditLogger:
    def __init__(self):
        self.file_path = "audit.log"

    def log_event(self, username, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.file_path, "a") as file:
            file.write(f"[{timestamp}] {username}: {action}\n")

    def get_recent_logs(self, limit=10):
        try:
            with open(self.file_path, "r") as file:
                logs = file.readlines()
                return logs[-limit:]
        except FileNotFoundError:
            return []

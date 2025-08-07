import requests
import smtplib
import json
import statistics
from datetime import datetime, timedelta
from collections import defaultdict


### --- 1. Google Nest API Client ---
class NestAPIClient:
    def __init__(self, credentials: dict):
        self.client_id = credentials.get("client_id")
        self.client_secret = credentials.get("client_secret")
        self.project_id = credentials.get("project_id")
        self.refresh_token = credentials.get("refresh_token")
        self.access_token = None
        self.api_base = "https://smartdevicemanagement.googleapis.com/v1"

    def authenticate(self):
        """Exchange refresh token for an access token."""
        token_url = "https://www.googleapis.com/oauth2/v4/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
        }
        resp = requests.post(token_url, data=data)
        resp.raise_for_status()
        self.access_token = resp.json()["access_token"]

    def fetch_events(
        self, device_id: str, start_time: datetime, end_time: datetime
    ) -> list:
        """Retrieve historical events within a time range."""
        if not self.access_token:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        url = f"{self.api_base}/enterprises/{self.project_id}/devices/{device_id}:listEvents"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "startTime": start_time.isoformat() + "Z",
            "endTime": end_time.isoformat() + "Z",
        }
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        return [
            Event(
                ev.get("type"),
                datetime.fromisoformat(ev.get("timestamp").replace("Z", "")),
                ev,
            )
            for ev in data.get("events", [])
        ]


### --- 2. Event Data Model ---
class Event:
    def __init__(self, event_type: str, timestamp: datetime, details: dict = None):
        self.event_type = event_type
        self.timestamp = timestamp
        self.details = details or {}

    def __repr__(self):
        return f"<Event {self.event_type} @ {self.timestamp}>"


### --- 3. Analytics & Anomaly Detection ---
class EventAnalytics:
    def __init__(self, events: list):
        self.events = events
        self.events_by_day = defaultdict(list)
        for event in events:
            self.events_by_day[event.timestamp.date()].append(event)

    def summarize_events(self) -> dict:
        """Compute daily counts of each event type."""
        summary = {}
        for day, events in self.events_by_day.items():
            day_counts = defaultdict(int)
            for ev in events:
                day_counts[ev.event_type] += 1
            summary[day.strftime("%Y-%m-%d")] = dict(day_counts)
        return summary

    def detect_anomalies(self) -> list:
        """Identify abnormal activity levels and night events."""
        summary = self.summarize_events()
        anomalies = []
        daily_counts = [sum(day.values()) for day in summary.values()]
        avg, sd = (
            (statistics.mean(daily_counts), statistics.pstdev(daily_counts))
            if daily_counts
            else (0, 0)
        )
        high_threshold, low_threshold = avg + 2 * sd, max(0, avg - 2 * sd)

        for day, events in self.events_by_day.items():
            total = len(events)
            if total > high_threshold:
                anomalies.append(
                    f"High activity on {day}: {total} events (normal ~{avg:.1f})"
                )
            if total < low_threshold:
                anomalies.append(
                    f"Low activity on {day}: only {total} events (normal ~{avg:.1f})"
                )
            if any(ev.timestamp.hour < 5 for ev in events):
                anomalies.append(f"Night event detected on {day}")

        return anomalies

    def print_report(self):
        """Print event statistics."""
        summary = self.summarize_events()
        print("Event Summary by Day:")
        for day, counts in summary.items():
            print(f"  {day}: {counts}")
        anomalies = self.detect_anomalies()
        if anomalies:
            print("\nAnomalies Detected:")
            for a in anomalies:
                print(f"  - {a}")


### --- 4. Alerting System ---
class AlertManager:
    def __init__(self, config: dict):
        self.config = config

    def send_email(self, subject: str, body: str):
        """Send an email notification."""
        cfg = self.config.get("email", {})
        if not cfg.get("enabled"):
            return
        try:
            with smtplib.SMTP(cfg["smtp_server"], 587) as server:
                server.starttls()
                server.login(cfg["from"], cfg["password"])
                server.sendmail(cfg["from"], cfg["to"], f"Subject: {subject}\n\n{body}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def send_alerts(self, anomalies: list):
        """Send alerts if anomalies are found."""
        if not anomalies:
            return
        subject = "[Nest Monitor] Anomaly Alert"
        body = "Detected anomalies:\n" + "\n".join(anomalies)
        self.send_email(subject, body)


### --- 5. Main Execution ---
if __name__ == "__main__":
    # Load Google API Credentials
    with open("nest_credentials.json") as f:
        credentials = json.load(f)

    # Setup and Authenticate API Client
    client = NestAPIClient(credentials)
    client.authenticate()

    # Define time range (default 7 days)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=7)
    device_id = "YOUR_DEVICE_ID"  # Replace with actual Nest device ID

    # Fetch events
    events = client.fetch_events(device_id, start_time, end_time)
    print(f"Collected {len(events)} events.")

    # Analyze Data
    analytics = EventAnalytics(events)
    analytics.print_report()
    anomalies = analytics.detect_anomalies()

    # Alert Configuration
    alert_config = {
        "email": {
            "enabled": True,
            "to": "your_email@example.com",
            "smtp_server": "smtp.gmail.com",
            "from": "your_gmail@gmail.com",
            "password": "your_app_password",
        }
    }

    # Send Alerts
    alerts = AlertManager(alert_config)
    alerts.send_alerts(anomalies)

# ========================
# dashboard/dashboard.py
# ========================

import dash
from dash import dcc, html
import plotly.graph_objs as go
from influxdb_client import InfluxDBClient
import pytz
import traceback
from dash.dependencies import Output, Input

# InfluxDB connection configuration — replace with your actual details
INFLUX_URL = "http://localhost:8086"          # Your InfluxDB URL
INFLUX_TOKEN = "4KF2sbhzwP0usTtl9oUYJd5z7z979RNWQJnw7JepJShfbyr4NDtqTf4ebDlUVs-FVFRXy9KAZrVlorGY85r6NQ=="  # Your token
INFLUX_ORG = "ABC"                            # Your organization name
INFLUX_BUCKET = "AlertsMonitoring"            # Your bucket name

# Initialize InfluxDB client and query API
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()

# Set your local timezone here for display (optional)
LOCAL_TZ = pytz.timezone("America/New_York")  # Change as needed

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("System Resource Monitoring (InfluxDB)"),
    dcc.Graph(id='live-graph'),
    html.Div(
        id='alert-messages',
        style={
            'whiteSpace': 'pre-line',
            'color': 'red',
            'marginTop': '20px',
            'fontWeight': 'bold',
            'fontSize': '16px',
            'border': '1px solid red',
            'padding': '10px',
            'borderRadius': '5px',
            'backgroundColor': '#ffe6e6'
        }
    ),
    dcc.Interval(id='interval', interval=2000, n_intervals=0),  # Update every 2 seconds
])


@app.callback(
    [Output('live-graph', 'figure'),
     Output('alert-messages', 'children')],
    [Input('interval', 'n_intervals')]
)
def update_dashboard(n):
    print(f"Callback triggered, n_intervals = {n}")

    flux_query_metrics = f'''
    from(bucket:"{INFLUX_BUCKET}")
      |> range(start: -10m)
      |> filter(fn: (r) => r._measurement == "system_metrics")
      |> filter(fn: (r) => r._field == "cpu_percent" or r._field == "memory_percent" or r._field == "disk_percent")
      |> aggregateWindow(every: 10s, fn: mean, createEmpty: false)
      |> yield(name: "mean")
    '''

    flux_query_alerts = f'''
    from(bucket:"{INFLUX_BUCKET}")
      |> range(start: -30m)
      |> filter(fn: (r) => r._measurement == "alerts")
      |> sort(columns: ["_time"], desc: true)
      |> limit(n: 10)
    '''

    try:
        # Query system metrics
        tables_metrics = query_api.query(flux_query_metrics)
        data_by_time = {}

        for table in tables_metrics:
            for record in table.records:
                time_val = record.get_time()
                local_time = time_val.astimezone(LOCAL_TZ)
                if local_time not in data_by_time:
                    data_by_time[local_time] = {"cpu_percent": None, "memory_percent": None, "disk_percent": None}
                data_by_time[local_time][record.get_field()] = record.get_value()

        sorted_times = sorted(data_by_time.keys())
        timestamps = list(sorted_times)
        cpu_data = [data_by_time[t]["cpu_percent"] or 0 for t in sorted_times]
        memory_data = [data_by_time[t]["memory_percent"] or 0 for t in sorted_times]
        disk_data = [data_by_time[t]["disk_percent"] or 0 for t in sorted_times]

        if not timestamps:
            graph_fig = {
                'data': [],
                'layout': go.Layout(
                    title='No data available in InfluxDB for the selected range',
                    xaxis=dict(title='Time'),
                    yaxis=dict(title='Usage %'),
                )
            }
        else:
            graph_fig = {
                'data': [
                    go.Scatter(x=timestamps, y=cpu_data, name='CPU Usage (%)', mode='lines+markers'),
                    go.Scatter(x=timestamps, y=memory_data, name='Memory Usage (%)', mode='lines+markers'),
                    go.Scatter(x=timestamps, y=disk_data, name='Disk Usage (%)', mode='lines+markers'),
                ],
                'layout': go.Layout(
                    title='System Metrics (InfluxDB)',
                    xaxis=dict(title='Time'),
                    yaxis=dict(title='Usage Percentage', range=[0, 100]),
                    legend=dict(x=0, y=1)
                )
            }

        # Query recent alerts
        tables_alerts = query_api.query(flux_query_alerts)
        alerts = []
        for table in tables_alerts:
            for record in table.records:
                alert_time = record.get_time().astimezone(LOCAL_TZ).strftime("%Y-%m-%d %H:%M:%S")
                # Use `message` field or fallback to record value
                message = record.values.get("message") or record.get_value()
                alerts.append(f"{alert_time}: {message}")

        alerts_display = "\n".join(alerts) if alerts else "No recent alerts."

        return graph_fig, alerts_display

    except Exception as e:
        print(f"Error querying InfluxDB: {e}\n{traceback.format_exc()}")

        error_fig = {
            'data': [],
            'layout': go.Layout(
                title='Error querying InfluxDB',
                xaxis=dict(title='Time'),
                yaxis=dict(title='Usage %'),
            )
        }
        error_alert = "Error querying InfluxDB for alerts."

        return error_fig, error_alert


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

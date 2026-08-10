from prometheus_client import Counter, Histogram, Info

# Define metrics
optimization_requests_total = Counter(
    "optimization_requests_total", 
    "Total number of optimization requests"
)

optimization_processing_seconds = Histogram(
    "optimization_processing_seconds", 
    "Time spent processing optimization requests"
)

app_info = Info("app_version", "Application version info")
app_info.info({'version': '1.0.0', 'environment': 'production'})

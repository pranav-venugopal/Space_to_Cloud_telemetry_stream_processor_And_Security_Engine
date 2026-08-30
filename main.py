from fastapi import FastAPI, Response 
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import random
import time

app = FastAPI()

#these three lines create metrics , once when the apps starts.
#counter(name,description) - name must be unique, desc should show up.
TELEMETRY_INGEST_COUNT = Counter(
    'satellite_telemetry_ingested',
    'Total ingested satellite telemetry frames'
)
BATTERY_VOLTAGE_GAUGE = Gauge(
    'satellite_battery_voltage_volts',
    'Current satellite battery voltage level'
)
SIGNAL_NOISE_RATIO_GAUGE = Gauge(
    'satellite_snr_db',
    'Signal to Noise Ratio in dB'
)

@app.get("/")
def read_root():
    return{"messages":"Hello, satellite ground station!"}

#this is called by Kubernetes and load balancers call this repeatedly to check if the containers are alive.
@app.get("/health")
def health_check():
    return{"status": "HEALTHY", "ground_station": "HYD-GS-01"}

@app.post("/api/v1/telemetry")
def ingest_telemetry():
    #Sensor reading form the satellite
    snr = round(random.uniform(12.5, 28.4), 2) #Sigal-to-noise ratio
    voltage = round(random.uniform(28.0, 34.2), 2) #battery Voltage

    #adds one to the counter .inc()-this function.
    TELEMETRY_INGEST_COUNT.inc()

    #.set(__) overwrites gauges with new current value of voltage and snr.
    #unlike counter, this can go up or down.
    BATTERY_VOLTAGE_GAUGE.set(voltage)
    SIGNAL_NOISE_RATIO_GAUGE.set(snr)
    
    return{
        "Status": "PROCESSED",
        "Satellite_Id": "BluePenguin-07",
        "Snr_db": snr,
        "Battery_Voltage": voltage,
        "timestamps":time.time()
    }

#the endpoint prometheus and garfana will poll from 
@app.get("/metrics")
def metrics():
    return Response(content= generate_latest(), media_type=CONTENT_TYPE_LATEST) #generate_latest formats all counters and gauges to plain-text.
    #this is what prometheus expects.
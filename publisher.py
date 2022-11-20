import psutil
from time import sleep
from datetime import datetime
import json
import paho.mqtt.publish as publish

# MQTT Settings
MQTT_Broker = "hairdresser.cloudmqtt.com"
MQTT_Port = 17214
USERNAME = "ixyzuhmh"
PASSWORD = "XNfCz_qhTNOi"
SAMPLERATE = 10

# initial network bytes stats
initTimestamp = datetime.utcnow()
totalBytesInitOffset = psutil.net_io_counters()
recvBytesInitOffset = totalBytesInitOffset.bytes_recv
sentBytesInitOffset = totalBytesInitOffset.bytes_sent

def cpuInfo():
    # let's print CPU information
    return psutil.cpu_percent()


def memoryInfo():
    # Memory Information
    swap = psutil.swap_memory()
    return swap.percent


def netStats():
    global recvBytesInitOffset, sentBytesInitOffset, initTimestamp
    # scale bytes to Megabytes
    scale = 1000000
    measurementTimestamp = datetime.utcnow()
    totalBytesMeasured = psutil.net_io_counters()
    recvBytes = totalBytesMeasured.bytes_recv
    sentBytes = totalBytesMeasured.bytes_sent

    if recvBytes > recvBytesInitOffset:
        recvMBytesDelta = (recvBytes - recvBytesInitOffset)/scale
        recvBytesInitOffset = recvBytes
    else:
        recvMBytesDelta = 0

    if sentBytes > sentBytesInitOffset:
        sentMBytesDelta = (sentBytes - sentBytesInitOffset)/scale
        sentBytesInitOffset = sentBytes
    else:
        sentMBytesDelta = 0

    timeDelta = measurementTimestamp - initTimestamp
    initTimestamp = measurementTimestamp
    timeElapsed = timeDelta.seconds + timeDelta.microseconds/1E6
    # 1M egabyte = 8 Megabits
    downloadBandwidth = recvMBytesDelta * 8 / timeElapsed
    uploadBandwidth = sentMBytesDelta * 8 / timeElapsed
    return downloadBandwidth, uploadBandwidth


def publishOnTopic(topic, data):
    publish.single(topic,
                   data,
                   hostname=MQTT_Broker,
                   port=MQTT_Port,
                   auth={'username': USERNAME, 'password': PASSWORD})


while True:
    timestamp = str(datetime.utcnow().replace(microsecond=0))
    ram = json.dumps({"val": memoryInfo(), "timestamp": timestamp})
    cpu = json.dumps({"val": cpuInfo(), "timestamp": timestamp})
    DownloadBandwidth, UploadBandwidth = netStats()
    netDownloadBandwidth = json.dumps({"val": DownloadBandwidth, "timestamp": timestamp})
    netUploadBandwidth = json.dumps({"val": UploadBandwidth, "timestamp": timestamp})
    publishOnTopic("laptop/stats/ram", ram)
    publishOnTopic("laptop/stats/cpu", cpu)
    publishOnTopic("laptop/stats/netDownloadBandwidth", netDownloadBandwidth)
    publishOnTopic("laptop/stats/netUploadBandwidth", netUploadBandwidth)
    sleep(SAMPLERATE)

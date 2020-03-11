cam_1 = 'rtsp://dsoft:Dsoft@321@113.176.195.116:554/ch1/main/av_stream'
cam_2 = 'rtsp://dsoft:Dsoft@321@113.176.195.116:555/ch1/main/av_stream'
cam_3 = 'rtsp://dsoft:Dsoft@321@192.168.2.6:554/ch1/main/av_stream'
cam_4 = 'rtsp://dsoft:Dsoft@321@192.168.2.7:554/ch1/main/av_stream'
cam_5 = 'rtsp://dsoft:Dsoft@321@192.168.2.8:554/ch1/main/av_stream'
API_HOST = '192.168.4.3'

API_PORT = 5000

timeline = [8,9,10,11,12,13,14,15,16,17]

AI_TRIGGER_START_FLASK = 'http://' + API_HOST + ':' + str(API_PORT) + '/started'
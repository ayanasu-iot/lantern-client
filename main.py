# _*_ encoding:utf-8 _*_
import requests
import urllib
import json
import time
import threading
import picamera
import subprocess

imgFaceapi = 'my_picture.jpg'
urlFaceapi = 'https://ayanasuface.cognitiveservices.azure.com/face/v1.0/detect'
keyFaceapi = 'abd17f24d6404cd7bf952ce85b49d301'
#keyFaceapi = '2f75113d03dc4f6fb7e35f9d6f8d2294'
retFaceapi = 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'

def useFaceapi(url,key,ret,image):
	headers ={
			'Content-Type':'application/octet-stream',
			'Ocp-Apim-Subscription-Key': key,
			'cache-control':'no-cache',
	}
	params = {
			'returnFaceId':'true',
			'returnFaceLandmarks':'false',
			'returnFaceAttributes': ret,
	}
	data = open(image, 'rb').read()

	try:
		jsnResponse = requests.post(url ,headers=headers, params=params, data=data)
		print(jsnResponse.status_code)
		if(jsnResponse.status_code != 200):
			jsnResponse = []
		else:
			jsnResponse = jsnResponse.json()
	except requests.exceptions.RequestException as e:
		jsnResponse = []

	return jsnResponse

def testFaceApi():
	#imgFaceapi = 'my_picture.jpg'
	#urlFaceapi = 'https://ayanasuproject.cognitiveservices.azure.com/face/v1.0/detect'
	#keyFaceapi = '6133806d1c5944bfa45e2e4fdd7445a3'
	#retFaceapi = 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'

	resFaceapi = useFaceapi(urlFaceapi,keyFaceapi,retFaceapi,imgFaceapi)
	#print(resFaceapi)
	marte = range(len(resFaceapi))
	happiness=0
	disgust=0
	surprise=0
	anger=0
	contempt=0
	fear=0
	sadness=0
	neutral=0
	for num in marte:
		happiness += resFaceapi[num]["faceAttributes"]["emotion"]["happiness"]
		disgust += resFaceapi[num]["faceAttributes"]["emotion"]["disgust"]
		surprise += resFaceapi[num]["faceAttributes"]["emotion"]["surprise"]
		disgust += resFaceapi[num]["faceAttributes"]["emotion"]["anger"]
		disgust += resFaceapi[num]["faceAttributes"]["emotion"]["contempt"]
		disgust += resFaceapi[num]["faceAttributes"]["emotion"]["fear"]
		sadness += resFaceapi[num]["faceAttributes"]["emotion"]["sadness"]
		neutral += resFaceapi[num]["faceAttributes"]["emotion"]["neutral"]
	numenume=[happiness,disgust,surprise,sadness,neutral]
	return numenume.index(max(numenume))

def takePicture():
	with picamera.PiCamera() as camera:
		camera.resolution = (1024, 768)
		camera.capture(imgFaceapi)

def playAnimation(result):
	if result == 0:
		print("happiness")
		subprocess.Popen("./scripts/happiness.sh", cwd = r"/home/pi/Ayanasu/")
	elif result == 1:
		print("disgust")
		subprocess.Popen("./scripts/disgust.sh", cwd = r"/home/pi/Ayanasu/")
	elif result == 2:
		print("surprise")
		subprocess.Popen("./scripts/surprise.sh", cwd = r"/home/pi/Ayanasu/")
	elif result == 3:
		print("sadness")
		subprocess.Popen("./scripts/sadness.sh", cwd = r"/home/pi/Ayanasu/")
	elif result == 4:
		print("neutral")
		subprocess.Popen("./scripts/neutral.sh", cwd = r"/home/pi/Ayanasu/")

def main():
	while True:
		takePicture()
		result = testFaceApi()
		playAnimation(result)
		print("Loop")
		time.sleep(30)

if __name__ == "__main__":
	main()


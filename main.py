# _*_ encoding:utf-8 _*_
import requests
import time
import picamera
import settings
import subprocess

imgFaceapi = 'my_picture.jpg'
urlFaceapi = settings.URI
keyFaceapi = settings.KEY
retFaceapi = 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,' \
             'noise '


def useFaceapi(url, key, ret, image):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': key,
        'cache-control': 'no-cache',
    }
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': ret,
    }
    data = open(image, 'rb').read()

    try:
        json_response = requests.post(url, headers=headers, params=params, data=data)
        print(json_response.status_code)
        if (json_response.status_code != 200):
            json_response = []
        else:
            json_response = json_response.json()
    except requests.exceptions.RequestException as e:
        json_response = []

    return json_response


def testFaceApi():
    resFaceapi = useFaceapi(urlFaceapi, keyFaceapi, retFaceapi, imgFaceapi)
    marte = range(len(resFaceapi))
    happiness = 0
    disgust = 0
    surprise = 0
    anger = 0
    contempt = 0
    fear = 0
    sadness = 0
    neutral = 0
    for num in marte:
        happiness += resFaceapi[num]["faceAttributes"]["emotion"]["happiness"]
        disgust += resFaceapi[num]["faceAttributes"]["emotion"]["disgust"]
        surprise += resFaceapi[num]["faceAttributes"]["emotion"]["surprise"]
        anger += resFaceapi[num]["faceAttributes"]["emotion"]["anger"]
        contempt += resFaceapi[num]["faceAttributes"]["emotion"]["contempt"]
        fear += resFaceapi[num]["faceAttributes"]["emotion"]["fear"]
        sadness += resFaceapi[num]["faceAttributes"]["emotion"]["sadness"]
        neutral += resFaceapi[num]["faceAttributes"]["emotion"]["neutral"]
    numenume = [happiness, disgust, surprise, sadness, neutral]
    return numenume.index(max(numenume))


def takePicture():
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.capture(imgFaceapi)


def playAnimation(result):
    if result == 0:
        print("happiness")
        subprocess.Popen("./scripts/happiness.sh", cwd=r"/home/pi/Ayanasu/")
    elif result == 1:
        print("disgust")
        subprocess.Popen("./scripts/disgust.sh", cwd=r"/home/pi/Ayanasu/")
    elif result == 2:
        print("surprise")
        subprocess.Popen("./scripts/surprise.sh", cwd=r"/home/pi/Ayanasu/")
    elif result == 3:
        print("sadness")
        subprocess.Popen("./scripts/sadness.sh", cwd=r"/home/pi/Ayanasu/")
    elif result == 4:
        print("neutral")
        subprocess.Popen("./scripts/neutral.sh", cwd=r"/home/pi/Ayanasu/")


def main():
    while True:
        takePicture()
        result = testFaceApi()
        playAnimation(result)
        print("Loop")
        time.sleep(30)


if __name__ == "__main__":
    main()

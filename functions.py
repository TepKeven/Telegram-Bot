import requests
from gtts import gTTS
import json as Json_library


def non_callback_query(result, TOKEN) -> None:
    chat_id = result["message"]["chat"]["id"]
    if 'voice' in result["message"]:
        audioID = result["message"]["voice"]["file_id"]
        audioUrl = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={audioID}"
        request = requests.get(audioUrl)
        json2 = request.json()
        fileURL = f"https://api.telegram.org/file/bot{TOKEN}/{json2['result']['file_path']}"
        responseFile = requests.get(fileURL)
        audio_name = json2["result"]["file_unique_id"]
        open("audio/received/" + audio_name + ".oga", "wb").write(responseFile.content)
        replied = "Hello I am Bot"
        audioObject = gTTS(text=replied, lang='en')
        audioObject.save("audio/replied/" + audio_name + ".mp3")
        urlSendVoiceResponse = f"https://api.telegram.org/bot{TOKEN}/sendVoice?chat_id={chat_id}"
        requestSendAudio = requests.post(urlSendVoiceResponse, files={"voice": (audio_name + ".mp3", open("audio/replied/" + audio_name + ".mp3", 'rb'))})
        sendAudioJson = requestSendAudio.json()
        print(sendAudioJson)
    elif 'text' in result["message"]:
        message_received = result["message"]["text"]
        message_sent = "Hello I am bot"
        urlMessage = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message_sent}"
        requestSendMessage = requests.get(urlMessage)
        sendMessageJson = requestSendMessage.json()
        print(sendMessageJson)
    elif 'photo' in result["message"]:
        photo_resolution = []
        photoID = result["message"]["photo"][len(result["message"]["photo"]) - 1]["file_id"]
        for key, photo in enumerate(result["message"]["photo"]):
            photo_resolution.append([{"text": str(photo["width"]) + " X " + str(photo["height"]), "callback_data": str(key)}])

        reply_markup = Json_library.dumps({"inline_keyboard": photo_resolution})
        urlSendPhotoResponse = f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}&photo={photoID}&reply_markup={reply_markup}"
        requestSendPhoto = requests.get(urlSendPhotoResponse)
        sendPhotoJson = requestSendPhoto.json()
        print(sendPhotoJson)


def callback_query(result, TOKEN):
    chat_id = result["callback_query"]["message"]["chat"]["id"]
    if 'photo' in result["callback_query"]["message"]:
        chosen_photo = result["callback_query"]["data"]
        photoID = result["callback_query"]["message"]["photo"][int(chosen_photo)]["file_id"]
        photoUrl = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={photoID}"
        request = requests.get(photoUrl)
        json2 = request.json()
        fileURL = f"https://api.telegram.org/file/bot{TOKEN}/{json2['result']['file_path']}"
        responseFile = requests.get(fileURL)
        photo_name = json2["result"]["file_unique_id"]
        open("photo/" + photo_name + ".jpg", "wb").write(responseFile.content)
        urlSendPhotoResponse = f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}"
        requestSendPhoto = requests.post(urlSendPhotoResponse, files={"photo": (photo_name + ".jpg", open("photo/" + photo_name + ".jpg", 'rb'))})
        sendPhotoJson = requestSendPhoto.json()
        print(sendPhotoJson)

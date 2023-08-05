# ngChat Speech SDK

Please contact info@seasalt.ai if you have any questions.

## Speech-to-Text Example:

### Prerequisites
You will need a ngChat speech-to-text service url to run this example. Please contact info@seasalt.ai and apply for it.

### Install and import
To install ngChat Speech SDK:

```pip install ngchat-speech-sdk```

To import ngChat Speech SDK:

```import ngchat_speech.speech as speechsdk```


### Recognition
In the example below, we show how to recognize speech from an audio file. You can also apply recognition to an audio stream.

#### Speech Configuration
Use the following code to create SpeechConfig (contact info@seasalt.ai for the service host):
```
    speech_config = speechsdk.SpeechConfig(
        host="ws://NGCHAT_STT_SERVER/client/ws/speech"
    )
```

#### Audio Configuration
Use the following code to create AudioConfig.
```
    # Code commented out is an example for recognition on an audio stream.
    # audio_format = speechsdk.audio.AudioStreamFormat(
    #     samples_per_second=16000, bits_per_sample=16, channels=1)
    # audio_stream = speechsdk.audio.PushAudioInputStream(stream_format=audio_format)
    # audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)
    audio_config = speechsdk.audio.AudioConfig(filename="test.wav")
```

#### Recognizer initialization
SpeechRecognizer can be initialzed as follows:
```
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
```

#### Callbacks connection
SpeechRecognizer has 5 kinds of callbacks:
- Recognizing - called when recognition is in progress.
- Recognized - called when a single utterance is recognized.
- Canceled - called when a continuous recognition is interrupted.
- Session_started - called when a recognition session is started.
- Session_stopped - called when a recognition session is stopped.

To connect the callbacks:
```
    speech_recognizer.recognizing.connect(
        lambda evt: print(f"Recognizing: {evt.result.text}"))
    speech_recognizer.recognized.connect(
        lambda evt: print(f'Recognized: {evt.result.text}'))
    speech_recognizer.canceled.connect(
        lambda evt: print(f'Canceled: {evt}'))
    speech_recognizer.session_started.connect(
        lambda evt: print(f'Session_started: {evt}'))
    speech_recognizer.session_stopped.connect(
        lambda evt: print(f'Session_stopped: {evt}'))
```

#### Recognizing speech
Now it is ready to run SpeechRecognizer. SpeechRecognizer has two ways for speech recognition:
- Single-shot recognition - Performs recognition once. This is to recognize a single audio file. It stops recognition after a single utterance is recognized.
- Continuous recognition (async) - Asynchronously initiates continuous recognition on an audio stream. Recognition results are available through callback functions. To stop the continuous recognition, call stop_continuous_recognition_async().

```
    # Code commented out is for recognition on an audio stream.
    # speech_recognizer.start_continuous_recognition_async()
    speech_recognizer.recognize_once()
```

#### Putting everything together
Now, put everything together and run the example:


```
import speech as speechsdk
import audio as audio
import asyncio
import threading
import sys
import time

if __name__=="__main__":
    # this is an example to show how to use the ngChat Speech SDK to recognize once

    try:
        speech_config = speechsdk.SpeechConfig(
            host="ws://NGCHAT_STT_SERVER/client/ws/speech"
        )
        audio_config = audio.AudioConfig(filename="test.wav")
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )

        speech_recognizer.recognizing.connect(
            lambda evt: print(f"Recognizing: {evt.result.text}"))
        speech_recognizer.recognized.connect(
            lambda evt: print(f'Recognized: {evt.result.text}'))
        speech_recognizer.canceled.connect(
            lambda evt: print(f'Canceled: {evt}'))
        speech_recognizer.session_started.connect(
            lambda evt: print(f'Session_started: {evt}'))
        speech_recognizer.session_stopped.connect(
            lambda evt: print(f'Session_stopped: {evt}'))

        speech_recognizer.recognize_once()
        time.sleep(3)

    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Canceling tasks...")
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        sys.exit()
```

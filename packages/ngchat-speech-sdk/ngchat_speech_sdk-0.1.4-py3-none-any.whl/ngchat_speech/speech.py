"""
ngChat Speech SDK

Descriptions:
To connect to ngChat STT & TTS server to finish speech recognizing and synthesizing work.
"""


from typing import (
    Optional,
    Dict,
    Callable,
    Text
)
import websockets
from ws4py.client.threadedclient import WebSocketClient
import websocket
import urllib
import asyncio
from ngchat_speech import audio
import threading
import json
import warnings
from ngchat_speech import logger

import base64
import hashlib
import hmac
import os
import ssl
import time
import _thread as thread
import enum
import io
from ngchat_speech.utils import Wave

# used by SlothWebsocketParam
from wsgiref.handlers import format_date_time
from urllib.parse import urlencode
from datetime import datetime
from time import mktime

svc_logger = logger.get_SVCLogger(__name__)

SUPPORTED_AUDIO_FORMAT = {
    'riff-16khz-16bit-mono-pcm': {
        "frame_rate": 16000,
        "sample_width": 2,
        "channels": 1
    },
    'riff-22khz-16bit-mono-pcm': {
        "frame_rate": 22050,
        "sample_width": 2,
        "channels": 1
    }
}
SLOTH_WEBSOCKET_STATUS_LAST_FRAME = 2


class SpeechConfig():
    """ Setup speech arguments """

    def __init__(
        self,
        host: Text,
        speech_recognition_language: Optional[Text] = 'zh-TW',
        speech_synthesis_language: Optional[Text] = 'zh-TW',
        speech_synthesis_voice_name: Optional[Text] = 'zh-TW-Biaobei',
        speech_synthesis_output_format_id: Text = 'riff-16khz-16bit-mono-pcm',
    ):
        """Init speech arguments"""
        self.__host = host
        self.__speech_recognition_language = speech_recognition_language
        self.__speech_synthesis_language = speech_synthesis_language
        self.__speech_synthesis_voice_name = speech_synthesis_voice_name
        try:
            self.__output_format = SUPPORTED_AUDIO_FORMAT[speech_synthesis_output_format_id]
        except KeyError:
            raise ValueError("Unavailable format id")
        self.__speech_synthesis_output_format_id = speech_synthesis_output_format_id
        self.__speech_synthesis_format_label = 'X-SeasaltAI-OutputFormat'

    @property
    def host(self) -> Text:
        """Retrun host"""
        return self.__host

    @property
    def format_label(self) -> Text:
        """Return format label"""
        return self.__speech_synthesis_format_label

    @property
    def ngchat_format_label(self) -> Text:
        """Return format lable"""
        return self.__speech_synthesis_format_label

    @property
    def output_format(self) -> Dict:
        """Return output format"""
        return self.__output_format

    @property
    def speech_recognition_language(self) -> Optional[Text]:
        """Return recognition language"""
        return self.__speech_recognition_language

    @speech_recognition_language.setter
    def speech_recognition_language(self, language: Text) -> None:
        """Return recognition language"""
        self.__speech_recognition_language = language

    @property
    def speech_synthesis_language(self) -> Optional[Text]:
        """Return synthesis language"""
        return self.__speech_synthesis_language

    @speech_synthesis_language.setter
    def speech_synthesis_language(self, language: Text) -> None:
        """Set synthesis language"""
        self.__speech_synthesis_language = language

    @property
    def speech_synthesis_voice_name(self) -> Optional[Text]:
        """Return voice name"""
        return self.__speech_synthesis_voice_name

    @speech_synthesis_voice_name.setter
    def speech_synthesis_voice_name(self, voice_name: Text) -> None:
        """Set voice name"""
        self.__speech_synthesis_voice_name = voice_name

    @property
    def speech_synthesis_output_format_id(self) -> Text:
        """Return output format id"""
        return self.__speech_synthesis_output_format_id

    @speech_synthesis_output_format_id.setter
    def speech_synthesis_output_format_id(self, format_id: Text) -> None:
        """Set output format id"""
        try:
            self.__output_format = SUPPORTED_AUDIO_FORMAT[format_id]
        except KeyError:
            raise ValueError("Unavailable format id")
        self.__speech_synthesis_output_format_id = format_id

    def enable_audio_logging(self):
        """Enable audio loggin"""
        pass


class Recognizer(WebSocketClient):
    """Base class of recognizer"""

    def __init__(
        self,
        speech_config: SpeechConfig,
        audio_config: Optional[audio.AudioConfig] = None
    ):
        """Initialize speech recognizer"""
        # load speech_config
        self.__speech_config = speech_config
        self.__format_label = speech_config.format_label
        self.__host = speech_config.host
        self.__speech_recognition_language = speech_config.speech_recognition_language
        self.__speech_synthesis_language = speech_config.speech_synthesis_language
        self.__speech_synthesis_voice_name = speech_config.speech_synthesis_voice_name
        self.__output_format = speech_config.output_format
        self.__speech_synthesis_output_format_id = speech_config.speech_synthesis_output_format_id
        self.__recognizer_semaphore = threading.Semaphore(0)

        # load audio_config
        self.__input_stream = None
        self.__content_type = None
        self.__audio_config = audio_config
        self.__ws_uri = None
        self.__input_filename = None
        self.__recognize_once = False
        if audio_config is not None:
            if audio_config.stream is not None:
                self.__input_stream = audio_config.stream
                self.__content_type = urllib.parse.urlencode(
                    [
                        ("content-type", self.__input_stream.stream_format.content_type)
                    ]
                )
            elif audio_config.filename is not None:
                self.__input_filename = audio_config.filename
        if self.__content_type is not None:
            self.__ws_uri = f"{self.__host}?{self.__content_type}"
        else:
            self.__ws_uri = f"{self.__host}"
        self.is_running = False

        # create events
        self.__session_started_event = EventSignal()
        self.__session_stopped_event = EventSignal()
        self.__recognizing_event = EventSignal()
        self.__recognized_event = EventSignal()
        self.__canceled_event = EventSignal()
        self.session_id = None

        # init websocket client
        super().__init__(url=self.__ws_uri)

    def recognize_once(self):
        self.connect()
        if self.__input_filename is None:
            raise RuntimeError("No filename provided!")
        self.__recognize_once = True
        with open(self.__input_filename, "rb") as wav:
            while True:
                frame = 4000
                frame_data = wav.read(frame)
                if len(frame_data) == 0:
                    break
                self.send(frame_data, binary=True)
            self.send("EOS")

    def start_continuous_recognition_async(self):
        """Start continuous speech recognition in asynchronized way"""
        self.is_running = True
        self.connect()
        recognition_thread = threading.Thread(
            target=self.send_thread,
        )
        recognition_thread.daemon = True
        recognition_thread.start()

    def start_continuous_recognition(self):
        """Start continuous speech recognition in synchronized way"""
        self.start_continuous_recognition_async()
        self.__recognizer_semaphore.acquire()

    def thread_start_continuous_recognition_async(self):
        """
        Start a thread to start continuous recognition

        Deprecated: this is used for websockets, but since it has the issue of ws.send(), we changed to use ws4py.
        See coninuous_recognition_async for more info.
        """
        warnings.warn("Deprecated: websockets has the issue of sending data", DeprecationWarning)
        self.ngchat_stt_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.ngchat_stt_loop)
        try:
            self.ngchat_stt_loop.run_until_complete(
                self.await_continuous_recognition_async()
            )
        except Exception as e:
            svc_logger.error(
                f"Exception in thread_start_continuous_recognition_async: {e}"
            )
        finally:
            self.ngchat_stt_loop.close()

    async def await_continuous_recognition_async(self):
        """
        Wait results of continuous recognition

        Deprecated: this is used for websockets, but since it has the issue of ws.send(), we changed to use ws4py.
        See coninuous_recognition_async for more info.
        """
        warnings.warn("Deprecated: websockets has the issue of sending data", DeprecationWarning)
        await self.continuous_recognition_async()

    async def continuous_recognition_async(self):
        """
        Connect ngchat stt server by websocket

        Start a thread to send data to ngchat stt server
        Wait recognized results

        Deprecated: this is used for websockets, but when test, if started a new thread running coninuous_recognition_async
        in on_event_start in twilio_voice.py, from logs of ngchat stt server, ws.send() doesn't send package in real time.
        It sent the first package after about 2 seconds, then sent other packages continuously.
        After changed to use ws4py client, logs of stt server show sending packages is right. So we changed to use ws4py.

        """
        warnings.warn("Deprecated: websockets has the issue of sending data", DeprecationWarning)
        try:
            async with websockets.client.connect(self.__ws_uri) as ws:
                if self.__session_started_event.is_set:
                    # Not sure how to get session id on websocket starting
                    # the handshake response header is set in evt id
                    evt = {"id": f"{ws.response_headers}"}
                    evt_res = EventResults(evt)
                    self.__session_started_event.callback(evt_res)
                if self.__input_stream is not None:
                    thread_send = threading.Thread(target=self.send, args=(ws,))
                    thread_send.start()
                    await self.receive(ws)
            if self.__session_stopped_event.is_set:
                evt = {"session_id": self.session_id}
                evt_res = EventResults(evt)
                self.__session_stopped_event.callback(evt_res)
        except Exception as e:
            svc_logger.error(f"Exception in continuous_recognition_async: {e}")

    def opened(self):
        """Open websocket"""
        svc_logger.info("websocket opened")

    def closed(self, code, reason):
        """Close websocket"""
        svc_logger.info(f"Closed down: {code}, {reason}")

    def send_thread(self):
        """Send data to websocket"""
        while self.is_running:
            try:
                if self.__input_stream is not None:
                    buf = self.__input_stream.read_wait()
                    if buf is not None and len(buf) > 0:
                        self.send(buf, binary=True)
            except KeyboardInterrupt:
                self.stop_continuous_recognition_async()
        else:
            if self.__canceled_event.is_set:
                evt = {"session_id": self.session_id}
                evt_res = EventResults(evt)
                self.__canceled_event.callback(evt_res)
            self.send("EOS")
            self.close()

    def received_message(self, message) -> None:
        """Receive result from websocket"""
        try:
            evt = json.loads(str(message))
            if evt['status'] == 0:
                self.session_id = evt['id']
                if 'result' in evt:
                    if evt['result']['final']:
                        if self.__recognized_event.is_set:
                            evt_res = EventResults(evt)
                            self.__recognized_event.callback(evt_res)
                            if self.__recognize_once is True:
                                self.__recognize_once = False
                                self.close()
                    else:
                        if self.__recognizing_event.is_set:
                            evt_res = EventResults(evt)
                            self.__recognizing_event.callback(evt_res)
            else:
                errmsg = "Received error from server: "
                if 'message' in evt:
                    errmsg += f"{evt['message']}"
                raise RuntimeError(errmsg)
        except Exception as e:
            svc_logger.error(f"Exception in receive of continuous_recognition_async: {e}")
            self.stop_continuous_recognition_async()

    def stop_continuous_recognition_async(self):
        """Stop recognition"""
        self.is_running = False

    def stop_continuous_recognition(self):
        """Stop recognition"""
        self.is_running = False
        self.__recognizer_semaphore.release()

    @property
    def speech_config(self) -> SpeechConfig:
        """Return speech config"""
        return self.__speech_config

    @property
    def audio_config(self) -> Optional[audio.AudioConfig]:
        """Return audio config"""
        return self.__audio_config

    @property
    def format_label(self) -> Text:
        """Return format lable"""
        return self.__format_label

    @property
    def myhost(self) -> Text:
        """Return host"""
        return self.__host

    @property
    def speech_recognition_language(self) -> Optional[Text]:
        """Return recognition language"""
        return self.__speech_recognition_language

    @property
    def speech_synthesis_language(self) -> Optional[Text]:
        """Return synthesis language"""
        return self.__speech_synthesis_language

    @property
    def speech_synthesis_voice_name(self) -> Optional[Text]:
        """Return voice name"""
        return self.__speech_synthesis_voice_name

    @property
    def output_format(self) -> Dict:
        """Return output format"""
        return self.__output_format

    @property
    def speech_synthesis_output_format_id(self) -> Optional[Text]:
        """Return output format id"""
        return self.__speech_synthesis_output_format_id

    @property
    def session_started(self):
        """Return session started event"""
        return self.__session_started_event

    @property
    def session_stopped(self):
        """Return session stopped event"""
        return self.__session_stopped_event

    @property
    def speech_start_detected(self):
        """Return start detected"""
        raise NotImplementedError

    @property
    def speech_end_detected(self):
        """Return end detected"""
        raise NotImplementedError

    @property
    def recognizing(self):
        """Return Recognizing event"""
        return self.__recognizing_event

    @property
    def recognized(self):
        """Return recognized event"""
        return self.__recognized_event

    @property
    def canceled(self):
        """Return canceled event"""
        return self.__canceled_event


class SpeechRecognizer(Recognizer):
    """Speech recognize"""

    def __init__(
        self,
        speech_config: SpeechConfig,
        audio_config: Optional[audio.AudioConfig] = None
    ):
        """Initialze speech recognizer"""
        super().__init__(
            speech_config=speech_config,
            audio_config=audio_config
        )


class EventBase():
    """Base class for events"""

    def __init__(self):
        """Init event base"""
        self.callback = None
        self.__is_set = False

    def connect(self, callback: Callable):
        """
        Connects given callback function to the event signal, to be invoked when the
        event is signalled.
        """
        self.callback = callback
        self.__is_set = True

    @property
    def is_set(self):
        """Return if a callback is set"""
        return self.__is_set


class EventSignal(EventBase):
    """
    Clients can connect to the event signal to receive events, or disconnect from
    the event signal to stop receiving events.
    """

    def __init__(self):
        """Initialze the event"""
        super().__init__()


class EventResults():
    """Simulate MS SessionEventArgs class"""

    def __init__(self, evt):
        """Init event results"""
        self.status = None
        self.segment = None
        self.result = None
        self.session_id = None

        if "status" in evt:
            self.status = evt.get("status")
        if "segment" in evt:
            self.segment = evt.get("segment")
        if "result" in evt:
            self.result = Results(evt.get("result"))
        if "id" in evt:
            self.session_id = evt.get("id")

    def __str__(self):
        """Return event info"""
        return (
            f"status={self.status}, "
            f"segment={self.segment}, "
            f"result=({self.result}), "
            f"session_id={self.session_id}"
        )


class Results():
    """Simulate MS SpeechRecognitionEventArgs class"""

    def __init__(self, results):
        """Initialize results"""
        self.result_id = None
        self.text = None
        self.reason = None
        self.final = None

        if 'result_id' in results:
            self.result_id = None
        if 'hypotheses' in results:
            self.text = results['hypotheses'][0]['transcript']
        if 'reason' in results:
            self.reason = None
        if 'final' in results:
            self.final = results['final']

    def __str__(self):
        """Return result info"""
        return (
            f"result_id={self.result_id}, "
            f"text={self.text}, "
            f"reason={self.reason}, "
            f"final={self.final}"
        )


class ResultReason(enum.Enum):
    ResultReason_Canceled = 9
    ResultReason_SynthesizingAudioStarted = 10
    ResultReason_SynthesizingAudio = 11
    ResultReason_SynthesizingAudioCompleted = 12


class SpeechSynthesisResult():
    """
    Result of a speech synthesis operation.
    """

    def __init__(
            self,
            audio,
            reason,
            result_id=None,
            cancellation_details=None
    ):
        """
        Constructor for SpeechSynthesisResult.
        """
        self._cancellation_details = cancellation_details
        self._result_id = result_id
        self._reason = reason
        self._audio_data = audio

    @property
    def cancellation_details(self) -> str:
        """
        The reason why speech synthesis was cancelled.

        Returns `None` if there was no cancellation.
        """
        return self._cancellation_details

    @property
    def result_id(self) -> str:
        """
        Synthesis result unique ID.
        """
        return self._result_id

    @property
    def reason(self) -> ResultReason:
        """
        Synthesis reason.
        """
        return self._reason

    @property
    def audio_data(self) -> bytes:
        """
        The output audio data from the TTS.
        """
        return self._audio_data

    def __str__(self):
        return u'{}(result_id={}, reason={}, audio_length={})'.format(
            type(self).__name__, self._result_id, self._reason, len(self._audio_data))


class ResultFuture():
    """
    The result of an asynchronous operation.
    """
    def __init__(self, client):
        """
        constructor
        """
        self.__client = client

    def get(self) -> SpeechSynthesisResult:
        """
        Waits until the result is available, and returns it.
        """
        self.__client.semaphore.acquire()
        return self.__client.speech_synthesis_result


class SlothWebsocketParam(object):
    def __init__(self, app_id, api_key, api_secret, text):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.text = text

        self.common_args = {"app_id": self.app_id}
        self.business_args = {"aue": "raw", "auf": "audio/L16;rate=16000", "vcn": "xiaoyan", "tte": "utf8"}
        self.data = {"status": SLOTH_WEBSOCKET_STATUS_LAST_FRAME,
                     "text": str(base64.b64encode(self.text.encode('utf-8')), "UTF8")}

    def create_url(self, host_url):
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"

        signature_sha = hmac.new(self.api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key={self.api_key}, algorithm="hmac-sha256", headers="host date request-line", signature={signature_sha}'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        svc_logger.info(f'Sloth websocket: {authorization_origin.encode("utf-8")}')

        value = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }

        url = host_url + '?' + urlencode(value)
        svc_logger.info(f'Sloth websocket: url {url}')
        return url


class SlothWebsocketClient():
    def __init__(
            self,
            host,
            output_stream=None,
            output_filename=None
    ):
        websocket.enableTrace(False)
        self.__host = host
        ws = websocket.WebSocketApp("",
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        self.ws = ws
        self.ws.on_open = self.on_open
        self.__audio_buf = io.BytesIO()
        self.__running = True
        self.speech_synthesis_result = None
        self.semaphore = threading.Semaphore(0)
        self.__output_stream = output_stream
        self.__output_filename = output_filename

    def save_wav_file(self, audio_pcm, filename):
        audio = Wave(filename, 'wb')
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(22050)
        audio.writeframes(audio_pcm)
        audio.close()

    def speak_text(
            self,
            input_text: str):
        self.ws_param = SlothWebsocketParam(app_id='appid_001', api_key='appkey_001',
                                            api_secret='api_secret',
                                            text=input_text)
        ws_url = self.ws_param.create_url(host_url=self.__host)
        self.ws.url=ws_url
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        self.__audio_buf.seek(0)
        audio_data = self.__audio_buf.read()
        self.speech_synthesis_result = SpeechSynthesisResult(
            audio_data,
            ResultReason.ResultReason_SynthesizingAudioCompleted
        )
        if self.__output_stream is not None:
            self.__output_stream.write(audio_data)
        if self.__output_filename is not None:
            self.save_wav_file(audio_data, self.__output_filename)
        self.semaphore.release()
        return self.speech_synthesis_result

    def speak_text_async(self,
                         input_text: str):
        task_speak = threading.Thread(
            target = self.speak_text,
            args = (input_text,)
        )
        task_speak.daemon = True
        task_speak.start()
        return ResultFuture(self)

    def on_message(self, message):
        try:
            message = json.loads(message)
            code = message["code"]
            sid = message["sid"]
            audio = message["data"]["audio"]
            audio = base64.b64decode(audio)
            status = message["data"]["status"]
            if status == 2:
                self.__audio_buf.write(audio)
                self.ws.close()
                self.__running = False

                if self.synthesis_completed is not None:
                    if self.synthesis_completed.is_set is True:
                        self.synthesis_completed.callback()

                svc_logger.info("Sloth websocket: ws is closed")
            if code != 0:
                err_msg = message["message"]
                svc_logger.info(f"Sloth websocket: sid: {sid}; error: {err_msg}; code: {code}.")
            else:
                if self.__running is True:
                    self.__audio_buf.write(audio)

                    if self.synthesizing is not None:
                        if self.synthesizing.is_set is True:
                            self.synthesizing.callback()

        except Exception as e:
            svc_logger.error(f"Sloth websocket exception: {e}")

    def on_error(self, error):
        if self.synthesis_canceled is not None:
            if self.synthesis_canceled.is_set is True:
                self.synthesis_canceled.callback()
        svc_logger.error(f"Sloth websocket error: {error}")

    def on_close(self):
        svc_logger.info("Sloth websocket: closed.")

    def on_open(self):
        def run(*args):
            data = {"common": self.ws_param.common_args,
                    "business": self.ws_param.business_args,
                    "data": self.ws_param.data,
            }
            data = json.dumps(data)
            svc_logger.info("Sloth websocket: start sending text data.")
            self.ws.send(data)

        if self.synthesis_started is not None:
            if self.synthesis_started.is_set is True:
                self.synthesis_started.callback()

        thread.start_new_thread(run, ())


class SpeechSynthesizer(SlothWebsocketClient):
    """
    A speech synthesizer.

    :param speech_config: The config for the speech synthesizer
    :param audio_config: The config for the audio output.
        This parameter is optional.
        If it is not provided, the default speaker device will be used for audio output.
        If it is None, the output audio will be dropped.
        None can be used for scenarios like performance test.
    """
    def __init__(
            self,
            speech_config: SpeechConfig,
            audio_config: Optional[audio.AudioOutputConfig] = None
    ):
        """Initialize speech recognizer"""
        if not isinstance(speech_config, SpeechConfig):
            raise ValueError('speech_config must be a SpeechConfig instance')

        # load speech_config
        self.__speech_config = speech_config
        self.__format_label = speech_config.format_label
        self.__host = speech_config.host
        self.__speech_synthesis_language = speech_config.speech_synthesis_language
        self.__speech_synthesis_voice_name = speech_config.speech_synthesis_voice_name
        self.__output_format = speech_config.output_format
        self.__speech_synthesis_output_format_id = speech_config.speech_synthesis_output_format_id

        # load audio_output_config
        self.__output_stream = None
        self.__audio_config = audio_config
        self.__output_filename = None
        if audio_config is not None:
            if audio_config.stream is not None:
                self.__output_stream = audio_config.stream
            elif audio_config.filename is not None:
                self.__output_filename = audio_config.filename
        self.is_running = False

        # create events
        self.__synthesis_started_event = EventSignal()
        self.__synthesizing_event = EventSignal()
        self.__synthesis_completed_event = EventSignal()
        self.__synthesis_canceled_event = EventSignal()
        self.session_id = None

        # init sloth websocket client
        super().__init__(self.__host, self.__output_stream, self.__output_filename)

    def speak_text(self, text: str) -> SpeechSynthesisResult:
        """
        Performs synthesis on plain text in a blocking (synchronous) mode.

        :return: A SpeechSynthesisResult.
        """
        return super().speak_text(text)

    def speak_ssml(self, ssml: str) -> SpeechSynthesisResult:
        """
        Performs synthesis on ssml in a blocking (synchronous) mode.

        :return: A SpeechSynthesisResult.
        """
        raise NotImplementedError

    def speak_text_async(self, text: str) -> ResultFuture:
        """
        Performs synthesis on plain text in a non-blocking (asynchronous) mode.

        :return: A future with SpeechSynthesisResult.
        """
        return super().speak_text_async(text)

    def speak_ssml_async(self, ssml: str) -> ResultFuture:
        """
        Performs synthesis on ssml in a non-blocking (asynchronous) mode.

        :return: A future with SpeechSynthesisResult.
        """
        raise NotImplementedError

    def start_speaking_text(self, text: str) -> SpeechSynthesisResult:
        """
        Starts synthesis on plain text in a blocking (synchronous) mode.

        :return: A SpeechSynthesisResult.
        """
        raise NotImplementedError

    def start_speaking_ssml(self, ssml: str) -> SpeechSynthesisResult:
        """
        Starts synthesis on ssml in a blocking (synchronous) mode.

        :return: A SpeechSynthesisResult.
        """
        raise NotImplementedError

    def start_speaking_text_async(self, text: str) -> ResultFuture:
        """
        Starts synthesis on plain text in a non-blocking (asynchronous) mode.

        :return: A future with SpeechSynthesisResult.
        """
        raise NotImplementedError

    def start_speaking_ssml_async(self, ssml: str) -> ResultFuture:
        """
        Starts synthesis on ssml in a non-blocking (asynchronous) mode.

        :return: A future with SpeechSynthesisResult.
        """
        raise NotImplementedError

    @property
    def properties(self):
        """
        A collection of properties and their values defined for this SpeechSynthesizer.
        """
        raise NotImplementedError

    @property
    def authorization_token(self) -> str:
        """
        The authorization token that will be used for connecting to the service.

        .. note::
          The caller needs to ensure that the authorization token is valid. Before the
          authorization token expires, the caller needs to refresh it by calling this setter with a
          new valid token. Otherwise, the synthesizer will encounter errors while speech synthesis.
        """
        raise NotImplementedError

    @authorization_token.setter
    def authorization_token(self, authorization_token: str):
        raise NotImplementedError

    @property
    def synthesis_started(self) -> EventSignal:
        """
        Signal for events indicating synthesis has started.

        Callbacks connected to this signal will be called.
        """
        return self.__synthesis_started_event

    @property
    def synthesizing(self) -> EventSignal:
        """
        Signal for events indicating synthesis is ongoing.

        Callbacks connected to this signal will be called.
        """
        return self.__synthesizing_event

    @property
    def synthesis_completed(self) -> EventSignal:
        """
        Signal for events indicating synthesis has completed.

        Callbacks connected to this signal will be called.
        """
        return self.__synthesis_completed_event

    @property
    def synthesis_canceled(self) -> EventSignal:
        """
        Signal for events indicating synthesis has been canceled.

        Callbacks connected to this signal will be called.
        """
        return self.__synthesis_canceled_event

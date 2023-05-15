import wave
from multiprocessing import Queue, Process, set_start_method, get_context

from typing import ByteString, Union, Iterable

import numpy as np
import pyaudio  # sudo apt-get install portaudio19-dev  python3-pyaudio

from vannypi.inputmanagement.audiomanager.audio import Audio


class AudioRecorder:

    def __init__(self, main_seconds: int, post_incidentt_seconds: int, rate: int = 8000, chunk_length: int = 1024,
                 mq: Queue = None):
        self._audio_frames: Iterable[Union[ByteString, memoryview]] = []
        self._main_seconds: int = main_seconds
        self._post_incident_seconds: int = post_incidentt_seconds
        # self.audio_to_keep: List[np.ndarray] = []
        self._rate = rate
        self._chunk_length: int = chunk_length
        self._num_of_chunks_per_sec = self._rate / self._chunk_length
        self._mq = mq
        self._mode: int = 0
        self._files_count: int = 0
        self._waveFile = None

    def initialize(self):
        self.p = pyaudio.PyAudio()
        print("stree")
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=2,
                                  rate=self._rate,
                                  input=True,
                                  frames_per_buffer=self._chunk_length)

        print("audio init")

    def _change_mode(self):
        if not self._mq.empty():
            detected = self._mq.get_nowait()
            print("audio changing mode")
            return True
        return False

    def record_audio(self) -> None:
        recording_seconds = self._main_seconds
        while True:
            if len(self._audio_frames) >= self._num_of_chunks_per_sec * recording_seconds:
                self._audio_frames = self._audio_frames[1:]

            audio_frame = self.stream.read(self._chunk_length)
            self._audio_frames.append(audio_frame)

            if self._mode == 0 and self._change_mode():
                self.save_audio(mode=self._mode)

                recording_seconds = self._post_incident_seconds
                print("writing audio...")

            elif self._mode == 1 and len(
                    self._audio_frames) >= self._num_of_chunks_per_sec * self._post_incident_seconds:
                self.save_audio(mode=1)

    def save_audio(self, mode: int) -> None:
        if mode == 0:
            self._waveFile = wave.open('audio_capture_{}.wav'.format(self._files_count), 'wb')
            self._waveFile.setnchannels(2)
            self._waveFile.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            self._waveFile.setframerate(self._rate)

            self._waveFile.writeframes(b''.join(self._audio_frames))
            self._audio_frames: Iterable[Union[ByteString, memoryview]] = []
            self._mode = 1

        elif mode == 1:
            print("writing post")

            self._waveFile.writeframes(b''.join(self._audio_frames))
            self._waveFile.close()
            self._audio_frames: Iterable[Union[ByteString, memoryview]] = []
            self._mode = 0
            self._files_count += 1
            # maybe consume all of the queue in case there is issue


def _run(main_seconds: int, post_incidentt_seconds: int, rate: int = 8000, chunk_length: int = 1024, mq: Queue = None):
    audio_recorder = AudioRecorder(main_seconds=main_seconds,
                                   post_incidentt_seconds=post_incidentt_seconds,
                                   rate=rate, chunk_length=chunk_length, mq=mq)
    print("intit..")
    audio_recorder.initialize()
    print("initt done")
    audio_recorder.record_audio()
    audio_recorder.stream.stop_stream()
    audio_recorder.stream.close()
    audio_recorder.p.terminate()


def start_process(main_seconds: int, post_incidentt_seconds: int, rate: int = 8000, chunk_length: int = 1024,
                  mq: Queue = None):
    print("started audio recording ...")
    ctx = get_context('spawn')
    print(ctx)
    audio_process = ctx.Process(target=_run, args=(main_seconds, post_incidentt_seconds, rate, chunk_length, mq))
    audio_process.start()
    print("started audio recording ...")

import speech_recognition as sr
import threading
import keyboard  # Library for detecting key presses

class RealTimeVoiceToText:
    def __init__(self, mic_index=0):
        self.recognizer = sr.Recognizer()
        self.stop_listening = False
        self.mic_index = mic_index

    def listen_from_mic(self):
        with sr.Microphone(device_index=self.mic_index) as source:
            print("Adjusting for ambient noise... Please wait.")
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening... Press 'q' to stop.")
            
            while not self.stop_listening:
                try:
                    # Capture audio for a short period to minimize delay
                    audio = self.recognizer.listen(source, timeout=1)
                    text = self.recognizer.recognize_google(audio)
                    # Clear the previous line and print the new text
                    print(f"\r{text}", end='')
                except sr.UnknownValueError:
                    # Optional: Handle the case when speech is not recognized
                    pass
                except sr.RequestError:
                    print("\nSorry, there was an issue with the request to the speech recognition service.")
                    break
                except sr.WaitTimeoutError:
                    # Continue listening if timeout occurs
                    continue

    def stop(self):
        self.stop_listening = True

if __name__ == "__main__":
    # Replace 0 with the index of your desired microphone
    mic_index = 2
    rtvt = RealTimeVoiceToText(mic_index=mic_index)
    
    # Start the listening in a separate thread
    listening_thread = threading.Thread(target=rtvt.listen_from_mic)
    listening_thread.start()
    
    print("Press 'q' to stop.")
    while True:
        if keyboard.is_pressed('q'):
            rtvt.stop()
            listening_thread.join()
            print("\nStopped listening.")
            break

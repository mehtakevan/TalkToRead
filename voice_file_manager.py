import subprocess
import speech_recognition as sr

def listen_for_command():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()


    while True:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)


        try:
            command = recognizer.recognize_google(audio)
            print("Command:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
        except sr.RequestError:
            print("Sorry, I couldn't request results from the speech recognition service.")


def main():
    while True:
        command = listen_for_command()


if __name__ == "__main__":
    main()
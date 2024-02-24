import subprocess
import speech_recognition as sr
import pyautogui

current_file = None
opened_files = {}

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


def open_file(filename):
    global current_file
    try:
        if current_file:
            close_file(current_file)
        process = subprocess.Popen(["notepad.exe", filename])
        print("File opened successfully:", filename)
        current_file = filename
        opened_files[filename] = process  # Store the subprocess in opened_files dictionary
    except FileNotFoundError:
        print("File not found:", filename)


def close_file(filename=None):
    global current_file
    if filename is None:
        # If filename is not provided, close the currently opened file
        if current_file:
            pyautogui.hotkey('ctrl', 'w')  # Send Ctrl + W to close the current file in Notepad
            print("File closed successfully:", current_file)
            current_file = None
        else:
            print("No file is currently opened.")
    elif filename in opened_files:
        pyautogui.hotkey('ctrl', 'w')  # Send Ctrl + W to close the specified file in Notepad
        del opened_files[filename]
        print("File closed successfully:", filename)
        if current_file == filename:
            current_file = None
    else:
        print("File is not opened:", filename)


def scroll_up():
    pyautogui.press('pageup')  # Scroll up 3 steps (adjust as needed)


def scroll_down():
    pyautogui.press('pagedown') # Scroll down 3 steps (adjust as needed)


def stop_script():
    print("Stopping the script...")
    exit()


def main():
    while True:
        command = listen_for_command()

        if command.startswith("open"):
            filename = command.split(" ")[1] if len(command.split(" ")) > 1 else None
            if filename:
                filename = filename + ".txt" if not filename.endswith(".txt") else filename
                open_file(filename)
            else:
                print("Please provide a filename to open.")

        elif command.startswith("close"):
            close_file()

        elif command.startswith("scroll up"):
            scroll_up()

        elif command.startswith("scroll down"):
            scroll_down()

        elif command.startswith("stop"):
            stop_script()


if __name__ == "__main__":
    main()
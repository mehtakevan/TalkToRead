import subprocess
import speech_recognition as sr
import pyautogui
import pyttsx3
import PyPDF2
import fitz
import os

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



def read_file():
    global current_file
    if current_file:
        try:
            if current_file.lower().endswith(".pdf"):
                with open(current_file,"rb") as pdf:
                    reader = PyPDF2.PdfReader(pdf,strict=False)
                    pdf_text = []

                    for page in reader.pages:
                        content = page.extract_text()
                        tts = pyttsx3.init()
                        tts.say(content)
                        tts.runAndWait()
                    

            else:
                with open(current_file, "r") as file:
                    file_content = file.read()
                    print("Reading file content for", current_file)
                    tts = pyttsx3.init()
                    tts.say(file_content)
                    tts.runAndWait()
        except FileNotFoundError:
            print("File not found:", current_file)
    else:
        print("No file currently opened.")



def open_file(filename):
    global current_file
    global current_file
    try:
        if current_file:
            close_file(current_file)
        if filename.lower().endswith(".pdf"):
            document = fitz.open(filename)
            os.startfile(filename)
            print("PDF file opened successfully:", filename)
            current_file = filename
            opened_files[filename] = document
        else:
            process = subprocess.Popen(["notepad.exe", filename])
            print("File opened successfully:", filename)
            current_file = filename
            opened_files[filename] = process  # Store the subprocess in opened_files dictionary
    except FileNotFoundError:
        print("File not found:", filename)
  

def close_file():
    global current_file
    if current_file:
        save_file(current_file)
        pyautogui.hotkey('ctrl', 'w')  # Send Ctrl + W to close the current file in Notepad
        print("File closed successfully:", current_file)
        current_file = None
    else:
        print("No file is currently opened.")


def save_file(filename):
    pyautogui.hotkey('ctrl', 's')  # Send Ctrl + S to save the file in Notepad
    print("File saved successfully:", filename)


def delete_file(filename):
    try:
        os.remove(filename)
        print("File", filename, "deleted successfully.")
    except FileNotFoundError:
        print("File", filename, "not found.")


def rename_file(old_filename, new_filename):
    global current_file  # Declare current_file as global

    try:
        # Add .txt extension if not present in old filename
        old_filename = old_filename + ".txt" if not old_filename.endswith(".txt") else old_filename
        
        # Add .txt extension if not present in new filename
        new_filename = new_filename + ".txt" if not new_filename.endswith(".txt") else new_filename
        
        os.rename(old_filename, new_filename)
        print("File renamed successfully to:", new_filename)
        
        # Update current_file if it matches the old filename
        if current_file == old_filename:
            current_file = new_filename

    except FileNotFoundError:
        print("File not found:", old_filename)
    except FileExistsError:
        print("A file with the new name already exists:", new_filename)
    except Exception as e:
        print("An error occurred:", str(e))


def scroll_up():
    pyautogui.press('pageup')  # Scroll up 3 steps (adjust as needed)


def scroll_down():
    pyautogui.press('pagedown') # Scroll down 3 steps (adjust as needed)


def write_file(text):
    global current_file
    if current_file:
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write(text)  # Write the text to Notepad
        print("Text written to file:", text)
    else:
        print("No file currently opened.")


def append_file(text):
    global current_file
    if current_file:
        pyautogui.press('end')  # Move cursor to the end of the file
        pyautogui.write('\n' + text)  # Write the text to a new line in Notepad
        print("Text appended to file:", text)
    else:
        print("No file currently opened.")


def stop_script():
    close_file()
    print("Stopping the script...")
    exit()


def main():
    while True:
        command = listen_for_command()

        if command.startswith("open pdf"):
            filename = command.split(" ")[2] if len(command.split(" ")) > 2 else None
            if filename:
                filename = filename + ".pdf" if not filename.endswith(".pdf") else filename
                open_file(filename)
            else:
                print("Please provide a PDF filename to open.")
        
        elif command.startswith("open"):
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

        elif command.startswith("read"):
            read_file()
        
        elif command.startswith("write"):
            text = command.split(" ", 1)[1] if len(command.split(" ")) > 1 else None
            if text:
                write_file(text)
            else:
                print("Please provide text to write.")

        elif command.startswith("append"):
            text = command.split(" ", 1)[1] if len(command.split(" ")) > 1 else None
            if text:
                append_file(text)
            else:
                print("Please provide text to append.")

        elif command.startswith("delete"):
            filename = command.split(" ")[1] if len(command.split(" ")) > 1 else None
            if filename:
                filename = filename + ".txt" if not filename.endswith(".txt") else filename
                delete_file(filename)
            else:
                print("Please provide a filename to delete.")

        elif command.startswith("rename"):
            filenames = command.split(" ")[1:]  # Extract both old and new filenames
            if len(filenames) == 2:
                old_filename, new_filename = filenames
                old_filename = old_filename + ".txt" if not old_filename.endswith(".txt") else old_filename
                renamed_file = rename_file(old_filename, new_filename)
                if renamed_file:
                    if current_file == old_filename:
                        current_file = renamed_file
            else:
                print("Please provide both old and new filenames separated by a space.")


if __name__ == "__main__":
    main()

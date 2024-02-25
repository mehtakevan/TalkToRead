import subprocess
import speech_recognition as sr
import pyautogui
import pyttsx3
import PyPDF2
import fitz # pip install PyMuPDF
import os
import shutil
import sys
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"
SENTENCES_COUNT = 3  # Number of sentences in the summary
current_file = None
current_directory = os.getcwd()  # Get the current working directory

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
            print("Sorry, Please try again later.")


def create_file(filename):
    try:
        if not os.path.exists(filename):
            with open(filename, 'w'):
                print(filename, "created successfully.")
        else:
            print(filename, "already exists.")
    except Exception as e:
        print("error creating file.")

def rename_file(old_filename, new_filename):
    global current_file  # Declare current_file as global

    try:
        # Add .txt extension if not present in old filename
        old_filename = old_filename + ".txt" if not old_filename.endswith(".txt") else old_filename
        
        # Add .txt extension if not present in new filename
        new_filename = new_filename + ".txt" if not new_filename.endswith(".txt") else new_filename
        
        os.rename(old_filename, new_filename)
        print("file renamed successfully.")
        
        # Update current_file if it matches the old filename
        if current_file == old_filename:
            current_file = new_filename

    except FileNotFoundError:
        print(old_filename, "not found.")
    except FileExistsError:
        print(new_filename, "already exists.")
    except Exception as e:
        print("sorry, try again.")

def write_file(text):
    global current_file
    if current_file:
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write(text)  # Write the text to Notepad
        print("Text written to file.")
    else:
        print("no file currently opened.")

def append_file(text):
    global current_file
    if current_file:
        pyautogui.press('end')  # Move cursor to the end of the file
        pyautogui.write('\n' + text)  # Write the text to a new line in Notepad
        print("Text appended to file.")
    else:
        print("no file currently opened.")

def save_file(filename):
    pyautogui.hotkey('ctrl', 's')  # Send Ctrl + S to save the file in Notepad
    print("File saved successfully.")

def summarize_file():
    if current_file.endswith('.txt'):
        parser = PlaintextParser.from_file(current_file, Tokenizer(LANGUAGE))
    else:
        raise ValueError("Unsupported file format")

    stemmer = Stemmer(LANGUAGE)
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summary = []
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        summary.append(str(sentence))

    text = ' '.join(summary)
    print(text)
    tts = pyttsx3.init()
    tts.say(text)
    tts.runAndWait()


def open_file_pdf(filename):
    global current_file
    try:
        if current_file:
            close_any_file(current_file)
        if filename.lower().endswith(".pdf"):
            document = fitz.open(filename)
            os.startfile(filename)
            print("PDF file opened successfully:", filename)
            current_file = filename
        else:
            if os.path.exists(filename):  # Check if the file exists
                process = subprocess.Popen(["notepad.exe", filename])
                print("File opened successfully:", filename)
                current_file = filename
            else:
                print(filename, "file not found.")
    except FileNotFoundError:
        print(filename, "file not found.")


def scroll_up():
    pyautogui.press('pageup')  # Scroll up 3 steps (adjust as needed)

def scroll_down():
    pyautogui.press('pagedown') # Scroll down 3 steps (adjust as needed)


def read_file_pdf():
    global current_file
    if current_file:
        try:
            if current_file.lower().endswith(".pdf"):
                with open(current_file,"rb") as pdf:
                    reader = PyPDF2.PdfReader(pdf,strict=False)
                    for page in reader.pages:
                        content = page.extract_text()
                        tts = pyttsx3.init()
                        tts.say(content)
                        tts.runAndWait()
            else:
                with open(current_file, "r") as file:
                    file_content = file.read()
                    tts = pyttsx3.init()
                    tts.say(file_content)
                    tts.runAndWait()
        except FileNotFoundError:
            print(current_file, "file not opened.")
    else:
        print("no file currently opened.")


def make_folder(folder_name):
    global current_directory
    new_folder_path = os.path.join(current_directory, folder_name)
    try:
        os.makedirs(new_folder_path)
        print("folder", folder_name, "created successfully.")
    except FileExistsError:
        print("folder", folder_name, "already exists.")
    except Exception as e:
        print("try again later.")

def open_folder(folder_name):
    global current_directory
    new_folder_path = os.path.join(current_directory, folder_name)
    if os.path.exists(new_folder_path):
        current_directory = new_folder_path
        print(current_directory, "is now opened.")
    else:
        print(folder_name, "does not exis.")

def go_back():
    global current_directory
    root_drive = os.path.splitdrive(current_directory)[0]  # Get the root drive of the current directory
    if current_directory != root_drive:  # Check if the current directory is not the root drive
        current_directory = os.path.dirname(current_directory)  # Go back one directory
        print(current_directory, " is current folder.")
    else:
        print("cannot go back beyond the root drive.")

def list_directory():
    global current_directory
    try:
        files = os.listdir(current_directory)
        if files:
            print("files and directories in ", current_directory + " are ")
            for item in files:
                print(item)
        else:
            print("the directory is empty.")
    except FileNotFoundError:
        print("directory not found.")
    except Exception as e:
        print("try again later.")

def delete_folder(folder_name):
    folder_path = os.path.join(current_directory, folder_name)
    try:
        shutil.rmtree(folder_path)
        print("folder", folder_name, "deleted successfully.")
    except FileNotFoundError:
        print("folder", folder_name, "not found.")
    except Exception as e:
        print("error deleting folder.")


def delete_any_file(filename):
    try:
        os.remove(filename)
        print(filename, "deleted successfully.")
    except FileNotFoundError:
        print(filename, "not found.")


def close_any_file():
    global current_file
    if current_file:
        if current_file.lower().endswith(".txt"):
            save_file(current_file)
        pyautogui.hotkey('alt', 'f4')  # Send Alt + f4 to close the any opened file
        print(current_file, "closed successfully.")
        current_file = None
    else:
        print("no file is currently opened.")


def exit_script():
    close_any_file() # close the file before exiting
    print("Good bye ")
    exit()


def main():
    while True:
        command = listen_for_command()
        
        # for txt files ----------------
        if command.startswith("open file"):
            filename = command.split(" ")[2] if len(command.split(" ")) > 2 else None
            if filename:
                filename = filename + ".txt" if not filename.endswith(".txt") else filename
                open_file_pdf(filename)
            else:
                print("provide a filename to open.")

        elif command.startswith("create file"):
            filename = command.split(" ")[2] if len(command.split(" ")) > 2 else None
            if filename:
                filename = filename + ".txt" if not filename.endswith(".txt") else filename
                create_file(filename)
            else:
                print("provide a filename to create.")

        elif command.startswith("write"):
            text = command.split(" ", 1)[1] if len(command.split(" ")) > 1 else None
            if text:
                write_file(text)
            else:
                print("provide text to write.")

        elif command.startswith("append"):
            text = command.split(" ", 1)[1] if len(command.split(" ")) > 1 else None
            if text:
                append_file(text)
            else:
                print("provide text to append.")

        elif command.startswith("delete file"):
            filename = command.split(" ")[2] if len(command.split(" ")) > 2 else None
            if filename:
                filename = filename + ".txt" if not filename.endswith(".txt") else filename
                delete_any_file(filename)
            else:
                print("provide a filename to delete.")        
        
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
                print("provide both old and new filenames.")

        # for pdf files ----------------
        elif command.startswith("open pdf"):
            filename = command.split(" ")[2] if len(command.split(" ")) > 2 else None
            if filename:
                filename = filename + ".pdf" if not filename.endswith(".pdf") else filename
                open_file_pdf(filename)
            else:
                print("provide a PDF name to open.")

        elif command.startswith("delete pdf"):
            filename = command.split(" ")[2] if len(command.split(" ")) > 2 else None
            if filename:
                filename = filename + ".pdf" if not filename.endswith(".pdf") else filename
                delete_any_file(filename)
            else:
                print("provide a PDF name to delete.")

        # for image files ----------------
                
        # for audio files ----------------

        # for both txt and pdf files ----------------
        elif command.startswith("scroll up"):
            scroll_up()

        elif command.startswith("scroll down"):
            scroll_down()

        elif command.startswith("read"):
            read_file_pdf()

        # for folder ----------------
        elif command.startswith("make folder"):
            folder_name = command.split(" ", 2)[2] if len(command.split(" ")) > 2 else None
            if folder_name:
                make_folder(folder_name)
            else:
                print("provide a folder name to create.")

        elif command.startswith("open folder"):
            folder_name = command.split(" ", 2)[2] if len(command.split(" ")) > 2 else None
            if folder_name:
                open_folder(folder_name)
            else:
                print("provide a folder name to open.")

        elif command.startswith("go back"):
            go_back()

        elif command.startswith("delete folder"):
            folder_name = command.split(" ", 2)[2] if len(command.split(" ")) > 2 else None
            if folder_name:
                delete_folder(folder_name)
            else:
                print("provide a folder name to delete.")

        elif command.startswith("list"):
            list_directory()

        # for closing any file ----------------
        elif command.startswith("close"):
            close_any_file()

        # for exiting script ----------------
        elif command.startswith("exit"):
            exit_script()

if __name__ == "__main__":
    main()
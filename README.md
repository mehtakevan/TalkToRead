# **TalkingTom**:

Our project aims to empower the handicapped and visually impaired by providing a versatile file management tool. This Python script is a voice-controlled file manager that allows users to perform various file management operations using voice commands. The script uses speech recognition to understand user commands and performs actions such as creating files, reading files, renaming files, writing to files, opening PDFs, reading PDFs, opening images, playing audio files, and more. At the core of our mission is the belief that access to digital content should be a right, not a privilege. By breaking down barriers and enabling access for all, we are fostering independence and empowerment. Our script is a testament to this belief, as it has the potential to transform countless lives with just a few lines of code. Just one script can open up a world of possibilities, allowing individuals to navigate the digital landscape with ease and confidence

# **Features**
- Open and create text files
- Read The text files
- Rename and delete text files
- Write to and append to text files
- Open and delete PDF files
- Read The text files
- Open and delete image files
- Play audio files
- Navigate through folders
- List files and directories in the current folder
- summarise the file

# **Speech Commands**
| **Function** | **Speech Commands** |
|-------|-----|
| Open Text File | open file {name}  | 
| Read Text File | read |
| Delete Text File   | delete file {name}  | 
| Close Text File | close  |
| Create Text File | create file {name}  |
| Rename Text File | rename {old} {new}  |
| Write in Text File | write {text}  |
| Append Text File | append {text}  |
| Scroll Up | Scroll Up  |
| Scroll Down | Scroll Down  |
| Open PDF File | open pdf {name} |
| Close PDF File | close |
| Delete PDF File | delete pdf {name} |
| Read PDF File | read pdf {name} |
| Open Image | open image {name} |
| Close Image | close |
| Delete Image | delete image {name} |
| Play Audio | play audio {name} |
| Close Audio file | stop audio |
| Pause Audio | pause  |
| Continue Audio | continue |
| Open Folder | open folder {name} |
| Delete Folder | delete folder {name} |
| Go Back | go back |
| List the files | list |
| Make New Folder | make folder {name} |
| Exit the application | goodbye |

# **Platforms supported:**
- Windows
- Linux
- MacOS

# **Dependencies**
- speech_recognition
- pyautogui
- pyttsx3
- PyPDF2
- fitz (PyMuPDF)
- sumy
- PIL
- pygame

# **Usage**
- Install the required dependencies using pip install -r requirements.txt.
- Run the script using python voice_file_manager.py.
- Speak commands to interact with the file manager (e.g., "Open file example.txt", "Create file new.txt", "Play audio music.mp3", "Read").
# **Note**
This script is designed for Windows operating systems and may require adjustments for use on other platforms.

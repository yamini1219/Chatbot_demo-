import speech_recognition as sr
import pyttsx3
import threading

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()


def say_message(message):
    """Speaks a given message."""
    tts_engine.say(message)
    tts_engine.runAndWait()


def listen_for_activation():
    """Continuously listens to the microphone and activates on the keyword."""
    with sr.Microphone() as source:
        print("Listening for 'Hey bro'...")
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                # Listen for audio
                audio = recognizer.listen(source, timeout=None)

                # Recognize speech using Google's speech recognition
                text = recognizer.recognize_google(audio)
                print(f"Heard: {text}")
                """
                At the command line, only need to run once to install the package via pip:

                $ pip install google-generativeai
                """

                import google.generativeai as genai

                genai.configure(api_key="AIzaSyBtwWetIYbVLGxTTb2fpM0UlxRojAA3OK8")

                # Set up the model
                generation_config = {
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 0,
                    "max_output_tokens": 8192,
                }

                safety_settings = [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                ]

                model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                              generation_config=generation_config,
                                              safety_settings=safety_settings)

                convo = model.start_chat(history=[
                    {
                        "role": "user",
                        "parts": ["how os works"]
                    },
                    {
                        "role": "model",
                        "parts": [
                            "## How an Operating System Works: A Simplified Explanation\n\nThink of your computer as a bustling city and the operating system (OS) as its mayor.  Just like a mayor manages city resources and services, the OS controls everything that happens on your computer.\n\nHere's a breakdown of how an OS works:\n\n*1. The Boot Process:\n\n When you turn on your computer, the OS is loaded into memory from the hard drive or SSD. This process is called booting.\n* During booting, the OS initializes hardware components like the CPU, memory, and storage devices.\n\n*2. Managing Hardware:\n\n The OS acts as a mediator between applications and hardware. \n* It provides a consistent way for applications to interact with hardware components without needing to know the specifics of each device.\n* For example, when you print a document, the OS handles communicating with the printer, sending data, and managing print queues.\n\n*3. Providing User Interface:\n\n The OS provides a user interface (UI) for you to interact with the computer. This can be a graphical interface (GUI) with windows, icons, and menus, or a command-line interface (CLI) where you type commands.\n\n*4. Managing Applications:\n\n The OS manages running applications, allocating resources like CPU time, memory, and storage space. \n* It allows you to switch between applications, start and stop them, and ensures they don't interfere with each other.\n\n*5. Handling Files and Data:\n\n The OS provides a file system that organizes data on storage devices. \n* It allows you to create, delete, move, and copy files and folders. \n* It also provides security features to protect your data.\n\n*6. Networking:\n\n Modern operating systems handle network connections, enabling communication with other computers and the internet. \n* They manage network protocols and ensure secure data transmission.\n\n*7. Security:\n\n The OS protects your computer from malware and unauthorized access. \n* It provides user accounts and permissions, firewalls, and other security features.\n\n*In simpler terms:\n\nImagine a restaurant. The OS is the head chef who manages all the cooks (applications) and ensures they have the ingredients (hardware resources) they need. The head chef also takes orders from customers (users) and delivers the final product (output) while keeping the kitchen organized and running smoothly.\n\nTypes of Operating Systems:\n\n *Windows:* The most popular desktop OS, known for its user-friendly interface.\n* *macOS:* Designed for Apple computers, known for its sleek design and focus on creativity.\n* *Linux:*  A free and open-source OS, popular for servers and developers, known for its flexibility and stability.\n* *Android:*  A mobile OS designed for smartphones and tablets, known for its versatility and app ecosystem.\n* *iOS:*  A mobile OS designed for Apple's iPhones and iPads, known for its simplicity and focus on security.\n\nThis is a simplified explanation of how an operating system works. The actual mechanisms are complex and involve intricate interactions between software and hardware components. However, this overview should give you a basic understanding of the crucial role an OS plays in making your computer functional and user-friendly."]
                    },
                ])

                convo.send_message(text)
                print(convo.last.text)
                say_message(convo.last.text)
                # Check for the activation phrase
                if "hey prasad" in text.lower():
                    say_message("Hello Boss, what can I do for you?")
            except sr.UnknownValueError:
                # Handle unintelligible speech
                print("Could not understand audio")
            except sr.RequestError as e:
                # Handle errors in the recognition request
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                # General exception handling
                print(f"An unexpected error occurred: {e}")


# Run the listening function in a separate thread with daemon=True
thread = threading.Thread(target=listen_for_activation, daemon=True)
thread.start()

# Keep the main thread alive (you might have other code here)
while True:
    pass
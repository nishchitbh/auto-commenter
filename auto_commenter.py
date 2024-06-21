import os
import argparse
import google.generativeai as genai
from dotenv import load_dotenv
from colorama import Fore
import json

load_dotenv()

# This script utilizes the Google Generative AI API to automatically add comments to provided Python code files. It supports both single file and directory processing. 
def parse():
    '''Parses command line arguments for file or directory input.
    Args:
        None
    Returns:
        str: file path if provided.
        str: directory path if provided. '''
    parser = argparse.ArgumentParser(description="Auto commenter")
    parser.add_argument(
        "--file",
        type=str,
        required=False,
        default=None,
        help="File to be commented",
    )
    parser.add_argument(
        "--directory",
        type=str,
        required=False,
        default=None,
        help="Directory to be commented",
    )
    args = parser.parse_args()
    filename = args.file
    directory = args.directory
    return filename, directory

def llm_init():
    '''Initializes the Google Generative AI model and starts a chat session.
    Args:
        None
    Returns:
        genai.Chat: Chat session object for interacting with the model. '''
    with open("sys_instruction.txt", "r") as instruction_file:
        sys_instruction = instruction_file.read()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", system_instruction=sys_instruction
    )
    chat = model.start_chat(history=[])
    return chat

def commenter(chat, file):
    '''Sends the code to the LLM for commenting and retrieves the commented code.
    Args:
        genai.Chat: Chat session object for interacting with the model.
        str: Code as a string.
    Returns:
        str: Commented code. '''
    response = chat.send_message(file)
    code_with_comments = response.text
    return code_with_comments

def content_generator(file_name):
    '''Reads the content of a file and formats it for LLM input.
    Args:
        str: File path.
    Returns:
        str: JSON string containing the file path and content. '''
    with open(file_name, "r") as file:
        content = file.read()
    json_content = json.dumps({file_name: content})
    return json_content

def content_writer(directory, commented_code):
    '''Writes commented code to a file.
    Args:
        str: File path.
        str: Commented Python code.
    Returns:
        None '''
    with open(directory, "w") as file:
        file.write(commented_code)

def extension_extractor(filename: str):
    '''Extracts the extension of a file.
    Args:
        str: File path.
    Returns:
        str: File extension. '''
    name_ext = filename.split(".")
    return name_ext[-1]

def directory_commenter(root_dir):
    '''Recursively traverses a directory and comments all supported code files.
    Args:
        str: Directory path.
    Returns:
        None '''
    chat = llm_init()
    ignore = ["venv", ".git", "__pycache__"]
    codes = ["c", "cpp", "py", "js", "ts", "java", "rs"]
    entries = [
        folder
        for folder in os.listdir(root_dir)
        if folder not in ignore and extension_extractor(folder) in codes
    ]
    entries = sorted(entries)

    for iter, entry in enumerate(entries):
        path = os.path.join(root_dir, entry)

        if os.path.isdir(path):
            directory_commenter(path)
        else:
            content = content_generator(path)
            print(f"{Fore.GREEN}Processing {path}...{Fore.WHITE}")
            commented = commenter(chat, content)
            content_writer(path, commented)

def main():
    '''Main function that orchestrates single file or directory commenting.
    Args:
        None
    Returns:
        None '''
    chat = llm_init()

    single_file, directory = parse()

    if not single_file:
        directory_commenter(directory)
    else:
        content = content_generator(single_file)
        print(f"{Fore.GREEN}Processing {single_file}...{Fore.WHITE}")
        commented = commenter(chat, content)
        # Removing the initial "```python" and the last "```" from the code, as these are added by the LLM
        if commented[:9] == "```python":
            commented = commented[10:-3]
        with open(single_file, "w") as code_file:
            code_file.write(commented)


main()

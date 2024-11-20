# This Python script is designed to comment out the code within specified files and directories. It uses a chat model from Ollama to generate comments based on human-readable input. The script supports various programming languages and can process both individual files and entire directories.

import os  
import argparse  
import ollama  
from colorama import Fore  
import json  

# Load historical data from "history.json"
with open("history.json", "r") as history_file:  
    history = json.load(history_file)  

def parse():  
    '''Parses command-line arguments to determine whether to comment a single file or an entire directory.
    Returns:
        tuple: A tuple containing the filename and directory, which can be None if not specified. '''
    parser = argparse.ArgumentParser(description="Auto commenter")
    parser.add_argument("--file", type=str, required=False, default=None, help="File to be commented")
    parser.add_argument("--directory", type=str, required=False, default=None, help="Directory to be commented")
    args = parser.parse_args()  
    filename = args.file  
    directory = args.directory  
    return filename, directory  

with open("sys_instruction.txt", "r") as sys_file:  
    sys_text = sys_file.read()  

# Insert the system instruction into the history list
history.insert(0, {"role": "system", "content": sys_text})  

def generate_comment(human_text):  
    '''Generates a comment using an Ollama chat model based on the provided human text.
    Args:
        human_text (str): The input text for which to generate a comment.
    Returns:
        str: The generated comment. '''
    history.append({"role": "user", "content": human_text})
    response = ollama.chat(model="qwen2.5-coder:7b", messages=history)
    return response["message"]["content"]  

def commenter(chat, file):  
    '''Reads the content of a file and returns it commented.
    Args:
        chat (function): The function to generate comments.
        file (str): The path to the file to comment.
    Returns:
        str: The commented content. '''
    with open(file, "r") as f:
        content = f.read()
    return chat(content)  

def content_generator(file_name):  
    '''Generates a JSON representation of the content of a single file.
    Args:
        file_name (str): The path to the file.
    Returns:
        str: A JSON string containing the file name and its content. '''
    with open(file_name, "r") as file:
        content = file.read()
    return json.dumps({file_name: content})  

def content_writer(directory, commented_code):  
    '''Writes the commented code to a specified directory.
    Args:
        directory (str): The path to the directory where the commented code will be written.
        commented_code (str): The commented code. '''
    with open(directory, "w") as file:
        file.write(commented_code)  

def extension_extractor(filename: str):  
    '''Extracts the file extension from a filename.
    Args:
        filename (str): The filename to extract the extension from.
    Returns:
        str: The file extension. '''
    name_ext = filename.split(".")
    return name_ext[-1]  

def directory_commenter(root_dir):  
    '''Recursively comments all supported code files in a given directory.
    Args:
        root_dir (str): The path to the directory to comment. '''
    chat = generate_comment
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
            print(f"{Fore.GREEN}Processing {path}...{Fore.WHITE}")
            commented = commenter(chat, path)
            content_writer(path, commented)  

def main():  
    '''Main function to parse command-line arguments and comment files or directories accordingly. '''
    chat = generate_comment

    single_file, directory = parse() 

    if not single_file:  
        directory_commenter(directory) 
    else:  
        print(f"{Fore.GREEN}Processing {single_file}...{Fore.WHITE}")
        commented = commenter(chat, single_file)
        if commented[:9] == "```python":  
            commented = commented[10:-3]
        with open(single_file, "w") as code_file:
            code_file.write(commented)  

main()
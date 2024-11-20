import os  
import argparse  
import ollama  
from colorama import Fore  
import json  

# Load historical chat data from a JSON file.
with open("history.json", "r") as history_file:  
    history = json.load(history_file)  

def parse():  
    '''Parse command-line arguments to specify a file or directory for commenting.
    
    Returns:
        tuple: A tuple containing the filename and directory specified by the user.'''
    parser = argparse.ArgumentParser(description="Auto commenter")
    parser.add_argument("--file", type=str, required=False, default=None, help="File to be commented")
    parser.add_argument("--directory", type=str, required=False, default=None, help="Directory to be commented")
    args = parser.parse_args()  
    filename = args.file  
    directory = args.directory  
    return filename, directory  

# Read system instruction from a text file.
with open("sys_instruction.txt", "r") as sys_file:  
    sys_text = sys_file.read()  

# Insert the system instruction into the historical chat data.
history.insert(0, {"role": "system", "content": sys_text})  

def generate_comment(human_text):  
    '''Generate a comment for the given human text using an AI model.
    
    Args:
        human_text (str): The input text to be commented.
    
    Returns:
        str: Commented code or message.'''
    history.append({"role": "user", "content": human_text})
    response = ollama.chat(model="qwen2.5-coder:7b", messages=history)
    return response["message"]["content"]  

def commenter(chat, file):  
    '''Read the content of a file and pass it to the comment generation function.
    
    Args:
        chat (function): The function to generate comments.
        file (str): Path to the file to be commented.
    
    Returns:
        str: Commented code or message.'''
    with open(file, "r") as f:
        content = f.read()
    return chat(content)  

def content_generator(file_name):  
    '''Read the content of a single file and convert it into JSON format.
    
    Args:
        file_name (str): Path to the file to be read.
    
    Returns:
        str: JSON formatted string containing the file content.'''
    with open(file_name, "r") as file:
        content = file.read()
    return json.dumps({file_name: content})  

# Write the commented code back to the specified directory or file.
def content_writer(directory, commented_code):  
    '''Write the commented code back to a file.
    
    Args:
        directory (str): Path to the file where commented code will be written.
        commented_code (str): The commented code to write.'''
    with open(directory, "w") as file:
        file.write(commented_code)  

# Extract the file extension from a filename.
def extension_extractor(filename: str):  
    '''Extract the file extension from the given filename.
    
    Args:
        filename (str): The filename from which to extract the extension.
    
    Returns:
        str: The file extension.'''
    name_ext = filename.split(".")
    return name_ext[-1]  

# Recursively comment all relevant files in a directory structure.
def directory_commenter(root_dir):  
    '''Recursively comment all relevant files in a directory structure.
    
    Args:
        root_dir (str): Path to the root directory containing code files.'''
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

# Main function to process either a single file or an entire directory.
def main():  
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
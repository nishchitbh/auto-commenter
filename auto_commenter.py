import os
import argparse
import google.generativeai as genai
from dotenv import load_dotenv
import json
from colorama import Fore

load_dotenv()

# This code uses Google's Generative AI model to automatically add comments to a given file or directory.
# The code first parses user-provided arguments, then extracts the content of the target file or files within the directory. 
# It then calls the Generative AI model to add comments to the extracted content and finally writes the commented code back to the original file(s).

def parse():
    '''Parses command line arguments.
    Args:
        None
    Returns:
        str: filename
        str: directory'''
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

def commenter(file):
    '''Adds comments to a given code snippet using Google's Generative AI model.
    Args:
        str: file
    Returns:
        str: code_with_comments'''
    with open("sys_instruction.txt", "r") as instruction_file:
        sys_instruction = instruction_file.read()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", system_instruction=sys_instruction
    )

    response = model.generate_content(file)
    code_with_comments = response.text
    return code_with_comments

def content_generator(file_name):
    '''Reads content from a given file.
    Args:
        str: file_name
    Returns:
        str: content'''
    with open(file_name, "r") as file:
        content = file.read()
    return content

def content_writer(directory, commented_code):
    '''Writes commented code to a given file.
    Args:
        str: directory
        str: commented_code
    Returns:
        None'''
    with open(directory, "w") as file:
        file.write(commented_code)

def extension_extractor(filename: str):
    '''Extracts the file extension from a given filename.
    Args:
        str: filename
    Returns:
        str: extension'''
    name_ext = filename.split(".")
    return name_ext[-1]

def directory_commenter(root_dir):
    '''Recursively comments all code files within a given directory.
    Args:
        str: root_dir
    Returns:
        None'''
    ignore = ["venv", ".git", "__pycache__"]
    codes = ["c", "cpp", "py", "js", "ts", "java", "rs"]
    entries = [folder for folder in os.listdir(root_dir) if folder not in ignore]
    entries = sorted(entries)

    for entry in entries:
        path = os.path.join(root_dir, entry)

        if os.path.isdir(path):
            directory_commenter(path)
        else:
            if extension_extractor(path) in codes:
                content = content_generator(path)
                print(f"{Fore.GREEN}Processing {path}...{Fore.WHITE}")
                commented = commenter(content)
                content_writer(path, commented)
                


def main():
    '''Main function that orchestrates the comment adding process.
    Args:
        None
    Returns:
        None'''
    single_file, directory = parse()

    if not single_file:
        files = [a for a in os.listdir(directory) if os.path.isfile(a)]
        contents = {i: content_generator(i) for i in files}
        json_contents = json.dumps(contents)
        commented = commenter(json_contents)
        if commented[:3] == "```":
            commented = commented[8:-3]
        dict_commented = json.loads(commented)
        for i in dict_commented:
            with open(i, "w") as output:
                output.write(dict_commented[i])
    else:
        content = content_generator(single_file)
        print(f"{Fore.GREEN}Processing {single_file}...{Fore.WHITE}")
        commented = commenter(content)
        if commented[:9] == "```python":
            commented = commented[10:-3]
        with open(single_file, "w") as code_file:
            code_file.write(commented)


main()

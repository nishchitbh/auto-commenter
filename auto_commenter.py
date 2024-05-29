import os
import argparse
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()


def parse():
    '''Parses command line arguments to determine the file or directory to be commented.

    Returns:
        tuple: filename and directory'''
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
    '''Uses Google's Gemini AI model to generate comments for the given code.

    Args:
        str: Python code to be commented

    Returns:
        str: Python code with generated comments'''
    with open("sys_instruction.txt", "r") as instruction_file:
        sys_instruction = instruction_file.read()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro", system_instruction=sys_instruction
    )

    response = model.generate_content(file)
    code_with_comments = response.text
    return code_with_comments


def content_generator(file_name):
    '''Reads and returns the content of the given file

    Args:
        str: name of the file
    Returns:
        str: content of the file'''
    with open(file_name, "r") as file:
        content = file.read()
    return content


def main():
    '''Main function to orchestrate the comment generation process.'''
    single_file, directory = parse()

    if not single_file:
        # Process all files in the given directory
        files = [a for a in os.listdir(directory) if os.path.isfile(a)]
        contents = {i: content_generator(i) for i in files}
        json_contents = json.dumps(contents)
        commented = commenter(json_contents)
        dict_commented = json.loads(commented)
        for i in dict_commented:
            with open(i, "w") as output:
                output.write(dict_commented[i])
    else:
        # Process the single given file
        content = content_generator(single_file)
        commented = commenter(content)[10:-3]
        with open(single_file, "w") as code_file:
            code_file.write(commented)



main()

import os
import argparse
import google.generativeai as genai
from dotenv import load_dotenv
import json

# This code leverages Google's Gemini API to add comments to python code. You can comment single file as well as a directory.

# Load environment variables from .env file
load_dotenv()


def parse():
    """Parses command line arguments and returns filename and directory.

    Returns:
        tuple: filename, directory"""
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
    """Takes code as input, generates comments using Gemini and returns commented code.

    Args:
        str: code to be commented

    Returns:
        str: commented code"""
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
    """Reads content from a file.

    Args:
        str: filename

    Returns:
        str: file content"""
    with open(file_name, "r") as file:
        content = file.read()
    return content


def main():
    """Main function to orchestrate the comment generation process."""
    single_file, directory = parse()

    if not single_file:
        # Process all files in the given directory
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
        # Process single file
        content = content_generator(single_file)
        commented = commenter(content)
        if commented[:9] == "```python":
            commented = commented[10:-3]
        with open(single_file, "w") as code_file:
            code_file.write(commented)


main()

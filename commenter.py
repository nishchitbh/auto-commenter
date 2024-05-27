import argparse
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()


def parse():
    """Parses command line arguments.

    Args:
        None

    Returns:
        str: The filename provided as an argument.
    """
    parser = argparse.ArgumentParser(description="Auto commenter")
    parser.add_argument("--file", type=str, required=True, help="File to be commented")
    args = parser.parse_args()
    filename = args.file
    return filename


def commentor(filename):
    """Adds comments to a Python code file using a language model.

    Args:
        filename (str): The path to the Python code file.

    Returns:
        None
    """
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="You are a coding assistant that helps in commenting codes. The inputs will be python codes with no useful comments. Then, you should add comments to the code. Add comments about how the main logic of the code works, what are the inputs and outputs of functions, etc. DHowever, you don't have to add comments on what the libraries do. If the file is already well commented, don't touch anything and return the file as it is."
    )
    with open(filename, "r") as file:
        code = file.read()
    response = model.generate_content(code)
    code_with_comments = response.text
    with open(filename, "w") as main_file:
        main_file.write(code_with_comments[10:-3])


def main():
    """Main function that orchestrates the comment addition process.

    Args:
        None

    Returns:
        None
    """
    filename = parse()
    commentor(filename)


if __name__ == "__main__":
    main()

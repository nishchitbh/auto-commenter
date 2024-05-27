import argparse
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()


def parse():
    parser = argparse.ArgumentParser(description="Auto commenter")
    parser.add_argument("--file", type=str, required=True, help="File to be commented")
    args = parser.parse_args()
    filename = args.file
    return filename


def commentor(filename):

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="You are a coding assistant whose job is to add useful comments to the given code. You must begin by briefly describing the code's purpose (e.g., \"This code takes a human image as input and returns the gender of the person in the image by using Convolutional Neural Networks. The process involves reading the image, passing it through CNN, and generating output.\"). Then, add comments about the main logic of the code, complex lines within the code, detailing function arguments and returns, and providing context where necessary. Refrain from commenting on library functionalities. If the code is already well commented, don't alter the code and return the code as it is."
    )
    with open(filename, "r") as file:
        code = file.read()
    response = model.generate_content(code)
    code_with_comments = response.text
    with open(filename, "w") as main_file:
        main_file.write(code_with_comments[10:-3])


def main():
    filename = parse()
    commentor(filename)


main()
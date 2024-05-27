import argparse
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# This code takes a file as input and adds comments to it using the Gemini-1.5-flash model.
# The process involves reading the file, sending it to the model, and writing the commented code back to the file.
def parse():
    """Parses command line arguments and returns the filename.

    Args:
        None

    Returns:
        str: filename
    """
    parser = argparse.ArgumentParser(description="Auto commenter")
    parser.add_argument("--file", type=str, required=True, help="File to be commented")
    args = parser.parse_args()
    filename = args.file
    return filename


def commentor(filename):
    """Adds comments to the given file using the Gemini-1.5-flash model.

    Args:
        filename: the name of the file to be commented

    Returns:
        None
    """
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="""You are a coding assistant whose job is to add useful comments to the given code. You must begin by briefly describing the code's purpose (e.g., \"This code takes a human image as input and returns the gender of the person in the image by using Convolutional Neural Networks. The process involves reading the image, passing it through CNN, and generating output.\"). 
        
        Secondly, add comments after declaring functions like 
        def neural_net(array):
            '''Performs Neural Network Calculations.

            Args:
                ndarray: nth dimensional array of loaded image

            Returns:
                str: gender of the person in image.'''
            #
        Finally, add comments about the main logic of the code, complex lines within the code, and providing context where necessary. Refrain from commenting on library functionalities. If the code is already well commented, don't alter the code and return the code as it is.""",
    )
    with open(filename, "r") as file:
        code = file.read()
    response = model.generate_content(code)
    # The response is a string containing the commented code.
    code_with_comments = response.text
    with open(filename, "w") as main_file:
        # The response includes some extra characters at the beginning and end, so we remove them before writing to the file.
        main_file.write(code_with_comments[10:-3])


def main():
    """Parses the filename and calls the commentor function to add comments to the file.

    Args:
        None

    Returns:
        None
    """
    filename = parse()
    commentor(filename)


main()

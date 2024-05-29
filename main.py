import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables from the .env file
load_dotenv()


def commentor(file):
    '''This function takes a string containing json with code files as values and returns a string with comments added to the code.

    Args:
        file: json string containing code files.

    Returns:
        str: json string with commented code.
    '''
    with open("sys_instruction.txt", "r") as instruction_file:
        sys_instruction = instruction_file.read()
    # Get the Google API key from environment variables
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    # Configure the Google Generative AI library with the API key
    genai.configure(api_key=GOOGLE_API_KEY)
    # Initialize the Gemini model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", system_instruction=sys_instruction
    )

    # Generate comments using the model
    response = model.generate_content(file)
    code_with_comments = response.text
    return code_with_comments


def content_generator(file_name):
    '''This function reads the content of a file and returns it as a string.

    Args:
        file_name: name of the file to be read

    Returns:
        str: content of the file
    '''
    with open(file_name, 'r') as file:
        content = file.read()
    return content


def main():
    # This code takes a directory as an input and iterates through all the files. It then reads the contents of each file, adds comments using Google's Gemini model, and writes the commented code back to the file.
    # Get a list of all files in the current directory
    files = [a for a in os.listdir('.') if os.path.isfile(a)]

    # Create a dictionary to store the content of each file
    contents = {i: content_generator(i) for i in files}
    # Convert the dictionary to a JSON string
    json_contents = json.dumps(contents)
    # Use the commentor function to add comments to the code
    commented = commentor(json_contents)[8:-3]
    # Convert the commented code back to a dictionary
    dict_commented = json.loads(commented)
    # Write the commented code back to the files
    for i in dict_commented:
        with open(f"{i}", "w") as output:
            output.write(dict_commented[i])

main()


# Auto Commenter

This script automatically adds comments to Python code files using Google's Gemini AI model. It takes a Python file as input and generates useful comments that explain the main logic of the code, inputs, and outputs of functions. If the file is already well-commented, the script leaves it unchanged.

## Features

- Parses command-line arguments to get the input file.
- Uses Google Generative AI to generate comments.
- Updates the Python file with the generated comments.

## Prerequisites

- Python 3.6 or later
- A Google API key with access to the Google Generative AI models
- An `.env` file with the Google API key

## Installation

1. Clone this repository or download the script files.
2. Install the required libraries using pip:

   ```bash
   pip install google-generativeai python-dotenv
   ```

3. Create an `.env` file in the same directory as the script and add your Google API key:

   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

Run the script from the command line, specifying the file to be commented with the `--file` argument:

```bash
python commenter.py --file path/to/your/python_file.py
```

## Example

Suppose you have a Python file `example.py` that you want to add comments to. You would run:

```bash
python your_script_name.py --file example.py
```

The script will read `example.py`, generate comments using Google's Gemini AI model, and update `example.py` with the new comments.

## Detailed Explanation of Functions

- `parse()`: Parses command-line arguments to get the filename.
- `commentor(filename)`: Reads the code from the specified file, sends it to the Google Generative AI model to generate comments, and writes the commented code back to the file.
- `main()`: The main function that coordinates the parsing of arguments and the commenting process.

## Notes

- Ensure that your Google API key is active and has access to the required AI models.
- The script uses the Gemini 1.5 flash model to generate comments.
- The system instruction for the AI model is configured to add comments to the code, focusing on explaining the main logic, inputs, and outputs.

## License

This project is licensed under the MIT License.

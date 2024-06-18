# Auto Commenter

The Auto Commenter is a Python script designed to automatically generate comments for your Python code using Google's Gemini AI model. This tool can process individual files or entire directories, adding helpful comments to your code to improve readability and maintainability.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Example](#example)
- [License](#license)

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/mr0bn0xi0us/auto-commenter.git
    cd auto-commenter
    ```

2. **Set up a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install google-generativeai, colorama
    ```

4. **Create a `.env` file** in the root directory of the project and add your Google API key:
    ```sh
    echo "GOOGLE_API_KEY=your_google_api_key" > .env
    ```

## Usage

The script can be run from the command line and accepts two optional arguments: `--file` for a single file and `--directory` for a directory of files.

### Command Line Arguments

- `--file`: Specify a single file to be commented.
- `--directory`: Specify a directory containing multiple files to be commented.

### Examples

#### Commenting a Single File

```sh
python auto_commenter.py --file path/to/your_file.py
```

#### Commenting All Files in a Directory

```sh
python auto_commenter.py --directory path/to/your_directory
```

## Configuration

The script reads a system instruction from a file named `sys_instruction.txt` which should be located in the same directory as the script. This file contains the instructions that will be given to the AI model for generating comments.

## Example

Given a Python file `example.py` with the following content:

```python
def add(a, b):
    return a + b
```

Running the command:

```sh
python auto_commenter.py --file example.py
```

Might produce the following commented code:

```python
# Function to add two numbers
def add(a, b):
    # Returns the sum of a and b
    return a + b
```

## License

This project is licensed under the MIT License.
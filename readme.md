# Auto Commenter

**Auto Commenter** is a Python tool that automates the process of adding comments to code files. Using AI, it analyzes the code and generates meaningful comments to enhance readability and maintainability. The tool supports both individual files and entire directories containing code files.

## Features
- **AI-Powered Commenting**: Generates comments for code files using an AI model.
- **File or Directory Processing**: Process a single file or recursively comment all files in a directory.
- **Customizable Instructions**: Define AI system instructions via a `sys_instruction.txt` file.
- **Supported Languages**: Works with files written in Python, JavaScript, TypeScript, C, C++, Java, Rust, and more.
- **Configurable Ignored Directories**: Skips directories like `venv`, `.git`, and `__pycache__`.

---

## Prerequisites

Ensure the following tools are installed:
- Python 3.8 or later
- Virtual Environment (optional but recommended)

---

## Installation

1. Clone this repository or download the source code.

2. Navigate to the project directory:
   ```bash
   cd auto-commenter
   ```

3. Install dependencies using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Command-Line Arguments

The tool supports two modes of operation:

1. **Single File Processing**
   Specify a single file to comment:
   ```bash
   python main.py --file <path_to_file>
   ```

2. **Directory Processing**
   Process all relevant files in a directory:
   ```bash
   python main.py --directory <path_to_directory>
   ```

   **Note**: Files in ignored directories (`venv`, `.git`, etc.) will be skipped.

---

### Input Files

- **System Instructions**: Provide instructions for the AI model in a `sys_instruction.txt` file.  
  Example:
  ```
  Please generate detailed comments for the given code.
  ```

- **Historical Data**: The AI model uses previous conversations stored in `history.json` for context.

---

## How It Works

1. **Input Parsing**: The script reads command-line arguments to determine whether a file or directory is being processed.
2. **AI Initialization**: Loads the system instructions from `sys_instruction.txt` and initializes historical chat data from `history.json`.
3. **Code Commenting**: For each code file:
   - Reads the content.
   - Sends it to the AI for comment generation.
   - Writes the commented code back to the file.
4. **Recursive Directory Processing**: If a directory is specified, the script recursively processes all relevant files.

---

## Supported Languages

The following file types are supported:
- `.py` (Python)
- `.js` (JavaScript)
- `.ts` (TypeScript)
- `.c` (C)
- `.cpp` (C++)
- `.java` (Java)
- `.rs` (Rust)

---

## Example

### Single File

To process a Python file `example.py`:
```bash
python main.py --file example.py
```

### Directory

To process all files in a directory `src`:
```bash
python main.py --directory src
```

---

## Contributing

If you'd like to contribute to this project:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m "Add feature name"`.
4. Push to the branch: `git push origin feature-name`.
5. Create a pull request.

---

## Issues

If you encounter any issues, please report them in the [Issues](#) section.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Requirements

All required libraries and frameworks are listed in `requirements.txt`. Install them using:
```bash
pip install -r requirements.txt
```

### Example `requirements.txt`

```
argparse
colorama
ollama
```

---

## Acknowledgements

- The AI model is powered by `ollama`.
- Inspired by the need for better code documentation using AI.
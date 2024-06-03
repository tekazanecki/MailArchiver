# File Converter

## Project Description
This project is a Python script that converts image files from the `.webp` format to `.jpg` or `.png` format. The script processes all files in the `input/` directory, saves the converted files in the `output/` directory, and moves the original files to the `arch/` directory.

## Requirements
To run this script, you need:
- Python 3.x
- `Pillow` library (PIL)

## Installation
To run application, you need clone this repository to your local disk:

sh

`git clone https://github.com/tekazanecki/FileConverter cd repository-name`

You need Python and the TtkBootstrap library installed. You can install them using the following commands:

sh

`pip install Pillow`

You can also use the requirements.txt file:

sh

`pip install -r requirements.txt`


## Usage
1. Place `.webp` files in the `input/` directory.
2. Run the script, specifying the target format (`jpg` or `png`):
    ```sh
    python file_converter.py [format]
    ```
    For example, to convert files to `jpg` format, run:
    ```sh
    python file_converter.py jpg
    ```
    If you do not specify a format, `png` will be used by default.

## Directory Structure
- `input/` - directory where you place `.webp` files for conversion.
- `output/` - directory where the converted files are saved.
- `arch/` - directory where the original files are moved after conversion.

## Functionality
- **File Conversion:** The script processes all `.webp` files in the `input/` directory, converts them to the chosen format (`jpg` or `png`), and saves them in the `output/` directory.
- **Archiving:** After successful conversion, the original `.webp` files are moved to the `arch/` directory.

## Example Output
After running the script, you will see information about the processed files in the console:

File example.webp has been loaded
File example.webp has been converted
File example.webp has been moved to archive

## Author
[Your Name](https://github.com/your-profile) - Creator and maintainer of the project

## License
This project is licensed under the MIT License - see the LICENSE file for details.
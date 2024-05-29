# Email Archiver Application using `ttkbootstrap`

![Screenshot](images/screenshot.png)

## Table of Contents
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Features](#features)
- [Files](#files)
  - [Main Application Files](#main-application-files)
  - [Dependencies](#dependencies)
- [Contribution](#contribution)
- [License](#license)

## Installation

To run the application, you need to clone this repository to your local disk:

```sh
git clone https://github.com/your-username/repository-name.git
cd repository-name
```

You need Python and the TtkBootstrap library installed. You can install them using the following command:

```sh
pip install ttkbootstrap
```

You can also use the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

## Running the Application

To run the application, simply execute the following command in the terminal while in the project directory:

```sh
python gui.py
```

## Features
- **IMAP Server Login**: Ability to log in to an email account using IMAP server credentials.
- **Folder Selection**: Option to select folders for archiving.
- **Filename Sanitization**: Automatic removal of invalid characters from filenames.
- **Saving Emails and Attachments**: Save email content and attachments to the chosen location.

## Files

### Main Application Files
- `imap_module.py`: IMAP connection handling and email archiving.
- `utils.py`: Helper functions, e.g., filename sanitization.
- `gui.py`: User interface using `ttkbootstrap`.

### Dependencies
- `ttkbootstrap`: For enhanced UI styling.
- `imaplib`: For IMAP server communication.
- `email`: For handling email message formats.

## Contribution

If you wish to contribute to the project, please submit a pull request or open an issue on GitHub.

## License

The project is available under the MIT license. Details can be found in the LICENSE file.

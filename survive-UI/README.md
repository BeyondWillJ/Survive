# My Flask Game Application

This project is a simple Flask-based game application that allows users to navigate through a text-based adventure. The game state is managed through user sessions, and the content is dynamically loaded from a JSON file.

## Project Structure

```
my-flask-app
├── app.py                # Main application file for the Flask app
├── survive               # Directory containing game data and images
│   ├── survive.json      # Game data in JSON format
│   ├── cover.jpg         # Cover image for the game
│   └── 1.jpg             # Scene image for a specific game state
├── templates             # Directory containing HTML templates
│   ├── cover.html        # Template for the cover page
│   └── index.html        # Template for the main game page
├── static                # Directory for static files
│   └── main.css          # CSS file for styling the application
├── requirements.txt      # List of Python dependencies
├── pyinstaller.spec      # Configuration file for PyInstaller
└── README.md             # Documentation for the project
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd my-flask-app
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment. You can create one using:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application**:
   Start the Flask application by running:
   ```
   python app.py
   ```
   The application will be accessible at `http://127.0.0.1:5000/`.

## Usage

- When you first access the application, you will see the cover page with the cover image.
- Click to enter the game, and navigate through the story by making choices presented on the main game page.

## Building Executable

To create an executable version of the application, use PyInstaller with the provided `pyinstaller.spec` file:
```
pyinstaller pyinstaller.spec
```
This will generate a standalone executable that can be run without needing to install Python or Flask on the target machine.
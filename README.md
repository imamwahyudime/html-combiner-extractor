# HTML Weaver - Combine and Extract HTML, CSS, and JavaScript

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)

**HTML Weaver** is a simple desktop application built with Python and `customtkinter` that allows you to easily combine separate HTML, CSS, and JavaScript files into a single HTML file, or extract these components from an existing HTML file. This tool can be useful for streamlining web development workflows, examining bundled code, or simplifying file management.

## Features:

**Combine:**

- Load content from separate HTML, CSS, and JavaScript files.
- Automatically embed CSS within `<style>` tags in the `<head>` of the HTML.
- Automatically embed JavaScript within `<script>` tags at the end of the `<body>` of the HTML.
- View the combined HTML output in a dedicated text area.
- Save the combined HTML to a `.html` file.

**Extract:**

- Load content from a single HTML file containing embedded CSS and JavaScript.
- Extract the HTML structure, CSS (from `<style>` tags), and JavaScript (from `<script>` tags) into separate text areas.
- Save the extracted HTML, CSS, and JavaScript to individual files (`.html`, `.css`, `.js`).

## Usage:

1. **Prerequisites:**
   - Python 3.x installed on your system.
   - `pip` (Python package installer).

2.  **Install dependencies:**

    ```bash
    pip install customtkinter beautifulsoup4
    ```

3.  **Run the application:**

    ```bash
    python html_gui_app.py
    ```

## How to Use:

1.  **Combine:**

      - Navigate to the "Combine" tab.
      - Click the "Load File..." buttons to select your HTML, CSS, and JavaScript files.
      - Click the "Combine into Single HTML" button.
      - The combined HTML will be displayed in the "Combined HTML Output" textbox.
      - Click "Save As..." to save the combined HTML to a file.

2.  **Extract:**

      - Navigate to the "Extract" tab.
      - Click the "Load File..." button to select the HTML file you want to extract from.
      - Click the "Extract Components" button.
      - The extracted HTML structure, CSS, and JavaScript will be displayed in their respective output textboxes.
      - Click the "Save As..." buttons to save each component to a separate file.

## Technology Used:

  - Built using the `customtkinter` library for the graphical user interface.
  - Utilizes the `Beautiful Soup 4` library for parsing and manipulating HTML.

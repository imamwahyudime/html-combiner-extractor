# File: html_gui_app.py

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

# Import the backend logic
from html_combextr_logic import combine_html_css_js, extract_html_css_js

# --- Constants ---
APP_NAME = "HTML Weaver"
DEFAULT_THEME = "blue" # Options: "blue", "dark-blue", "green"
DEFAULT_APPEARANCE = "System" # Options: "System", "Light", "Dark"
TEXTBOX_HEIGHT = 15 # lines

# --- Main Application Class ---
class HTMLToolApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("900x700") # Adjust size as needed

        # --- Appearance Settings ---
        ctk.set_appearance_mode(DEFAULT_APPEARANCE)
        ctk.set_default_color_theme(DEFAULT_THEME)

        # --- Main Container ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.combine_tab = self.tab_view.add("Combine")
        self.extract_tab = self.tab_view.add("Extract")

        # --- Configure Tab Layouts ---
        self._create_combine_tab()
        self._create_extract_tab()

    # --- Helper Function to Create Labeled Textbox with Load Button ---
    def _create_labeled_textbox(self, parent, row, label_text, file_types, default_ext):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=0, padx=5, pady=5, sticky="nsew")
        frame.grid_columnconfigure(1, weight=1) # Make textbox expand

        label = ctk.CTkLabel(frame, text=label_text, anchor="w")
        label.grid(row=0, column=0, padx=5, pady=(0, 2), sticky="w")

        load_button = ctk.CTkButton(frame, text="Load File...", width=100,
                                    command=lambda tb=None: self._load_file_to_textbox(tb, file_types)) # Placeholder tb
        load_button.grid(row=0, column=2, padx=5, pady=(0, 2), sticky="e")

        textbox = ctk.CTkTextbox(frame, height=TEXTBOX_HEIGHT, wrap="none") # Use wrap="none" for code
        textbox.grid(row=1, column=0, columnspan=3, padx=5, pady=(0, 5), sticky="nsew")

        # Assign the textbox to the button's command *after* textbox creation
        load_button.configure(command=lambda tb=textbox: self._load_file_to_textbox(tb, file_types))

        return textbox # Return the textbox for later reference


    # --- Helper Function to Create Output Textbox with Save Button ---
    def _create_output_textbox(self, parent, row, label_text, file_types, default_ext):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=0, padx=5, pady=5, sticky="nsew")
        frame.grid_columnconfigure(1, weight=1)

        label = ctk.CTkLabel(frame, text=label_text, anchor="w")
        label.grid(row=0, column=0, padx=5, pady=(0, 2), sticky="w")

        save_button = ctk.CTkButton(frame, text="Save As...", width=100,
                                    command=lambda tb=None: self._save_textbox_to_file(tb, default_ext, file_types)) # Placeholder
        save_button.grid(row=0, column=2, padx=5, pady=(0, 2), sticky="e")

        textbox = ctk.CTkTextbox(frame, height=TEXTBOX_HEIGHT, wrap="none", state="disabled") # Start disabled
        textbox.grid(row=1, column=0, columnspan=3, padx=5, pady=(0, 5), sticky="nsew")

        save_button.configure(command=lambda tb=textbox: self._save_textbox_to_file(tb, default_ext, file_types))

        return textbox


    # --- Tab Creation Methods ---
    def _create_combine_tab(self):
        self.combine_tab.grid_columnconfigure(0, weight=1)
        # Configure rows to distribute space (adjust weights as needed)
        self.combine_tab.grid_rowconfigure(0, weight=1) # HTML input
        self.combine_tab.grid_rowconfigure(1, weight=1) # CSS input
        self.combine_tab.grid_rowconfigure(2, weight=1) # JS input
        self.combine_tab.grid_rowconfigure(3, weight=0) # Combine button row
        self.combine_tab.grid_rowconfigure(4, weight=2) # Combined Output (give more space)

        # --- Inputs ---
        self.html_input_tb = self._create_labeled_textbox(self.combine_tab, 0, "HTML Input:",
                                                          [("HTML files", "*.html"), ("All files", "*.*")], ".html")
        self.css_input_tb = self._create_labeled_textbox(self.combine_tab, 1, "CSS Input:",
                                                         [("CSS files", "*.css"), ("All files", "*.*")], ".css")
        self.js_input_tb = self._create_labeled_textbox(self.combine_tab, 2, "JavaScript Input:",
                                                        [("JavaScript files", "*.js"), ("All files", "*.*")], ".js")

        # --- Action Button ---
        combine_button = ctk.CTkButton(self.combine_tab, text="Combine into Single HTML", command=self._perform_combine)
        combine_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # --- Output ---
        self.combined_output_tb = self._create_output_textbox(self.combine_tab, 4, "Combined HTML Output:",
                                                              [("HTML files", "*.html"), ("All files", "*.*")], ".html")

    def _create_extract_tab(self):
        self.extract_tab.grid_columnconfigure(0, weight=1)
        # Configure rows
        self.extract_tab.grid_rowconfigure(0, weight=2) # Combined Input (more space)
        self.extract_tab.grid_rowconfigure(1, weight=0) # Extract button
        self.extract_tab.grid_rowconfigure(2, weight=1) # HTML output
        self.extract_tab.grid_rowconfigure(3, weight=1) # CSS output
        self.extract_tab.grid_rowconfigure(4, weight=1) # JS output

        # --- Input ---
        self.extract_input_tb = self._create_labeled_textbox(self.extract_tab, 0, "Combined HTML Input:",
                                                            [("HTML files", "*.html"), ("All files", "*.*")], ".html")

        # --- Action Button ---
        extract_button = ctk.CTkButton(self.extract_tab, text="Extract Components", command=self._perform_extract)
        extract_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # --- Outputs ---
        self.extracted_html_tb = self._create_output_textbox(self.extract_tab, 2, "Extracted HTML Structure:",
                                                             [("HTML files", "*.html"), ("All files", "*.*")], ".html")
        self.extracted_css_tb = self._create_output_textbox(self.extract_tab, 3, "Extracted CSS:",
                                                            [("CSS files", "*.css"), ("All files", "*.*")], ".css")
        self.extracted_js_tb = self._create_output_textbox(self.extract_tab, 4, "Extracted JavaScript:",
                                                           [("JavaScript files", "*.js"), ("All files", "*.*")], ".js")

    # --- File Operations ---
    def _load_file_to_textbox(self, textbox, file_types):
        filepath = filedialog.askopenfilename(
            title="Open File",
            filetypes=file_types
        )
        if not filepath:
            return # User cancelled

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            # Enable textbox, clear, insert, disable again if needed (or just clear/insert if always editable)
            textbox.configure(state="normal") # Enable to insert
            textbox.delete("1.0", "end")
            textbox.insert("1.0", content)
            # Output textboxes should remain editable for copying, but disable for direct typing?
            # Or keep them normal. Let's keep inputs normal.

        except Exception as e:
            messagebox.showerror("Error Reading File", f"Failed to read file:\n{filepath}\n\nError: {e}")

    def _save_textbox_to_file(self, textbox, default_extension, file_types):
        content = textbox.get("1.0", "end-1c") # Get all text except trailing newline
        if not content:
            messagebox.showwarning("Empty Content", "There is nothing to save.")
            return

        filepath = filedialog.asksaveasfilename(
            title="Save File As",
            defaultextension=default_extension,
            filetypes=file_types
        )
        if not filepath:
            return # User cancelled

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            # Optionally show success message
            # messagebox.showinfo("File Saved", f"Content saved to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error Saving File", f"Failed to save file:\n{filepath}\n\nError: {e}")

    # --- Core Logic Callbacks ---
    def _perform_combine(self):
        html_in = self.html_input_tb.get("1.0", "end-1c")
        css_in = self.css_input_tb.get("1.0", "end-1c")
        js_in = self.js_input_tb.get("1.0", "end-1c")

        try:
            combined_html = combine_html_css_js(html_in, css_in, js_in)

            self.combined_output_tb.configure(state="normal") # Enable writing
            self.combined_output_tb.delete("1.0", "end")
            self.combined_output_tb.insert("1.0", combined_html)
            self.combined_output_tb.configure(state="disabled") # Make read-only after insert

        except Exception as e:
             messagebox.showerror("Combine Error", f"An error occurred during combination:\n{e}")
             # Clear output on error? Optional.
             self.combined_output_tb.configure(state="normal")
             self.combined_output_tb.delete("1.0", "end")
             self.combined_output_tb.configure(state="disabled")


    def _perform_extract(self):
        combined_in = self.extract_input_tb.get("1.0", "end-1c")

        if not combined_in.strip():
             messagebox.showwarning("Empty Input", "Please load or paste combined HTML content first.")
             return

        try:
            html_out, css_out, js_out = extract_html_css_js(combined_in)

            # Update HTML output
            self.extracted_html_tb.configure(state="normal")
            self.extracted_html_tb.delete("1.0", "end")
            self.extracted_html_tb.insert("1.0", html_out)
            self.extracted_html_tb.configure(state="disabled")

            # Update CSS output
            self.extracted_css_tb.configure(state="normal")
            self.extracted_css_tb.delete("1.0", "end")
            self.extracted_css_tb.insert("1.0", css_out)
            self.extracted_css_tb.configure(state="disabled")

            # Update JS output
            self.extracted_js_tb.configure(state="normal")
            self.extracted_js_tb.delete("1.0", "end")
            self.extracted_js_tb.insert("1.0", js_out)
            self.extracted_js_tb.configure(state="disabled")

        except Exception as e:
             messagebox.showerror("Extract Error", f"An error occurred during extraction:\n{e}")
             # Clear outputs on error
             for tb in [self.extracted_html_tb, self.extracted_css_tb, self.extracted_js_tb]:
                 tb.configure(state="normal")
                 tb.delete("1.0", "end")
                 tb.configure(state="disabled")


# --- Run the Application ---
if __name__ == "__main__":
    app = HTMLToolApp()
    app.mainloop()
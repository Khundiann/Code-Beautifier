# Code Beautifier 1.0

# Copyright (C) <2024>  <khundian.twitch@gmail.com>
# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import re
import Tkinter as tk
from collections import defaultdict

use_spaces = False  # Default flag indicating whether spaces are used for indentation
space_count = 1  # Default number of spaces used for each indentation level
comment_characters = ["#"]  # Default character used to denote comments in the code

# Constants for file paths and settings
open_settings_window = "code_beautifier_settings"  # String to open the settings window
settings_folder = "plugins/Config/PythonScript/scripts/Code Beautifier"  # Folder containing language settings files
language_settings = defaultdict(set)  # Default dictionary to store language settings


def load_keyword_groups(file_path):
    """
    Load keyword groups from a file.

    Args:
        file_path (str): The path to the file containing keyword groups.

    Returns:
        dict or None: A dictionary containing keyword groups, where keys are group names and values are sets of keywords,
            or None if no keyword groups were found in the file.

    Raises:
        Exception: If an error occurs while loading the keywords.
    """
    try:
        # Open the file for reading
        with open(file_path, "r") as f:
            # Initialize an empty dictionary to store keyword groups
            keyword_groups = defaultdict(set)
            current_group = None
            # Iterate through each line in the file
            for line in f:
                # Strip whitespace from the line
                line = line.strip()
                # Skip comments and empty lines
                if line.startswith("#") or not line:
                    continue
                # Check if the line indicates the start of a new group
                if line.startswith("Indent"):
                    # Extract the group name
                    current_group = line.split(":")[0]
                # If not a new group, add the line to the current group
                elif current_group:
                    keyword_groups[current_group].add(line)
            # Check if any keyword groups were found
            if not any(keyword_groups.values()):
                return None
            return keyword_groups
    # Handle any exceptions that occur during the process
    except Exception as e:
        print("Error loading keywords :", e)
        return None


def load_language_settings():
    """
    Load language settings from configuration files.

    This function iterates through files in the specified folder (settings_folder) that start with "keyword_groups_"
    and have a ".txt" extension. It extracts the language name from the file name, loads keyword groups using the
    load_keyword_groups function, and updates the global language_settings dictionary with the loaded settings.
    Additionally, it reads specific settings from each file, such as UseSpaces, SpaceCount, and CommentCharacters,
    and updates the language_settings dictionary accordingly.

    Global Variables:
        language_settings (dict): A dictionary containing language settings, where keys are language names and values
            are dictionaries containing keyword groups, UseSpaces flag, SpaceCount, and CommentCharacters.

    Raises:
        Exception: If an error occurs while loading the settings.
    """
    global language_settings
    # Get the folder path where language settings files are stored
    folder_path = os.path.join(settings_folder)
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # Iterate through files in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file is a language settings file
        if file_name.startswith("keyword_groups_") and file_name.endswith(".txt"):
            # Extract the language name from the file name
            lang_name_parts = (
                file_name.replace("keyword_groups_", "").replace(".txt", "").split("_")
            )
            lang_name_parts = [part for part in lang_name_parts if part]
            lang_name = " ".join(lang_name_parts)
            lang_name = lang_name.replace("udf - ", "").strip()
            # Get the full path to the settings file
            settings_file_path = os.path.join(folder_path, file_name)
            # Load keyword groups from the settings file
            keyword_groups = load_keyword_groups(settings_file_path)
            # Update language_settings if keyword groups are found
            if keyword_groups:
                if lang_name not in language_settings:
                    language_settings[lang_name] = {}
                language_settings[lang_name].update(keyword_groups)
                try:
                    # Read specific settings from the file and update language_settings
                    with open(settings_file_path, "r") as f:
                        for line in f:
                            if line.startswith("UseSpaces:"):
                                use_spaces = bool(int(line.split(":")[1].strip()))
                                language_settings[lang_name]["UseSpaces"] = use_spaces
                            elif line.startswith("SpaceCount:"):
                                space_count = int(line.split(":")[1].strip())
                                language_settings[lang_name]["SpaceCount"] = space_count
                            elif line.startswith("CommentCharacters:"):
                                comment_characters = line.split(":")[1].strip().split()
                                language_settings[lang_name][
                                    "CommentCharacters"
                                ] = comment_characters
                except Exception as e:
                    # Print an error message if an error occurs while loading settings
                    print("Error loading settings for", lang_name, ":", e)


# Load language settings when the script is executed
load_language_settings()


def get_settings_file_path(lang_name):
    """
    Get the path to the settings file for a specific language.

    This function constructs the file path for the settings file corresponding to the given language name. It replaces
    spaces and the prefix "udf - " in the language name with underscores. Then, it constructs the file name using the
    format "keyword_groups_{lang_name}.txt". The function checks if the folder specified by settings_folder exists,
    and if not, it creates the folder. It then checks if the settings file exists, and if not, it creates the file
    with default settings.

    Args:
        lang_name (str): The name of the language.

    Returns:
        str or None: The path to the settings file if it exists or is successfully created, otherwise None.

    Raises:
        Exception: If an error occurs while creating the settings folder.
    """
    # Replace spaces and "udf - " prefix in the language name with underscores
    lang_name = lang_name.replace(" ", "_")
    lang_name = lang_name.replace("udf - ", "")
    # Construct the folder path for keyword groups
    keyword_groups_folder = os.path.join(settings_folder)
    # Construct the file name for the settings file
    settings_file_name = "keyword_groups_" + lang_name + ".txt"
    # Construct the full path to the settings file
    keyword_groups_file = os.path.join(keyword_groups_folder, settings_file_name)
    # Check if the settings folder exists, and create it if not
    if not os.path.exists(keyword_groups_folder):
        try:
            os.makedirs(keyword_groups_folder)
        except Exception as e:
            # Print an error message if folder creation fails
            print("Error creating settings folder :", e)
            return None
    # Check if the settings file exists, and create it with default settings if not
    if not os.path.exists(keyword_groups_file):
        with open(keyword_groups_file, "w") as f:
            f.write(
                "# Code Beautifier settings file for "
                + lang_name.capitalize()
                + "\n# Do not edit this file unless you know what you're doing!"
                + "\n\nIndentRight:\n\nIndentLeft:\n\nIndentBoth:\n\nIndentNone:\n\n"
            )
    # Return the path to the settings file
    return keyword_groups_file


def get_languages_starting_with(letter):
    """
    Get a list of languages starting with a specific letter.

    This function searches for language settings files in the folder specified by `settings_folder`. It iterates
    through the files in the folder and extracts the language names from the file names. If a file name starts with
    "keyword_groups_" and ends with ".txt", it extracts the language name, removes the prefix "keyword_groups_" and
    the file extension ".txt", splits the name by underscores, removes any empty parts, joins the parts with spaces,
    and removes the prefix "udf - " if present. If the resulting language name starts with the specified letter,
    it adds it to the list of languages.

    Args:
        letter (str): The letter to search for at the beginning of language names.

    Returns:
        list: A list of languages whose names start with the specified letter.
    """
    # Initialize an empty list to store languages
    languages = []
    # Construct the folder path for language settings files
    folder_path = os.path.join(settings_folder)
    # Check if the folder exists, and create it if not
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # Iterate through the files in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file name starts with "keyword_groups_" and ends with ".txt"
        if file_name.startswith("keyword_groups_") and file_name.endswith(".txt"):
            # Extract the language name from the file name
            lang_name_parts = (
                file_name.replace("keyword_groups_", "").replace(".txt", "").split("_")
            )
            # Remove any empty parts from the language name
            lang_name_parts = [part for part in lang_name_parts if part]
            # Join the parts of the language name with spaces
            lang_name = " ".join(lang_name_parts)
            # Remove the prefix "udf - " if present and strip any leading or trailing whitespace
            lang_name = lang_name.replace("udf - ", "").strip()
            # Check if the language name starts with the specified letter
            if lang_name.startswith(letter):
                # Add the language name to the list of languages
                languages.append(lang_name)
    # Return the list of languages
    return languages


def is_comment(line, comment_characters):
    """
    Check if a line is a comment based on the provided comment characters.

    Args:
        line (str): The line to check.
        comment_characters (iterable): Iterable containing characters used for comments.

    Returns:
        bool: True if the line is a comment, False otherwise.

    """
    return any(line.strip().startswith(comment) for comment in comment_characters)


def adjust_keyword_capitalization(line, keyword_groups):
    """
    Adjusts the capitalization of keywords in the given line based on the provided keyword groups.
    This function preserves punctuation marks and capitalizes keywords accordingly.

    Args:
        line (str): The line to adjust.
        keyword_groups (dict): A dictionary containing keyword groups where keys are group names and values are sets of keywords.

    Returns:
        str: The adjusted line with proper capitalization for keywords.
    """
    # Create a dictionary mapping lowercase keywords to their original form
    keyword_dict = {}
    for group_keywords in keyword_groups.values():
        for keyword in group_keywords:
            keyword_dict[keyword.lower()] = keyword

    # Adjust the capitalization of keywords while preserving punctuation marks
    adjusted_line = ""
    current_word = ""
    for char in line:
        if char.isalnum() or char == "_":
            # Build the current word character by character
            current_word += char
        else:
            if current_word.lower() in keyword_dict:
                # Replace the current word with its original form if it's a keyword
                adjusted_line += keyword_dict[current_word.lower()]
            else:
                # Preserve the current word if it's not a keyword
                adjusted_line += current_word
            # Append the current character (punctuation mark) to the adjusted line
            adjusted_line += char
            # Reset the current word
            current_word = ""
    # Handle the last word in the line
    if current_word.lower() in keyword_dict:
        adjusted_line += keyword_dict[current_word.lower()]
    else:
        adjusted_line += current_word

    return adjusted_line


def compile_keyword_regex(keywords):
    """
    Compile a regular expression pattern for matching keywords.

    This function takes a list of keywords as input and compiles a regular expression pattern to match any of
    these keywords in a string. The resulting compiled regex pattern is case-insensitive, meaning it will match
    keywords regardless of their capitalization.

    Args:
        keywords (list): A list of keywords to be included in the regular expression pattern.

    Returns:
        Pattern: A compiled regular expression pattern object.

    """
    # Construct a regex pattern to match any of the keywords using a non-capturing group
    pattern = r"\b(?:{})\b".format("|".join(re.escape(keyword) for keyword in keywords))
    # Compile the regex pattern with the IGNORECASE flag to make it case-insensitive
    return re.compile(pattern, flags=re.IGNORECASE)


def create_language_tab(language_window, language, keyword_groups, settings_file_path):
    """
    Create a tab for configuring language-specific settings.

    This function creates a tab within a given Tkinter window for configuring language-specific settings.
    It allows users to set indentation styles, space counts, and comment characters for the specified language.

    Args:
        language_window (tk.Tk): The Tkinter window in which the tab will be created.
        language (str): The name of the language for which settings are being configured.
        keyword_groups (dict): A dictionary containing keyword groups for the language.
        settings_file_path (str): The path to the settings file for the language.

    """
    global comment_characters_entry, use_spaces, space_count

    # Define the groups of indentation styles
    indent_groups = ["IndentRight", "IndentLeft", "IndentBoth", "IndentNone"]

    # Create a frame for the tab
    frame = tk.Frame(language_window)
    frame.pack(fill=tk.BOTH, expand=True)

    # Add label and entry for setting comment characters
    comment_characters_label = tk.Label(frame, text="Comment Characters:")
    comment_characters_label.grid(
        row=len(indent_groups), column=0, padx=10, pady=1, sticky="w"
    )
    comment_characters_entry = tk.Entry(frame, width=40)
    comment_characters_entry.grid(
        row=len(indent_groups) + 1, column=0, padx=10, pady=12, sticky="w"
    )

    # Function to load comment characters from settings file
    def load_comment_characters():
        global comment_characters
        try:
            with open(settings_file_path, "r") as f:
                for line in f:
                    if line.startswith("CommentCharacters:"):
                        comment_characters = line.split(":")[1].strip().split()
                        comment_characters_entry.delete(0, tk.END)
                        comment_characters_entry.insert(
                            tk.END, " ".join(comment_characters)
                        )
                        break
        except IOError:
            print("Settings file not found.")
        except Exception as e:
            print("Error loading comment characters:", e)

    load_comment_characters()

    # Function to save comment characters to settings file
    def save_comment_characters():
        try:
            with open(settings_file_path, "r") as f:
                lines = f.readlines()
            with open(settings_file_path, "w") as f:
                for line in lines:
                    if not line.startswith("CommentCharacters:"):
                        f.write(line)
                f.write("CommentCharacters: {}\n".format(" ".join(comment_characters)))
        except IOError:
            print("Settings file not found.")
        except Exception as e:
            print("Error saving comment characters:", e)

    # Function to update comment characters
    def update_comment_characters():
        global comment_characters
        comment_characters = [
            char.strip() for char in re.split(r",|\s", comment_characters_entry.get())
        ]
        save_comment_characters()

    # Function to save settings to file
    def save_settings_file(settings_file_path):
        global language_settings, use_spaces, space_count
        with open(settings_file_path, "w") as f:
            f.write("# Code Beautifier settings file for {}\n".format(language))
            f.write("# Do not edit this file unless you know what you're doing!\n\n")
            f.write("CommentCharacters: {}\n".format(" ".join(comment_characters)))
            f.write("UseSpaces: {}\n".format(int(use_spaces)))
            f.write("SpaceCount: {}\n\n".format(space_count))
            for group, keywords in keyword_groups.items():
                if group not in ["CommentCharacters", "UseSpaces", "SpaceCount"]:
                    f.write("{}:\n{}\n\n".format(group, "\n".join(keywords)))
        lang_name = (
            os.path.basename(settings_file_path)
            .replace("keyword_groups_", "")
            .replace(".txt", "")
            .replace("_", " ")
        )
        lang_name = lang_name.replace("udf - ", "").strip()
        language_settings[lang_name] = keyword_groups
        language_settings[lang_name]["UseSpaces"] = use_spaces
        language_settings[lang_name]["SpaceCount"] = space_count
        language_settings[lang_name]["CommentCharacters"] = comment_characters

    # Function to save settings when focus is lost
    def save_on_focus_out(event):
        update_space_count()
        update_comment_characters()
        for i, group in enumerate(indent_groups):
            keyword_groups[group] = (
                text_widgets[i].get("1.0", "end").strip().split("\n")
            )
        save_settings_file(settings_file_path)

    # Function to save settings when window is closed
    def save_on_close():
        update_space_count()
        update_comment_characters()
        save_on_focus_out(None)
        language_window.destroy()

    # Set protocol to save settings when window is closed
    language_window.protocol("WM_DELETE_WINDOW", save_on_close)

    # Create text widgets for each indentation style group
    text_widgets = []
    scrollbars = []
    for i, group in enumerate(indent_groups):
        row = i // 2 * 2
        col = i % 2 * 2
        label = tk.Label(frame, text=group)
        label.grid(row=row, column=col, padx=10, pady=10, sticky="n")
        sorted_keywords = sorted(keyword_groups.get(group, []))
        text_widget = tk.Text(frame, width=40, height=10)
        text_widget.insert(tk.END, "\n".join(sorted_keywords))
        text_widget.grid(row=row + 1, column=col, padx=10, pady=(0, 10), sticky="ew")
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.grid(row=row + 1, column=col + 1, sticky="ns")
        text_widget.config(yscrollcommand=scrollbar.set)
        text_widget.bind("<FocusOut>", save_on_focus_out)
        text_widgets.append(text_widget)
        scrollbars.append(scrollbar)

    # Add space count label and spinbox
    space_count_label = tk.Label(frame, text="Space Count:")
    space_count_label.grid(
        row=len(indent_groups), columnspan=3, padx=50, pady=12, sticky="e"
    )
    space_count_spinbox = tk.Spinbox(
        frame,
        from_=1,
        to=8,
        increment=1,
        width=5,
        command=lambda: save_settings_file(settings_file_path),
    )
    space_count_spinbox.grid(
        row=len(indent_groups), columnspan=3, padx=1, pady=12, sticky="e"
    )

    # Function to update space count
    def update_space_count():
        global space_count
        space_count = int(space_count_spinbox.get())
        save_settings_file(settings_file_path)

    space_count_spinbox.bind("<FocusOut>", lambda event: update_space_count())

    # Function to toggle indent option
    def toggle_indent_option():
        global use_spaces
        use_spaces = not use_spaces
        save_settings_file(settings_file_path)
        if use_spaces:
            indent_option_checkbutton.select()
        else:
            indent_option_checkbutton.deselect()

    # Create checkbutton for using spaces
    indent_option_var = tk.IntVar()
    indent_option_checkbutton = tk.Checkbutton(
        frame,
        text="Use Spaces",
        variable=indent_option_var,
        command=toggle_indent_option,
    )
    indent_option_checkbutton.grid(
        row=len(indent_groups), columnspan=3, padx=10, pady=10, sticky="s"
    )

    # Function to initialize use spaces checkmark
    def initialize_use_spaces_checkmark():
        global use_spaces
        if "UseSpaces" in language_settings.get(language, {}):
            use_spaces = language_settings[language]["UseSpaces"]
            if use_spaces:
                indent_option_checkbutton.select()
            else:
                indent_option_checkbutton.deselect()

    # Function to initialize space count spinbox
    def initialize_space_count_spinbox():
        global space_count
        if "SpaceCount" in language_settings.get(language, {}):
            space_count = language_settings[language]["SpaceCount"]
            space_count_spinbox.delete(0, tk.END)
            space_count_spinbox.insert(0, space_count)

    initialize_use_spaces_checkmark()
    initialize_space_count_spinbox()
    load_comment_characters()
    language_window.bind("<FocusOut>", lambda event: save_on_focus_out(None))
    language_window.protocol("WM_DELETE_WINDOW", save_on_close)


def create_language_buttons(letter, root_geometry):
    """
    Create buttons for languages starting with a specific letter.

    This function creates buttons for each language starting with the specified letter.
    When a button is clicked, it triggers the 'language_button_click' function.

    Args:
        letter (str): The starting letter of the languages.
        root_geometry (str): The geometry string for the Tkinter window.

    """
    # Create a new Tkinter window
    language_window = tk.Tk()
    language_window.title("Languages Starting with %s" % letter)
    language_window.geometry(root_geometry)
    language_window.attributes("-topmost", True)

    # Get the list of languages starting with the specified letter
    languages = get_languages_starting_with(letter)

    # Create a button for each language
    for language in languages:
        language = language.replace(" ", "_")  # Replace spaces with underscores
        btn = tk.Button(
            language_window,
            text=language,
            command=lambda l=language: language_button_click(l, language_window),
        )
        btn.pack()  # Pack the button into the window

    # Run the Tkinter event loop
    language_window.mainloop()


def language_button_click(language, language_window):
    """
    Event handler for when a language button is clicked.

    Args:
        language (str): The language selected by the user.
        language_window (tk.Tk): The parent window containing the language buttons.

    """
    tab = tk.Toplevel(language_window)
    tab.title(language)
    tab.attributes("-topmost", True)
    settings_file_path = get_settings_file_path(language)
    try:
        keyword_groups = language_settings.get(language, {})
        create_language_tab(tab, language, keyword_groups, settings_file_path)
    except IOError:
        return


def create_alphabetical_window():
    """
    Create a window with alphabetical selection buttons.

    This function creates a Tkinter window containing buttons for each letter of the alphabet.
    When a letter button is clicked, it triggers the 'create_language_buttons' function to display
    languages starting with that letter.

    """
    # Create a new Tkinter window
    root = tk.Tk()
    root_geometry = "350x400"
    root.geometry(root_geometry)
    root.attributes("-topmost", True)
    root.configure()
    root.title("Alphabetical Selection")

    # Define button layout parameters
    start_x = 30
    start_y = 30
    button_width = 50
    button_height = 50
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Create buttons for each letter
    for idx, letter in enumerate(letters):
        # Define the button with the corresponding letter
        btn = tk.Button(
            root,
            text=letter,
            font=("consolas", 12, "normal"),
            command=lambda l=letter: create_language_buttons(l, root_geometry),
        )
        # Calculate button position based on index
        row = idx // 5
        col = idx % 5
        # Place the button in the window
        btn.place(
            x=start_x + col * (button_width + 10),
            y=start_y + row * (button_height + 10),
            width=button_width,
            height=button_height,
        )

    # Run the Tkinter event loop
    root.mainloop()


def on_char_add(args):
    """
    Event handler for adding characters in the editor.

    This function is triggered whenever a character is added in the editor. It checks if the added character
    triggers the opening of the alphabetical window for language selection. If so, it opens the alphabetical window.

    Args:
        args: Additional arguments passed to the event handler.

    """
    global show_alphabetical_window

    # Get the current cursor position in the editor
    pos = editor.getCurrentPos()
    # Extract the word around the cursor position
    char_search_word = editor.getTextRange(
        editor.wordStartPosition(pos, True), editor.wordEndPosition(pos, True)
    ).lower()

    # Check if the word contains the trigger for opening the alphabetical window
    if open_settings_window in char_search_word:
        show_alphabetical_window = True
    else:
        show_alphabetical_window = False

    # If the trigger is present, open the alphabetical window
    if show_alphabetical_window:
        create_alphabetical_window()


def beautify_code(args):
    """
    Beautify the code in the editor based on language settings.

    Args:
        args (dict): Additional arguments passed to the function.

    """
    try:
        current_bufferID = args["bufferID"]
        lang_type = notepad.getLangType(current_bufferID)
        lang_name = (
            notepad.getLanguageName(lang_type)
            if lang_type == LANGTYPE.USER
            else str(editor.getLexerLanguage()).upper()
        )
        lang_name = lang_name.replace("udf - ", "")
        keyword_groups = language_settings.get(lang_name, {})

        # If no keyword groups found, return
        if not keyword_groups:
            return

        # Extract relevant settings from language settings
        indent_groups = {
            group: keywords
            for group, keywords in keyword_groups.items()
            if group.startswith("Indent")
        }
        comment_characters = keyword_groups.get("CommentCharacters", set())
        use_spaces = language_settings.get(lang_name, {}).get("UseSpaces", False)
        space_count = language_settings.get(lang_name, {}).get("SpaceCount", 1)

        # Get the current document from the editor
        current_doc = editor.getText()
        leading_whitespace_pattern = re.compile(r"^\s+")
        keyword_patterns = {
            group: compile_keyword_regex(keywords)
            for group, keywords in indent_groups.items()
        }
        beautified_lines = []
        current_indentation = 0

        # Iterate through each line in the document
        for line in current_doc.split("\n"):
            if is_comment(line, comment_characters):
                # Handle comment lines
                indentation = (
                    " " * space_count * current_indentation
                    if use_spaces
                    else "\t" * current_indentation
                )
                beautified_lines.append(indentation + line.strip())
            else:
                if line.strip():
                    # Handle non-empty lines
                    indent_right, indent_left, indent_both, indent_none = (
                        False,
                        False,
                        False,
                        False,
                    )
                    # Check for keyword patterns
                    for group, pattern in keyword_patterns.items():
                        if pattern.search(line):
                            if group == "IndentRight":
                                indent_right = True
                            elif group == "IndentLeft":
                                indent_left = True
                            elif group == "IndentBoth":
                                indent_both = True
                            elif group == "IndentNone":
                                indent_none = True
                    # Adjust indentation based on patterns
                    if indent_left and not indent_both:
                        current_indentation = max(0, current_indentation - 1)
                    elif indent_both:
                        current_indentation = max(0, current_indentation - 1)
                    indentation = (
                        " " * space_count * current_indentation
                        if use_spaces
                        else "\t" * current_indentation
                    )
                    line = re.sub(leading_whitespace_pattern, "", line)
                    line = adjust_keyword_capitalization(line, indent_groups)
                    beautified_lines.append(indentation + line)
                    if indent_right or (indent_both and line.strip()):
                        current_indentation += 1
                    elif indent_none:
                        pass
                else:
                    beautified_lines.append("")
        if beautified_lines and not beautified_lines[-1]:
            beautified_lines = beautified_lines[:-1]
        beautified_lines.append("")
        beautified_code = "\n".join(beautified_lines)
        editor.setText(beautified_code)
    except Exception as e:
        print("Error in beautify_code:", e)
        return


def check_and_create_settings_file(args):
    """
    Check and create the settings file if it doesn't exist.

    Args:
        args (dict): Additional arguments passed to the function.

    """
    bufferID = args["bufferID"]
    lang_name = "unknown"
    try:
        # Get language type
        lang_type = notepad.getLangType(bufferID)

        # Check if it's a user-defined language
        if lang_type == LANGTYPE.USER:
            lang_name = notepad.getLanguageName(lang_type)
            lang_name = lang_name.replace(" ", "_")
        else:
            lang_name = str(editor.getLexerLanguage()).upper()

        # Remove 'udf - ' prefix if present
        if lang_name.startswith("udf_-_"):
            lang_name = lang_name.replace("udf_-_", "")
        settings_file = get_settings_file_path(lang_name)
    except Exception as e:
        print("Error settings file not found :", e)
        return


# Callback to trigger the 'on_char_add' function whenever a character is added in the editor
editor.callback(on_char_add, [SCINTILLANOTIFICATION.CHARADDED])

# Callback to trigger the 'beautify_code' function before saving a file in Notepad++
notepad.callback(beautify_code, [NOTIFICATION.FILEBEFORESAVE])

# Callback to trigger the 'check_and_create_settings_file' function when the language changes or a buffer is activated
notepad.callback(
    check_and_create_settings_file,
    [
        NOTIFICATION.LANGCHANGED,
        NOTIFICATION.BUFFERACTIVATED,
    ],
)

# Code Beautifier

Maintaining clean and organized code is paramount for readability, collaboration, and overall efficiency. However, manually formatting code can be time-consuming and error-prone. This is where the **Code Beautifier** script can lend a hand, designed to effortlessly enhance the structure and appearance of your code within Notepad++. Feel free to use any parts of the code in the script as long as its for opensource purposes.

## Features:

- **Language-Specific Settings:** Code Beautifier adapts to all current and future programming languages supported in Notepad++, including User Defined Languages. Allowing you to customize indentation style, spacing preference, and comment characters for each language.

- **Keyword Grouping:** Organize your code by categorizing keywords into logical groups, such as "IndentLeft", "IndentRight", "IndentBoth" and "IndentNone". Code Beautifier provides a seamless interface for managing these keyword groups.

- **Automatic Code Formatting:** Simply by saving your file, Code Beautifier automatically analyzes your code and applies the predefined formatting rules based on the language settings, significantly reducing manual effort and potential errors.

- **Keyword capitalization:** On top of checking the indentation of your code, it will also capitalize any keywords entered in the "Indent" groups in the language settings window. Any keyword found in the code page will be capitalized exactly as it is written in the keyword groups settings, further enhancing readability.

- **Intuitive GUI:** The graphical user interface (GUI) of Code Beautifier provides a user-friendly environment for configuring language-specific settings, making it a breeze to configure.

## README:

### 1. Installation:

- Ensure you have Notepad++ installed on your system.
- Download and install the PythonScript plugin for Notepad++ if you haven't already.
- Copy the code inside the code.beautifier.py file and paste code into a new *.py file called "code.beautifier".
- Place the script file in the appropriate folder in your Notepad++ installation directory.
**"plugins\Config\PythonScript\scripts"**

### 2. Using Code Beautifier:

- Open Notepad++ and navigate to the PythonScript menu.
- Select "Scripts" and then choose code beautifier from the list. Or you can choose to configure Notepad++ to load the script "ATSTARTUP" in the PythonScript "Configuration", That way you don't have to run it yourself each time when you start up Notepad++.
- The script will now run in the background while you are working, and when you have configured settings for the language you're using it will beautify the code based on your chosen settings when you save your file.
- When you change languages or change document in Notepad++, the script will check the **"plugins\Config\PythonScript\scripts"** folder if there is folder called "Code Beautifier" and if a settings file exists for this language and if not create a folder and settings file.

### 3. Configuring Language Settings:

- Type the keyword **"code_beautifier_settings"** in any document in Notepad++ while the script is running and you'll be presented with a window with buttons for each letter of the alphabet.
- Click on the letter corresponding to the language you're working with.
- This action will open another window displaying a list of languages starting with the selected letter.
- Click on the desired language to proceed.

### 4. Indentation Groups Explained

- **IndentRight:** when a keyword that belongs to this group is detected in the codepage, pushes the next line in the editor 1 indent level to the right.
- **IndentLeft:** when a keyword that belongs to this group is detected in the codepage, pulls the current line of the keyword in the editor 1 indent level to the left.
- **IndentBoth:** when a keyword that belongs to this group is detected in the codepage, pulls the current line of the keyword in the editor 1 indent level to the left and pushes the next line in the editor 1 indent level to the right.
- **IndentNone:** when a keyword that belongs to this group is detected in the codepage, does nothing in terms of indentation but is used for the capitalization of keywords feature.

### 5. Customizing Settings:

- In the language-specific settings window, you can customize various aspects such as indentation style, spacing preference, and comment characters.
- Use the provided options and input fields to tailor the settings according to your preferences.
- When entering keywords in the text widgets, the keywords should be in a long list, each keyword on a new line.
- Comment characters should be separated by a space or a comma,

### 6. Saving Settings:

- No interaction is needed for saving settings, the script saves on losing focus and closing of the language-specific window.

### 7. Automated Code Formatting:

- Once all your settings are configured for the language you are using, simply saving the document you are working on will apply the beautification process.

### 8.  Media:

![2024-02-17 23_44_32-_new 8 - Notepad++](https://github.com/Khundiann/code-beautifier/assets/151635111/a14a4898-d149-43e8-bc77-02630df198f9)


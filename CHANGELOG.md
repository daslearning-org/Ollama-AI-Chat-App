# Changelogs

## v0.2.0
- Now the app is `multi-threaded`, the call to llm is now `async` & wont block the main app thread.
- Removing `<think>` tags from `Deepseek` responses. Thanks to [Alejandro Caro](https://github.com/Lelale01) for the fixed code.
- Adding keyboard suggestions for text input in chatbot.
- Added a top-bar menu with documentation, update and other required links.
- Adding a copy button to copy the entire response from as `RST` document text.

## v0.1.4
- Fixing the code block copy which now removes the markup tags from the copied text.

## v0.1.3
- Updating the screen file names (app remains same)
- Adding the Computer application build steps using `pyinstaller`

## v0.1.2
- The first version of the working chatbot app.
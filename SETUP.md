# Setup Instructions

* Clone the repository. 
* Set up your editor/IDE. If using VS Code:
    * Open the repository folder (not a subfolder) as a workspace. 
    * Open the *workspace settings* and add, e.g.: 
        ```json
        {   "python.linting.enabled": true,
            "python.linting.pylintEnabled": true,
            "python.linting.pylintUseMinimalCheckers": false,
            "editor.formatOnSave": true,
            "python.linting.pylintArgs": [
                "--disable=C0103",
                "--disable=C0111"]}
        ```
* Create a Python virtual environment for this project. 
    * Note: ensure `python` refers to the Python 2.x executable. 
    * Follow [these instructions](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/). 
    * Recommended: create it *outside* the repository folders, to prevent its files from appearing in search. Otherwise, at least exclude it from source control. 
* Load the required packages into the virtual environment: `python -m pip install -r requirements.txt`, where `python` is the executable under `<environment>\Scripts'.
* Ensure that the code will be executed using the Python interpreter inside the virtual environment. If using VS Code:
    * In workspace settings, set `pythonPath`, e.g.:
        ```json
        {
            "python.pythonPath": "${workspaceFolder}\\..\\my-environment\\Scripts\\python.exe"
        }
        ```
    * Configure a build task that activates the virtual environment *before* running the script, e.g.:
        ```json
        {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Run Current Script",
                    "type": "shell",
                    "command": "..\\my-environment\\Scripts\\activate & python \"${file}\"",
                    "group": {
                        "kind": "build",
                        "isDefault": true
                    }
                }
            ]
        }

        ```
        * Note: if the `activate` script will not run, try using Command Prompt instead of PowerShell as VS Code's integrated terminal. 
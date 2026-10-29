# Static Code Analysis — Issues and Fixes

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Hardcoded password | Security | From original report | A password was stored directly in the source code. | Read the password from an environment variable instead. |
| Insecure temporary file creation | Security | From original report | `tempfile.mktemp()` can create a race condition. | Use `tempfile.NamedTemporaryFile()` to securely create the report file. |
| Shell command execution | Security | From original report | `os.system()` with a constructed path can introduce command-injection risks. | Replace shell execution with a safer file-opening approach. |
| Missing module docstring | Code quality | From Pylint report | The Python module lacked a description. | Add a module-level docstring. |
| Missing function docstrings | Code quality | From Pylint report | Functions did not explain their purpose. | Add concise docstrings to functions. |
| Invalid naming conventions | Code quality | From Pylint report | Function and variable names did not follow Python naming conventions. | Rename functions and variables consistently using `snake_case`. |
| Global statement | Code quality | From Pylint report | The budget setter modified a global variable. | Return the validated budget and assign it where needed. |
| Broad exception handling | Code quality | From Pylint report | A general exception was caught unnecessarily. | Catch the specific expected exception. |
| Inefficient index iteration | Code quality | From Pylint report | The loop used `range(len(...))`. | Use `enumerate()` to access the index and item. |
| Line too long | Style | From Flake8 report | A line exceeded the 79-character limit. | Split the expression across multiple lines. |

## Summary

Pylint was used to improve code quality and naming conventions, Bandit to identify security risks, and Flake8 to enforce formatting standards. The issues were fixed and the tools were rerun to verify the changes.

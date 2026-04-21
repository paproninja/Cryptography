# Development Guide - Adding New Tools

This guide explains how to add new cryptographic tools to the project.

## Step-by-Step Instructions

1.  **Create the Script**: 
    Create a new Python file in the `scripts/` directory (e.g., `scripts/mycipher.py`).

2.  **Implement the Logic**: 
    Define a function (usually named after the cipher) that takes at least `text`, `key`, and `operation` as arguments. Handle the different operations (`encrypt`, `decrypt`, `bruteforce`, `generate`, `info`) as needed.

    ```python
    def mycipher(text=None, key=None, operation=None):
        if operation == "encrypt":
            # Encryption logic
            pass
        # ... other operations
    ```

3.  **Register the Tool**: 
    Open `tool_info.py` and add your tool's metadata to the `TOOL_INFO` dictionary.
    
    ```python
    "mytool": {
        "name": "My New Cipher",
        "operations": ["encrypt", "decrypt", "info"],
        "key_type": "str" # or "int" or None
    }
    ```

4.  **Integrate with CLI**: 
    Update `crypto.py`:
    - Add an argument for your tool in the appropriate `argument_group`.
    - Import your script at the top.
    - Add a call to your function in the `CALL TOOL FUNCTION` section.

5.  **GUI Support**: 
    The GUI in `cryptogui.py` is mostly dynamic and loads tools from `TOOL_INFO`. However, if your tool requires custom UI behavior, you may need to update the `on_operation_change` logic in `CryptoGUI`.

## Verification

After adding a tool, always verify it via the CLI:
```bash
python3 crypto.py --mytool -e -t "test text" -k "test key"
```

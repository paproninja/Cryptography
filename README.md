# Cryptography - Classical Cipher Tools

This project is a collection of classical cryptography tools, offering both a Command Line Interface (CLI) and a Graphical User Interface (GUI) to encrypt, decrypt, and perform brute-force attacks on various historical ciphers.

## 🚀 Features

- **Support for multiple ciphers:** ROT (Caesar), Substitution, Atbash, Vigenère, Rail Fence, Columnar Transposition, and Numeric Value.
- **Operations:** Encryption, decryption, key generation, and detailed tool information.
- **Dual Interface:** Use the power of the terminal or the convenience of a graphical window.
- **Flexible Input:** Enter text directly or load text files.

## 🛠️ Installation

Ensure you have Python 3 installed. To use the graphical interface, install the necessary dependencies:

```bash
pip install customtkinter CTkMessagebox
```

## 💻 Command Line Interface (CLI) Usage

The main tool is `crypto.py`. The general syntax is:

```bash
python3 crypto.py [TOOL] [OPERATION] [-t TEXT/FILE] [-k KEY/FILE]
```

### Examples:

- **Caesar Cipher (ROT):**
  ```bash
  python3 crypto.py --rot -e -t "Hello World" -k 3
  ```

- **Atbash Cipher:**
  ```bash
  python3 crypto.py --atbash -e -t "Hello World"
  ```

- **Brute Force on Rail Fence:**
  ```bash
  python3 crypto.py --railfence -b -t "HAOMUDNLO"
  ```

- **Generate a key for Substitution:**
  ```bash
  python3 crypto.py --subst -g
  ```

## 🖼️ Graphical User Interface (GUI)

To launch the graphical interface, simply run:

```bash
python3 cryptogui.py
```

The GUI allows you to select the tool and operation intuitively, facilitating the loading of files for text and keys.

## 📜 Supported Ciphers

| Tool | Operations | Key Type |
| :--- | :--- | :--- |
| **ROT** | Encrypt, Decrypt, Brute Force, Generate | Integer (int) |
| **SUBST** | Encrypt, Decrypt, Generate | 26-character string |
| **ATBASH** | Encrypt, Decrypt | N/A |
| **VIGENERE** | Encrypt, Decrypt, Generate | String (str) |
| **RAIL FENCE** | Encrypt, Decrypt, Brute Force, Generate | Integer (int) |
| **COLUMNAR** | Encrypt, Decrypt, Generate | String (str) |
| **NUMVAL** | Encrypt, Decrypt | N/A |

## 🛠️ Development

If you wish to contribute or add new tools, refer to the following guide:
- [How to Add New Tools](DEVELOPMENT.md)

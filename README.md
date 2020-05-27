# Allods Version Tools

This small python script deals with `game.version` file. It allows you to print version information and check for game files validity.
It checks files as official executables from Allods Online would do it: 
* It can check `game.version` signature (the file is signed using PKCS1 PSS signature with MD5 hash)
* It can extract the public RSA certificates stored in AOGame.exe or Launcher.exe to verify game.version
* It provides ready-to-use command to patch Launcher.exe public RSA certificate to allow you create your own `game.version` file

WARNING: `game.version` file generation is a planned feature but it's still not implemented. You can only display `game.version` content for now

## Installation

* Install Python : https://www.python.org/
* Clone this repository
* Install requirements :
    ```cmd
    python -m pip install -r requirements.txt
    ```

## Usage

To see all available commands use:

```cmd
python cli.py -h
```

To see specific help for a command use:

```cmd
python cli.py <command> -h
```

### Example

To get help for `show` command, type:
```cmd
python cli.py show -h
```

Exhaustive documentation will come later



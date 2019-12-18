import pyperclip


def memeify(value=None):
    string = value if(value != None) else pyperclip.paste()
    string2 = ""
    for c in string:
        string2 = string2 + c + " "
    pyperclip.copy(string2.strip())


if(__name__ == "__main__"):
    memeify()

import pyperclip


def memeify(clipboardContext=None):
    string = clipboardContext if(clipboardContext != None) else pyperclip.paste()
    string2 = ""
    for c in string:
        string2 = string2 + c + " "
    pyperclip.copy(string2.strip())


if(__name__ == "__main__"):
    memeify()

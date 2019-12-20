import webbrowser


def openURL(URL="https://www.google.com.au"):
    webbrowser.open(URL)


if(__name__ == "__main__"):
    # opens google.com.au if no url provided
    openURL()

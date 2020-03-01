# Mokha: Workflow Automation

![Mokha-logo](https://i.imgur.com/wHj0zg0.png)

## What is Mokha

Mokha is a Python script that can be configured; via JSON, to automate workflows.

## How does it work

The basic idea of Mokha is as follows:

1. You have a task that needs automating - maybe a tedious task or something you need to do a bunch of times.
2. You write a Python script/method that does that job.
3. You write a little bit of JSON configuration to setup the script.
4. You add your python script to the dependencies folder.
5. You run mokha.py however you want - keyboard binding, command line alias, whatever floats ya boat.

Aside from writing your scripts, you don't have to _code_ anything to make it work with Mokha. _(unless you class JSON as a coding language then I don't know how to help you.)_

## Configuration in Mokha

All the configuration in Mokha is done via JSON files. There are two main categories of configurations:

### Base Configuration

- `config.json`: This is the first file loaded by Mokha on startup. The entire purpose of this file is configure the directories of the remaining three configuration files. The default location for all three files are the root directory of the application.

### User Configuration

- `dependencies.json`: A JSON file that outlines of what files, folders, and python scripts your code requires.
- `accounts.json`: A JSON file that outlines high-level structures that outlines different groups of methods you might have, for example: I have three profiles for Home use, Independent work use, and for my main job.
- `methods.json`: JSON File that outlines the structure of all methods being run by Mokha.

The reason for splitting the types of configuration is simple. `Base Config` encapsulates anything _fundamental_ to the operation of Mokha itself while `User Config` refers to the operation of your scripts.

## Setting up Mokha

1. Clone this repo and run `pip install click` and `pip install pyperclip`. _If that doesn't work try `pip3` instead_
2. Run Mokha.py. It will automatically generate the config.json file with the default values, however, it will not generate those files/folders for you.
3. Create `accounts.json`, `methods.json` and `dependencies.json` files and a `dependencies` folder wherever you want. If you deviate from the default values in `config.json` please update them there.  
   NOTE: Please put the _absolute_ path for any files or directories outside of the root directory.

4. Add an account to the `accounts.json` file as follows:

   ### Adding an account

   `accounts.json` contains an array of json objects for which each object is an account that can contain methods.

   ```JSON
   [
       {
       "--id": "1",
       "title": "Personal",
       "functions": [
       {
           "title": "Google Calendar",
           "methodID": "open-a-website",
           "arguments": {
           "URL": "https://calendar.google.com/calendar/b/0/r/month"
           }
       },
       {
           "title": "GitHub Profile",
           "methodID": "open-a-website",
           "arguments": {
           "URL": "https://github.com/ChildishhAlbino"
           }
       },
       {
           "title": "Personal Blog",
           "methodID": "open-a-website",
           "arguments": {
           "URL": "https://childishhalbino.github.io/"
           }
       }
       ]
   }
   ]
   ```

   _An account has the following fields:_

   - `--id`: A unique identifier for this profile.
   - `title`: A title for the profile. This gets printed to the console.
   - `functions`: An array of function objects that detail the method being called and the arguments being passed for this option.

   - `function`: A function object looks like this:

     ```JSON
     {
             "title": "Google Calendar",
             "methodID": "open-a-website",
             "arguments": {
             "URL": "https://calendar.google.com/calendar/b/0/r/month"
             }
         },
     ```

     _A function object has the following fields:_

     - `title`: This is the name of the function.
     - `methodID`: This is a reference to the ID of the method this function calls.
     - `arguments`: A JSON object that has keys that equal the parameters names outline in this method's configuration. The value of said key is the argument that will be passed to the method call.

5. Now that we have an account to add methods to, let's make one!

   ### Adding methods

   Before we can add anything to Mokha, we need to write some code first - let's make a small function that just opens any URL we throw at it in the web browser.

   We can achieve this with the following Python code. Let's save it as `utilities.py` in our `dependencies` folder.

   ```Python
   def openURL(URL="https://www.google.com.au"):
       webbrowser.open(URL)
   ```

   To implement this is in Mokha - We'd use the below JSON.

   ```JSON
   {
       "--id": "open-a-website",
       "name": "openURL",
       "dependency": "utilities",
       "schema": {
       "numParams": 1,
       "parameterNames": ["URL"]
   }
   ```

   _A method has the following fields_:

   - `--id`: Some unique ID for this specific method definition. Helps keep things modular.
   - `name`: This the name of the method in Python you are defining in the Mokha configuration file. This IS case sensitive.
   - `dependency`: This is the name of Python module you are importing to run this. You always need only 1 dependency - this will be elaborated in a section below.
   - `schema`: This is an object that verifies that a shortcut that calls this method is passing the correct arguments.
   - `numParams`: This outlines the number of parameters this method expects. This will be made optional in the future.
   - `parameterNames`: An array of string that outline the expected arguments.

6. There's one last step we need to do. We have to tell Mokha to attempt to load our `utilities` dependency on startup.

   ### Adding a dependency

   To add a dependency to Mokha, you just have to modify your `dependencies.json` file. By default, it should look like this:

   ```JSON
   {
   "python": [],
   "file-system": [],
   "remote": []
   }
   ```

   As you can see, there are two fields for different types of dependencies.

   - `python`: Dependencies on Python modules or `.py` files.
   - `file-system`: Dependencies on any files your Python modules may use to achieve their goals.  
     NOTE: All file paths stored here can be either absolute or relative to the `dependencies` path.
   - `remote`: Remote dependencies are files on your PC that may not be best suited stored in your dependencies folder for whatever reason. By putting the absolute path of this file here, Mokha will check said path and copy over the file if it doesn't exist or if the remote version does not match the current version byte-for-byte.

For the purposes of our `utilities.py` module, we just have to modify the `python` dependencies as follows:

```JSON
{
"python": ["utilities"],
"file-system": [],
"remote": []
}
```

7. That's it! You can run Mokha.py and it _should_ (fingers crossed) work. You should get some console output like this:

   ```None
   Attempting to import dependencies from: E:/Documents/Dropbox/Mokha/dependencies
   ---------------------

   Filesystem dependencies loaded successfully.
   Loaded module: Utilities

   ---------------------
   Welcome to Mokha V1.0-a. This is a tool designed to enable configuration of shortcuts to python code.
   1: Personal
   Select an option:
   ```

   Upon selecting a language, you should see this:

   ```None
   Attempting to import dependencies from: E:/Documents/Dropbox/Mokha/dependencies
   ---------------------

   Filesystem dependencies loaded successfully.
   Loaded module: Utilities

   ---------------------
   Welcome to Mokha V1.0-a. This is a tool designed to enable configuration of shortcuts to python code.
   1: Personal
   Select an option: 1
   1: Google Calendar
   2: GitHub Profile
   3: Personal Blog
   Select an option:
   ```

   Upon selecting whichever option you want; you should see the respective webpage you set for that option open inside your web browser.

## Okay... but how does that work like, in code

The basic flow of the application is as follows:

1. Mokha starts and it attempts to read in `config.py`.

   - If it doesn't exist, it's creates it with the default values in place.
   - Exits the application so the user can configure the rest.

2. Mokha adds whatever path the user set as your `dependencies-path` variable to `sys.path`. Allows the user to import modules from outside the root folder of `mokha.py`

3. The application then tries to load the user's filesystem dependencies, followed by your python dependencies.

   - If Mokha successfully imports their dependencies, it will load in the remainder of their `user-config` files.
   - Else it will throw an exception and explain why.

4. Mokha then prompts the user for input on which account they want to access.

5. Mokha takes the input and finds the `account` that matches it, it then finds all the `functions` associated with it.

6. The application will prompt the user for input for which function they want to run and then finds it from their config.

7. Mokha gets the attribute that matches the selected method's `name` field inside it's `dependency` module.

8. Mokha constructs a dictionary with keys that equal the parameters outlined in the method's `schema` object and maps them to the selected functions `arguments` object.

9. Mokha changes the current directory to the `dependencies-path` value. This is to ensure that a user's scripts function as they would if they were run in isolation.

10. This dictionary is then passed as the argument to the Python function call and thanks to keyword-arguments; as long as the dictionary does not have any keys that aren't a parameter on the method (in code), the function should be called without any issues.

(_Hopefully that made sense_ 😂)

## So why should I use this

Working in Software; both professionally and independently, I just couldn't find a tool that automated the menial, and repetitive tasks I encountered every day, and was flexible in the way _I_ wanted.

So I built Mokha. Mokha works the way _YOU_ want it to. It's cross platform (well, it's as cross platform as the scripts you make it run.) and it's designed to be flexible about how you integrate it into your workflow.

I personally have it bound to a keyboard shortcut on my work MacBook and Windows PC and it works a treat. I expect that other people will use it in a variety of ways so I've left it standalone to allow for you to integrate it the way you want.

## Further integration with Mokha

So far, there's one small convenience I've added to Mokha that is completely optional for you to implement. If a script you want to run requires text from the clipboard, you can set a parameter to `clipboardContext` as follows:

```Python
def memeify(clipboardContext=None):
    string = clipboardContext if(clipboardContext != None) else pyperclip.paste()
    string2 = ""
    for c in string:
        string2 = string2 + c + " "
    pyperclip.copy(string2.strip())
```

and the configuration in JSON is as such:

```JSON
      {
        "title": "Memeify the clipboard text.",
        "methodID": "memeify-the-text",
        "arguments": {
          "clipboardContext": {}
        }
      }
```

```JSON
 {
    "--id": "memeify-the-text",
    "name": "memeify",
    "dependency": "memetext",
    "schema": {
      "numParams": 1,
      "parameterNames": ["clipboardContext"]
    }
  }
```

Mokha will then pass the value of the clipboard (via `pyperclip.paste()`) into the value of `clipboardContext` during Step 8 of the application's flow.

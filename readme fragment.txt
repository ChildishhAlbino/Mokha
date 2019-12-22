Mokha is completely configurable from JSON files. There are four main config files when using Mokha:

### Base Configuration:

- `config.json`: This is the first file loaded my Mokha on startup. The entire purpose of this file is configure the directories of the remaining three configuration files. The default location for all three files are the root directory of the application.

### User Configuration:

- `dependencies.json`: A JSON file that outlines of what files, folders, and python scripts your code requires.
- `profiles.json`: A JSON file that outlines high-level structures that outlines different groups of methods you might have, for example: I have three profiles for Home use, Independent work use, and for my main job.
- `methods.json`: JSON File that outlines the structure of all methods being run by Mokha.

## Detailed explanation of each configuration file:

### Configuration for my other configuration files, uh... why?

To keep it brief, I use Mokha on a d2d basis between my work Macbook and my home Windows PC. I wanted to have a shared experience between both platforms in terms of what methods I had availablem etc.

Because of this I wanted to be able to move my `User Configuration` files to dropbox. To do this, I had to create some fundamental configuration for the application that _cannot_ be moved. This is `Base Configuration` and it currently only acts as a pointer for where to find the `User Config` JSON files.

```
{
  "config-types": {
    "methods": "./methods.json",
    "dependencies": "./dependencies.json",
    "accounts": "./accounts.json"
  }
}
```

#### What are methods?
#### What are methods?

Methods are simply the outline of a method in a Python Module. Looks as follows.

For the following Python method:

```
def openURL(URL="https://www.google.com.au"):
    webbrowser.open(URL)
```

```
{
    "--id": "1",
    "name": "openURL",
    "dependency": "openURL",
    "schema": {
      "numParams": 1,
      "parameterNames": ["URL"]
    }
  },
```

Field descriptions:

- `--id`: Some unique ID for this specific method definition. Helps keep things modular.
- `name`: This the name of the method in Python you are defining in the Mokha configuration file. This IS case sensitive.
- `dependency`: This is the name of Python module you are importing to run this. You always need 1 dependency - this will be elaborated in a section below.
- `schema`: This is an object that verifies that a shortcut that calls this method is passing the correct arguments.
  - `numParams`: This outlines the number of parameters this method expects. This will be made optional in the future.
  - `parameterNames`: An array of string that outline the expected arguments.

Methods are the most atomic thing in Mokha and everything going forward will be building on them.

#### What are profiles:

Profiles are a way of separating instances of methods for different workflows.

Below is the configuration for a single profile.

```
{
    "--id": "1",
    "title": "Personal",
    "functions": [
      {
        "title": "Google Calendar",
        "methodID": "1",
        "arguments": {
          "URL": "https://calendar.google.com/calendar/b/0/r/month"
        }
      },
      {
        "title": "GitHub Profile",
        "methodID": "1",
        "arguments": {
          "URL": "https://github.com/ChildishhAlbino"
        }
      },
      {
        "title": "Personal Blog",
        "methodID": "1",
        "arguments": {
          "URL": "https://childishhalbino.github.io/"
        }
      }
    ]
  },
```

A profile has the following fields:

- `--id`: A unique identifier for this profile.
- `title`: A title for the profile. This gets printed to the console.
- `functions`: An array of function objects that detail the method being called and the arguments being passed for this option.
  - `function`: A function object looks like this:
  ```
  {
        "title": "Google Calendar",
        "methodID": "1",
        "arguments": {
          "URL": "https://calendar.google.com/calendar/b/0/r/month"
        }
      },
  ```
  A function object has the following fields:
  - `title`: This is the name of the function.
  - `methodID`: This is a reference to the ID of the method this function calls.
  - `arguments`: A JSON object that has keys that equal the parameters names outline in this method's configuration. The value of said key is the argument that will be passed to the method call.

## Setting up dependencies

### What are dependencies in Mokha?

In short, everything is a dependency. Mokha runs your scripts for you. You write a Python script that does what you want it to do, put it in the dependencies of Mokha, and configure it and you're done.

In more detail; Mokha has three types of dependencies:

- `Python`: These are Python modules you're configuring Mokha to run methods from.
- `Folders`: These are folders that need to exist inside the dependencies subdirectory. It's a good way to make sure external resources that your modules may rely on are also present.
- `Files`: The same principal as above but for files. _This is potentially being refactored into one dependency object_

### How does this look in JSON?

It's really easy to setup dependencies in Mokha with JSON. All dependencies of the same type are grouped into an array. Mokha automatically assumes dependencies are in the sub-directory so you need only store the relative path from there.

```
{
  "python": ["memetext", "encryptPasswords", "openURL"],
  "file-system": ["jasypt", "jasypt/bin", "jasypt/lib", "jasypt/bin/encrypt.sh"]
}
```
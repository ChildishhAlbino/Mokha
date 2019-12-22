# Mokha: Workflow Automator

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

1. Clone this repo and run Mokha.py. It will autogenerate the config.json file with the default values, however, it will not generate those files/folders for you.
2. Create `accounts.json`, `methods.json` and `dependecies.json` files and a `dependecies` folder wherever you want. If you deviate from the default values in `config.json` please update them there.
3. Add an account to the `accounts.json` file as follows:

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
  }
]
```

A profile has the following fields:

- `--id`: A unique identifier for this profile.
- `title`: A title for the profile. This gets printed to the console.
- `functions`: An array of function objects that detail the method being called and the arguments being passed for this option.

  - `function`: A function object looks like this:

    ```JSON
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

## So why should I use this

Working in Software; both professionally and independently, I just couldn't find a tool that automated the menial, and repetitive tasks I encountered every day, and was flexible in the way _I_ wanted.

So I built Mokha. Mokha works the way _YOU_ want it to. It's cross platform (well, it's as cross platform as the scripts you make it run.) and it's designed to be flexible about how you integrate it into your workflow.

I personally have it bound to a keyboard shortcut on my work Macbook and Windows PC and it works a treat. I expect that other people will use it in a variety of ways so I've left it standalone to allow for you to integrate it the way you want.

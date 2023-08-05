# DevConsole

DevConsole Is A Developer Console That Lets Your User Or The Developers To Have A Console Interface For Testing.
This becomes extreamly handy when you want to execute functions at certain times and don't want to setup a super complex system for testing.

There Will Be A "Command" Class Which Is A Class That Stores A Function/Method That Gets Called When The Command Is Executed And A 
Name Which Is The Name Thats Used To Call The Command In The Console (Note: The Commands Will Be Lowered So Even A Command Like
"eXiT" will be recognised as "exit").

Usage Examples (Python Code):

```Python
from DevConsole.Console import Console, Command

console = Console("Console title", "icon path", "background color code") # Create a new console.   all these parameters are optional

def function(): # The Function That Will Get Activated When A Command Is Executed
	print("A Command Has Been Executed Through DevConsole")
	console.Log("You Just Executed A Command") # Writing A Line To The Console

cmd = Command("name", function) # Created a Command Object Called cmd and giving it a name and a function/method to call

# The Name Of The Command Will Be the text used to call the command

console.RegisterCommand(cmd) # Register The Command That We Just Created, You Could Register As Many As You Want

console.mainloop() # Calls the tkinter.mainloop() function
```

# Update 0.2.2
1.
Changed command "WriteLine" to "Log"
Added the prefix and text colour options
Usage (Python):

```Python
console.Log("Main Text", "Prefix (Optional)", "color (Optional)")
```

The colours in the color parameter needs to be lower case, compatible with tkinter.

2.
Forgot to add self in the RaiseError function in the console class. Thats fixed and it will properly raise an error or skip

# Update 0.2.1

added support for adding a list of commands in one function
```Python
command_list = [command1, command2] # Making A List Of Commands

console.RegisterCommands(command_list) # RegisterCommands() function added to the Console Class
```

fixed errors:

changed the path checking on the icon so it will work now and you won't get an AttributeError When Trying to add a icon to the window


# Upcomming Features (Maybe...)
1. Custom Console Window

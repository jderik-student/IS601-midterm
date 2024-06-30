# IS601-Midterm
## Student: Joshua Derikito

## Project Install Instructions & Commands
### install & start
1. clone
2. pip install -r requirements.txt
3. python main.py
### testing
1. pytest
2. pytest --pylint
3. pytest --pylint --cov
4. pytest --num_records=100
### Available REPL Commands
1. add \<operand1> \<operand2>
2. clearHistory
3. deleteCalculation \<calculation#>
4. divide \<operand1> \<operand2>
5. exit
6. getCalculation \<calculation#>
7. loadHistory \<csvFile>
8. menu
9. multiply \<operand1> \<operand2>
10. printHistory
11. saveHistory \<csvFile>
12. sutract \<operand1> \<operand2>
### Program Description
This application is an interactive (REPL) calculator that keeps a history of its calculations. The calculator can perform four basic
operations: add, subtract, mutliply, and divide. The application keeps history in memory and in a csv file that it creates or defined by
its environment variables. On start up, the calculator populates its history with the calculations stored in the environment variable defined csv file.
The user can save and load calculations to/from another csv file, delete its local history as well as the history stored in the csv file defined by the environment variables. The user can also delete and get specific Calcaultions from memory. While sending commands through the REPL, the Calculator automatically saves the file to history, the dataframe, and the assocaited csv file.
## Video Link
https://youtu.be/cXk9zkoL0xU

## Analysis of Application Design

### Implemented Design Patterns
All definitions of the Design Patterns came from [RefactoringGuru](https://refactoring.guru/)

#### Facade Pattern
Relevant Files:
- [DataframeManipulator](/app/calculator/data_manipulator/dataframe_data_manipulator.py)
- [CalculatorHistory](/app/calculator/calculator_history.py)

The Facade design pattern allows one to create a simplified interface to abstract away business logic from complex library/framework.

In my project, I implemented the Facade design pattern to create an interface that abstracted away the business logic of Pandas data manipulations. I created the DataframeManipulator class to handle all the Pandas logic to manipulate a pandas dataframe and a csv file with pandas. As a result, the CalculatorHistory class did not have to be filled with pandas library related code in the append, delete_history, and delete_calculation_at_index methods. As a result, the CalculatorHistory class is much easier to follow and understand what its trying to do as it is not filled with pandas data-related business logic. Also, if other aspects of the code needed to manipulate pandas dataframes or csv in the future, it can reference the DataframeManipulator and add methods to it, to handle the pandas data manipulations, and abstract away the business logic to make the code more readable. 

![screenshot of code snippet in dataframe_data_manipulator.py](/screenshots/dataframe_manipulator.png)

#### Command Pattern
Relevant Files:
- [Command Abstract Class & CommandHandler](/app/commands/__init__.py)
- [Plugin Directory](/app/plugins/)

The Command design pattern turns requests into stand-alone objects that contain all information about the request which allows for the requst to be passed as a method argument.

I implemented the Command design pattern for all of the commands that the user can use in the REPL interface. In the screenshot below, I created an abstract Command class that had an execute method, to be extended by each specific command to define logic to complete a certain task, and a string representation for logging and printing purposes. The Plugin Directory (seen in the second screenshot below) contains different Concrete implementations of the execute method to interact with the Calculator and its history. Due to the Command design pattern, in the CommandHandler's execute_command() method, the single execute() method called in line 91 would apply to all of the commands in the Plugins directory because each plugin is extended from the Command class and therefore can be interchangeable. Furthermore in app/__init.py, I implemented the load_plugins() method which allows for the dynamic loading and registering of commands into the CommandHandler. This along with the Command Design pattern, helps to uphold the Open/Close Principle as if I were to add a new command in the future, all I would need to do is create a new Concrete Command in the plugins directory and it will be able to be used in the REPL without touching exisitng code. The Command Design pattern also helps with the structure of the project as it enforces separations of concerns as each plugin Command does something different from each other. 

![screenshot of code snippet in command/__init__.py](/screenshots/command.png)
![screenshot of the Plugins Directory](/screenshots/plugins.png)

#### Factory Method Pattern
Relevant Files:
- [Calculation](/app/calculator/calculation.py)

The Factory Method design pattern provides an interface for creating objects in a superclass.

I implemented the FactoryMethod design pattern in the Calculation class by creating a staticmethod to create a new instance of the Calculation object with different operands and Operation. This allowed for increased flexibility and structure in the project by allowing for a specific interface to create Calculations with different operations.

![screenshot of code snippet in calculation.py](/screenshots/factory_method.png)

#### Singleton Pattern
Relevant Files:
- [singleton.py](/singleton.py)
- [CommandHandler](/app/commands/__init__.py)
- [CalculatorHistory](/app/calculator/calculator_history.py)

The Singleton design pattern allows for a class to have a single instance throughout a project and it provides a global access point to that instance.

To a lesser extent, I first implemented this design pattern in singleton.py as seen in the screenshot below. The file contains two variables, one storing the location of the csv file that the calculator will autoload and autosave to/from and a dictionary mapping to easily get the mathematical operation function from its string name. The singleton design pattern allowed me to not have to redefine these two frequently used variables throughout the code which reduced redundancy throughout my project. Furthermore, because these variables have a global scope, it allowed me to redefine the csv file history path once and I could see that change everywhere throughout the code. This made testing with mock files much easier.  

![screenshot of code snippet in singleton.py](/screenshots/singleton_py.png)

To incorporate the Singleton design pattern, I decided to make the CommandHandler a singleton. The screenshot below shows how I defined the CommandHandler to be a singleton and to have only one instance of the class. The CommandHandler registers and executes the available Commands from the plugin directory that can be used by the user in the REPL interface. Because of this, there exists only one CommandHandler as a result I thought it would benefit from becoming a singleton. As a result, commands would only need to be registered once and then they could be accessed anywhere in the program. Furthemore, because there is only one CommandHandler in the application, the singleton design pattern ensures that throughout the project, there is only one global CommandHandler being referenced. Lastly, the CommandHandler being a singleton aids in the scalability of this project, as if I were to add more capabilities, for example maybe a Graphical User Interface, the REPL and the GUI would use the same CommandHandler and I wouldn't have to worry about registering commands more than once and the registering of commands can be limited to one spot in the code. 

![screenshot of code snippet in commands/__init__.py](/screenshots/command_handler_singleton.png)

Lastly, the CalculatorHistory only has class methods that manipulate its class variables. As a result, the CalculatorHistory class can be thought as a singleton (although not a traditional singleton) as well as the methods are not working on a specific instance of the CalculatorHistory, rather on the class itself, therefore its class variables and class method calls to manipulate them can be seen globally throughout the project. This allowed for all the files and classes in the project to manipulate the same global class variables of the stored 'history' list and 'dataframe' pandas dataframe without having to initialize/redefine the CalculatorHistory class in each file and point to the same instance (if I were not using class methods and variables). This was important as there should be only one CalculatorHistory instance that needed to be referenced throughout the project. Lastly, the CalculatorHistory being defined in this way also helps to improve the scalability of this project because it ensures that any new features and commands that I may want to add would reference the same CalculatorHistory as the rest of the project.

#### Strategy Pattern
Relevant Files:
- [DataManipulationStrategy](/app/calculator/data_manipulator/__init__.py)
- [DataframeManipulator](/app/calculator/data_manipulator/dataframe_data_manipulator.py)
- [MemoryDataManipulator](/app/calculator/data_manipulator/memory_data_manipulator.py)
- [CalculatorHistory](/app/calculator/calculator_history.py)

The Strategy design patterns lets you define a family of algorithms that accomplish the same goal, but differ in implementation/execution, and allow for these algorithms to be used interchangeably.

I implemented the Strategy design pattern by creating different strategies for data manipulation depending where the data was stored. The DataManipulationStrategy class is the abstract class (the Context in this design pattern) that was extended by each Strategy (the DataframeManipulator strategy and the MemoryDataManipulator strategy). The methods of the DataManipulationStrategy defined three methods: append, clear_database, and delete_entry_at_index. These methods were then extended in each individual Strategy to preform these functions for the data location specific to the Strategy. The DataframeManipulator defined these methods to manipulate the data stored in the pandas dataframe and csv file whereas the MemoryDataManipulator defined these methods to manipulate data stored in CalculatorHistory's 'history' list. 

![screenshot of code snippet in data_manipulator/__init__.py](/screenshots/data_manipulation_strategy.png)

By implementing a Strategy design pattern for data manipulation, this allowed for a lot of flexability in the CalculatorHistory. For example, as seen in the screenshot below, there only needed to be one CalculatorHistory append method, and not one per database location or one giant append method to handle all locations, as this method calls the Context's append method and the Strategy chosen will handle the logic to execute the manipulation. This behavior is also seen in CalculatorHistory's  delete_history and delete_calculation_at_index methods. These Strategies for data manipulation also abstracted away the datalocation specific logic from these methods and made these methods easier to read and follow without needing to worry about the specific details needed to manipulate the data. Lastly, by implementing the Strategy design pattern, this greatly helps in the scalability of adding more database storage locations (an excel file for example), as there would be no need to edit the CalculatorHistory class when adding a new database location. Instead, one would just need to define a new Strategy and then the CalculatorHistory will be able to manipulate data at the new location without changing its methods (and without potentially breaking existing code), just by choosing the new strategy. Adding new Strategies helps to uphold the Open/Closed Principle which boosts the projects flexibility and scalibility.

![screenshot of code snippet in calculator_history.py](/screenshots/calculator_history_append.png)

### Environment Variable Usage
Relevant Files:
- [App](/app/__init__.py)

I used Environment Variables to dictate the logging level to use based on the environment/branch that was running the app and to determine which CSV file to autoload from and autosave Calculations to/from. In my env file and in GitHubActions Environment Variables I defined ENVIRONMENT and CSVFILENAME. In GitHubActions I had two environments, PROD and DEV, in which I used PROD to test master and DEV to test develop. In GitHubActions I specified a location/file path to be used for deployment defined in CSVFILENAME. Using these environment variables, I logged only up to INFO level logging for PROD but for DEV I allowed for all levels of logging, including DEBUG. This is because in the DEV enviornment, this is where I would be having my final testing/ deployment to ensure all the code is working before pushing to production. For production code, since in the real world, it would be used by actual customers, I wouldn't want the robustness of DEBUG messages as that would be too many log messages to keep track of and wouldn't be necessary if everything is working. I implemented the CSVFILENAME environment variable so that there could be on spot where I could change the associated csv file without touching the code.

![screenshot of code snippet in /app/__init__.py](/screenshots/calculator_history_append.png)

### Logging Strategy
Relevant Files:
- [App](/app/__init__.py)
- [CommandHandler](/app/commands/__init__.py)
- [PluginsDirectory](/app/plugins/)
- [CalculatorHistory](/app//calculator/calculator_history.py)

Generally, throughout my code I tried to limit logging to the App, the CommandHandler, and the Command themselves as these are what the user interact with directly. By doing this, it also helped reduced the redundancy of these logs as it limited the messages to be in specific areas that cover large areas of the code and will catch the behavior of the code and the user's workflow. I implemented ERROR log messages for when the user or app enters a case that would have caused the Command or App to fail, for example an Index error or putting a string instead of a number for the add command. I implemnted WARNING log messages, when the user or app does something that was not intended but doesn't stop the App from running, this could be that the user tried to divide by zero, it didn't compute, but was still added to the history. I also implemented WARNING log messages for when the program creates a file or directory as these files are expected to exist prior to runtime. I implemented INFO log messages in the CommandHandler to keep track of the commands that the user calls through the REPL so it can be traced later if an issue arises. And I implemented DEBUG log messages inside each command to print out the result of the command to be used if a bug appears for the user. Below I will provide screenshost and descriptions for each of the log message types I used.

#### ERROR & WARNING

![screenshot of an error and warning log message in /app/__init__.py](/screenshots/error_warning_log.png)

The above code snippet is inside the \__init__ method of app where it is checking if there exists the directory with the specified name. The warning message is being used since the app could not find the required directory at runtime, so it created one for the user, which I decided to be a warning since this behavior is not explicitly expected by the user and to highlight the directory was created by the app, not the user. The error message is to tell the user that the directory was found, but the app does not have the proper permissions to access it. As a result, the app exists as it cannot manage the Calaculator History and logs out that an error occured that stopped the app from working. 

### INFO

![screenshot of an info log message in /app/commands/__init__.py](/screenshots/info_log.png)

The above code snippet is inside the CommandHandler's execute_command method which logs out the command the user called with the arguments they called it with. I wanted to log out this information as it is the best way to trace the steps that the user did if they encountered a bug. I felt this was the most descriptive information to log out that would allow me to indentify where a problem occured in production. I didn't want to log out the result of the command in INFO as it would clutter the log file and I could just retrace the commands to see the results.

#### DEBUG

![screenshot of a debug log message in /app/plugins/add/__init__.py](/screenshots/debug_log.png)

The above code snipper is inside the add command's execute method which logs out what was stored in the history and the result of the addition. I replicated this for all the commands and logged out all of the results the user would see in debug. I felt the actual command return result would best be stored in debug as I would only be concerned with the results of the command if I was trying to either test a new feature or identify a bug which I would do in develop or do it locally, which would have a DEBUG level logger. As a result I wanted the most detail in DEBUG without cluttering the logs, so I thought logging out the command results was the best option.


### Look Before You Leap (LBYL) vs Easier to Ask For Forgiveness then Permission (EAFP)
Relevant Files:
- [App](/app/__init__.py)
- [CommandHandler](/app/commands/__init__.py)
- [PluginsDirectory](/app/plugins/)
- [CalculatorHistory](/app//calculator/calculator_history.py)

In general, I tried to limit the if statements (LBYL) I used and tried to used as many try/exceptions statements (EAFP) as possible in order to improve the performance of the code and because Python favors EAFP. I limited most of the if statments to the /__init__ method of the app as ensuring that the app and the environment are setup correctly is important for the app to run and because this initiazliation would only be ran once per application startup. As a result, these if statements would only be ran once and by using LBYL, it would ensure that the app was initalized correctly without running into any exceptions that may cause the code to fail or for the app to not be initialized correctly. For the remainder of the code, especially in the REPL and Command Handler, I used try/except statements and EAFP. Because the REPL prints the commands and I have written out this README, along with the application being relatively simple to use, it is more likely that the user would enter correct, working commands, rather than incorrect commands or arguments. As a result, I would try executing the user inputted commands through the CommandHandler rather than checking for proper command structure as it is more likely the user would enter a valid command than not. 

For example, the screenshot below (found in the /__init__ method of App) shows an if-elif statement that checks if the data directory exists and if it is set with the right permissions. I decided to incoporate LBYL here as this if-elif statement would only be ran once, during App initialization, and because I wanted to ensure that the data directory was properly created/ set up before attempting to use it as this directory is prerequisite for the App to run correctly.

![screenshot of an if elif statement in /app/__init__.py](/screenshots/error_warning_log.png)

The screenshot below (the execute_command method of the CommandHandler) shows an try-except statement for executing user provided commands from the REPL. Because the commands and their usage is printed on App start up and because the README is available, it is safe to assume that the user will input valid commands and parameters. As a result, it would be much faster to try executing the command and if an error was encountered to handle it after trying. Because most of the commands should be valid and should execute cleanly, it is expected that the try statement would rarely run into exceptions and therefore would preform much faster than checking for every possible exception before trying to run the command.

![screenshot of try except statement in /app/commands/__init__.py](/screenshots/try_statement.png)
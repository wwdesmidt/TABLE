---
# TABLE

Possible names:
- Tech/Analog Battle Layout Exhibitor
- Tabletop Advanced Battle Layour Environment
- Tabletop Alternative Battle Layour Environment
- ???

Write a cool summary here!

Some points about the project:
- It will be simple
- It is meant to run on a table with a screen in it
- It embraces the fact that a lot of gaming is done on the fly. You don't need to have all your maps pre-made digitaly before you can play to use this. it will have some basic drawing functions
- It is meant to supplement your current style, not replace it. Like using paper? Put a peice of paper on top of it. Maybe you can make the screen a solid color (blue for the ocean?) and add some background noise sound effects to deepen your experience. 
- What else?

---

## Testing instructions

 Since its main purpose is to be set up on a dedicated machine embedded in a table, and not for people to be able to easily download and run on their every day computers, there are a few hoops to jump through to test it (it's really not bad though). I don't plan on distributing an executable file for this, but I will include a .bat file to launch it in Windows (TODO: create a shell script for Linux and Mac).

**1. Install python**  
You can get it here: https://www.python.org/downloads/  
Make sure that you check the "Add Python X.X to PATH" option  
After it is installed, you can verify that it is installed correctly by opening a command prompt and running the following command:  
`python --version`  
If it says something like "Python 3.8.1", you have installed Python correctly.   

**2. Install Git**  
You can get it here: https://git-scm.com/downloads  
It will ask you a lot of questions, but you can just keep the default options for everything.  
After it is installed, you can verify that it is installed correctly by opening a command prompt and running the following command:  
`git --version`  
If it says something like "git version 2.25.0.windows.1", you have installed Python correctly.   

**3. Clone the git repository**  
This will download the source code for you to run. You can also just download it from this page, but if you do it this way, you will be able to automatically get updates in the future.
  1. Go to the directory where you want to create the TABLE folder on your computer
  2. Open a command prompt in that folder  
  (the easiest way to do that is to type "cmd" in the address bar and hit enter)
  3. Run the following command:  
  `git clone https://github.com/wwdesmidt/TABLE`
  
And that's it, you are done.

Now you can just go into the TABLE directory, and run table.bat to launch the program, or run get_latest_version.bat to get the latest version. 

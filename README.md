## 2/10/2020 - Lots of token changes

- You can now add tokens via an image file from the right click menu just like maps
- Token size and outline color are stored in a json file, like map size is, so it carries between sessions. This also means that a dm can load up all their tokens once each and set them up and not have to worry about them anymore
- Added a second right click menu for when you right click on a token. This allows you to:
    - Change a tokens color. I added ROYGBIV plus white black and grey
    - Change a tokens size. I added all the official DnD sizes plus one... extra... size. I also made small 4 ft instead of 5ft, almost entirely so halflings will look smaller on the screen :)
    - Delete a token
- Did some other small things
    - Made a minimum token size... I don't know if its the best minimum token size, but its a minimum token size. It makes it so the app doesnt crash when you put a 5 ft. token on a 900 mile map, and the token ends up being 0 pixels on the screen
    - Made it delete all the tokens when you change maps.
    - There is now a dedicated variable for whatever the last token you right clicked was. This lets you cleanly color, size, and delete a single token. I want to do this for left clicking on tokens too, which will help with, but not solve, the issues I mentioned last time.
    
Issues:
I need to make it so you can't load a token on a map with no size set.. like... really badly. Either that or make the default map size something decent like 100 feet or something. That's probably a good idea. Right now if you load a map, dont set the size, and the load a token, the token will be HUGE and fill the whole screen, and you'll have to crtl-alt-del or something?

Some UI design philosophy stuff:
So... for the colors and the sizes, I spent time making a seperate menu item for each one. This makes it easy to use everything with just a mouse, but it limits your options. You couldnt make a token thats exactly 42 feet, or have 9 rats that are all a slightly different shade of grey. I guess one solution could be to have popup windows with forms that you fill out (still using only a mouse but they could have more complex input options). What do you think, person who has no way to respond to this?

## 2/6/2020 - The beginnings of tokens

Started writing update summaries... apparently?

Merged the "token prep" branch back into master, which includes:
- The ability to do basic token stuff: put tokens on the table, move them around. This is pretty sweet because it makes the app really close to being awkwardly usable. All thats needed now is a ton of quality of life features.
- Created a token class with the basics
    - x and y position
    - radius (single value vs width and height, tokens are round for now)
    - image
    - draw, undraw, move methods
    - generate a unique object instance if on create, and use it as the images tag, so that it can be found and deleted when it moves
    - in object detection based on a set of x,y coordinates ("contains" method)
    - all values passed in through constructor, in the future will just take image file name and get values from external file
- Created a list to store tokens so there can be more than one on the table at a time.
- Added new table mode "token_moving"
- Added mouse event code to traverse list of tokens and do the stuff
- At first tokens were only solid colors, now they are only images. I need to decide if it should support both, or if, for simplicity, a solid color token should just be a token with an image of a solid color. 
- Added a fancy alpha mask to make the actual images on the tokens look like circles. I didn't actually expect to have that working at this point. This obviously only works with files that support alpha (png). It would look so ugly without it that maybe I should just force all tokens to only support png? (other formats that have an alpha channel?)
- Finally, set the app up to load a sample dungeon map and a few tokens so people can test it and see how it looks and feels.

Some issues I know about:
- When you move a token, it "snaps" to the mouse position. This is more apparent on larger tokens.
- When you have two tokens overlapping and you move one of them via the overlapping area, they snap together due to the previous note. If they are the exact same size, you can never recover from this; the one on the bottom is forever hidden under the one on top.

Solutions?

I see two possible solutions to the issues above. 
1. Make it so you can only move one token at a time. This might be a good idea regardless, unless at some point I make some better way of selecting multiple tokens (which would be nice at some point). This way if there were two on top of eachother, you could just move the top one off. This might get into weird issues with the order of the token list. When the code decides if you are clicking on a token, it looks at the position of the mouse and the position of the token and decides if the mouse is "inside" the token. It does this for each token in the list one at a time. It would be pretty weird if a token you can see on the screen is further down the list than a token that is hidden under it. I guess maybe an easy fix would be to move a token to the beginning of the list if its clicked.
2. Make it so tokens move relative to the mouse instead of snapping to it. This would allow you to move a token from its side, or move two tokens at the same time without them snapping on top of eachother. This would also be nice ot have either way. I should probably just do both.

Up next:
- A menu option and popup dialog box to load tokens. This is going to be pretty complicated because all the metadata for tokens will have to be loaded at this time, and there wont really be a good way to change it other than deleting the json file. Maybe eventually you should be able to right click on individual tokens and get a special token menu for editing them.
- Create and manage json files to accompany the tokens (like how the maps work). This can store the tokens size, what color its border should be, etc.
- A form of tokens that are just semi transparent colored shapes to represent area effects.
- How in the world am I gonna figure out where to put each token when it is created?
- Need to rework the whole system that shows you how far you are moving things. Maybe a dotted red line thats thicker than the 1px black line. I'm also thinking about putting the move distance somewhere specific on the screen, instead of next to the thing you are moving. There were alway issued with it going off the top and right of the screen, but now that there are tokens its also covered by the tokens. 
- Maybe some kind of token numbering scheme to help the dm keep track of tokens with the same image?

Random thoughts

Some way of selecting multiples...

I wonder if there can be a seperate type of token called a "vehicle" or something. When you move a vehicle, any token that is touching a "vehicle" would move when you move with it. The more I think about it the more complicated it is getting... something to come back to.

---

# TABLE
(summary is wip)
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

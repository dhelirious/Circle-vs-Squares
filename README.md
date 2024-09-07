Circle vs Squares: The Showdown.

How To Play:
- Download main.py which is the game
- Open console in the folder of the game directory and write "python3 main.py" or simple right click on main.py and use python to open it.

Controllers:
- W,A,S,D for movement
- J rotate left, K rotate right
- SPACEBAR to shoot

Perception: This is a quick experiment to see the capabilities of LLMs to make a python game with no corrections, one shot programming with precise indications on how to implement it's mechanics, the LLM was abble to get every detail mentioned as asked flawlessly. The only improvements of gameplay mechanics that are lacking, are just because I didn't realize them while asking for them in the prompt, such as:
- a marker to show where the player rotation is.

To See the power of fixes, I'll build another branch with a newer and improved version, I'll try to avoid correcting the LLM by hand, I'll just use prompts to iterate over the existing code and adjust it's current mechanics.


Circle vs Squares: The Showdown is a little TOPDOWN Arcade Python game programmed in python in "One Single Prompt", no corrections made, no iterations.

PROMPT USED:
"I'd like a to make a python game, I've created a file named main.py for the algorythm and I'd like you to share me it in a good way manner.
The game needs to be rendered in a window using pygame and it should use basic shapes made with the engine:
circle for the player
square for the enemies

the game is topdown 2D viewed and the player can be controlled using W,A,S,D to move in every direction. 
Using J the player can turn left the circle rotating it by itself and pressing K it can rotate to the right in the same manner.

The main objective of the game is to kill incoming squares before they touch the player so colliders with the same size of the shape on enemy and player (square and circle) should be considered for collisions and counting lose or kills.
Pressing the bar, the player can shoot little circles to the direction he's facing, so the player should have a point where it spawns little circular bullet that are 1/3 the size of the player. 
If those bullets collide with an enemy the enemy is killed and a counter above the screen starts to count one by one. If an enemy touches the player, the player dies and shows a message in the middle of the screen saying "You Lost" and shows the current score when the player lost, if player presses the "space bar" which is the same to shoot, the game restarts and the counter goes to 0.

The game is infinite mode, so it would start spawning enemies that will be walking towards the character in a slow manner, in a constant speed, so the player can avoid them. As the time passes, the enemies will start to appear faster and faster. The spawn rate time would be 1 enemy every 3 seconds at first, and as passes 2 minutes, the rate should be 1 enemy per 0.1 seconds.
The player should have a cooldown rate for shooting, so player can't spawn bullets as hell, the cooldown of shooting should be 1 second between each shot, but it should have a counter so every 3 kills that the player kill squares, it gives the shooting cooldown of the player a discount in cooldown time, lets say for example,  the player has 1 second cooldown, then the player kills 3 enemies, so the cooldown gets reduced 0.05 seconds, and so on as the player kills 3 enemies, so the count should say every time "killcount % 3 = 0" the player gets the shooting cooldown reduced by 0.05 seconds."

Libraries used:
pip install pygame

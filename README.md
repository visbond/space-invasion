# Space Invasion
Space Invaders tribute in Python. 

Built while slowly following Eric Matthes' excellent Python book. 

To run this, you would need the pygame package (www.pygame.org). Instructions differ for different platforms, so please refer to the site rather than just relying on ```pip install pygame```.

Make sure all the .py files are present and the directory structure is the same (mainly that the sprite images are in the /images folder, sounds in /sounds. Else modify the code files to reflect your path). 

Then just run 
```
python space_invasion.py
```
Press P to play.

Space bar to shoot, cursor keys (left and right) to move (only horizontal movement yet). 

After all the alien ships are shot down, the next wave will come. Each successive wave would be faster.

Press Q or Esc to quit.

The project is highly modular. Every element is in its own class in a separate py file. Various settings can be modified by editing the respective file. The names are self-explanatory. For example ship speed can be modified by editing ship.py, bullet width and speed in bullet.py etc. 

This is a basic version. Much more can be done, especially enhancing the visual elements (animated sprites, animated backgrounds). Background music. A project for a rainy day...




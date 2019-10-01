# mini-keyboard
keyboard simulator

The code proposed here is a keyboard simulator different from regular keyboards. Each pyramid is a small joystick. This enables the user to perform not only pressing, but also applying various efforts, while seeing on the screen a reflection of their actions. While the action is taking place, the input character should appear in a temporary pop-up window. In this case, the action can be canceled or switched to another mode. The final solution is to lift your finger, which corresponds to releasing the button or “1” in the keyboard code. The initial reset is respectively "0". However, the format here is more extended. The signal is transmitted not by one, but by two values. That is, the starting zero is "0 0", and the end of the event is "1 1". These two values are transmitted in one step and interconnected so that there can be many intermediate states. That is, the relationship between pressing and releasing goes through superposition.
The operation of the device itself is a combination of capacitive and piezoresistive sensitivity. When you touch the tip of the pyramid, a capacitance is triggered. Data from capacitive sensors can indicate only the pyramid number, but not the direction of inclination. Then the spring rod is bent under the action of force in one of the parties, which causes a change in resistance at the sensors. The sensors are located crosswise and oriented on four sides of the PCB. Each side is connected to a separate ADC. On the ADC, you can get the direction of the effort, but not a specific address. 

The code reflects this as follows.

0 1 - upward relative to the PCB.
0 -1  down
-1 0  left side
1 0  right
Since the event is completed when the finger comes off the pyramid (and the capacitance is reset), then + - 1 here indicates the very last moment of contact. Intermediate states here should be outside 0  t o 1. It also allows you to get rid of floating point values, and use the ADC data directly. For 12 bit ADC, this is 4096. That is, the picture may be something like the following.
Relative sampling rate of 10 hertz.
For upward force.
0 0 start
0 500
0 1000
……….
0 3500
0 4000
0 1  separation
1 1  stop
Of course, this is data from one ADC. If we take the difference, then at a reference voltage of 3 volts, the voltage difference can be obtained in the region of 30 millivolts. That is, all values must be divided by 100.
0 35
0 40 
I will add that it is obviously immediately impossible to determine the value of the difference in resistances. This is due to both physics and the possibility of a circuit. However, if the address is already determined by capacitive sensitivity, the initial stream can be used to transmit the address of the element. Suppose that the sensitivity threshold is 1505. Then the very beginning of the touch will be like this:
The letter A is located on the sixth pyramid. I decided to put this value in the front row. The second row is a general increase in effort to the threshold of sensitivity.

0 0 start 
6 500
6 1000
6 1500
then the threshold is overcome, and we get the direction of the tilt force, for A this is the tilt to the left.
- 20 0
- 25 0
……….
- 35 0
-40 0
- 1 0  separation
OR
here each pair of values shows in the time window the letter A, the size of which is proportional to the magnitude of the force. This gives the user the opportunity to observe the process and actively interact. Separation means the end of input, after which the letter A is placed in the text. But if the user changes his mind and returns everything back, the input is canceled.

No separation
-40 0
-35 0
……….
-25 0
- 20 0
sensitivity threshold
6 1500
... ..
6 500
0 0  input canceled
1 1  stop 
However, the user can also continue to act to the opposite position. Suppose he intended to enter "S" which is on the opposite side from "A".
Non stop 
0 0
6 500
.......
6 1500
the threshold is overcome, but now the sign is positive
20 0
25 0
... ..
30 0
1 0  separation
1 1 stop 
now the letter “S” is loaded into the text

In addition, there is another possibility to change the input. This hold the finger in some position. For example, with a delay of one and a half efforts, the system will produce both “A” and “S” values with a time interval. Separation during the period of one or another means a choice.

…….
20 0
-20 0
... ...
20 0
-20 0
- 1 0  separation  "A" is selected.
1 1 
The last example implements the behavior of a "stubborn" user pushing  his own view. 

One-touch text entry is also possible. This is possible when a significant part of the word is already typed and the whole word is easy to guess from the dictionary. This is all the more accurate since touching reduces the choice of 4 letters.
This should be reminiscent of colloquial speech with alternating stressed and reduced letters and syllables. Some parts of the word are clearer if emphasis is put on them, others are guessed.
Here is the touch of the sixth pyramid.
A sample with a conditional frequency of 20 hertz will look something like this.

6 250
6 500
……..
6 1500
6 1250
……..
6 1000
6 750 
……..
On the faces of the sixth pyramid “AS” horizontally and “6$” vertically. 
In the simulator, the text is entered in the prb_miss.py file on lines 35 - 37
The output stream is converted into a list of two levels and stored in the port_sens.json file as a list.





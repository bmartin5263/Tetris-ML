# Tetris ML

**Primary Goal:** Train an AI Agent to play Tetris effectively

**The Spicy Bit:** The game will be running on separate hardware (an Arduino) than the Agent (Raspberry PI).
The Agent will have to *visually* read the state of the board (represented by a 16x32 LED matrix) and send its move over Serial communication (UART)

## Roadmap

- [ ] Develop Python version of Tetris with the same behavior as the Arduino one (which is in C++)
- [ ] Train Agent to Play the Game Locally
- [ ] Test Training on Actual Arduino Version, using Serial communication
- [ ] Adjust Behavior - if necessary
- [ ] Build harness for Raspberry PI camera
- [ ] Add Computer Vision component to Agent as a means of reading the board state

## UART Communication
The communication between the Arduino and Raspberry PI will initially be 100% Serial, starting with UART
If a bare-metal UART connection is used, the TX/RX pins will be connected on both devices and they must be grounded and use a level shifter for the 5V/3.3V difference
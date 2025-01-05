# Rock-Paper-Scissors-Spock-Lizard

## Description
"Rock-Paper-Scissors-Spock-Lizard" is an extended and interactive version of the classic Rock-Paper-Scissors game, using real-time hand gesture recognition. With a webcam and the MediaPipe library, the player's gestures are detected and compared to the randomly generated choices of the computer.

## Game Rules
The game follows the classic "Rock-Paper-Scissors" rules with the addition of two extra gestures: "Spock" and "Lizard." Each gesture beats two other gestures and is beaten by two different gestures:

- **Rock**:
  - Beats: Scissors, Lizard
  - Loses to: Paper, Spock
- **Paper**:
  - Beats: Rock, Spock
  - Loses to: Scissors, Lizard
- **Scissors**:
  - Beats: Paper, Lizard
  - Loses to: Rock, Spock
- **Spock**:
  - Beats: Rock, Scissors
  - Loses to: Paper, Lizard
- **Lizard**:
  - Beats: Paper, Spock
  - Loses to: Rock, Scissors

## Recognizable Gestures
Here’s how the gestures are interpreted by the system:
- **Rock**: All fingers are folded.
- **Paper**: All fingers are extended.
- **Scissors**: Only the index and middle fingers are extended.
- **Spock**: The index and middle fingers are extended, and the middle and ring fingers are spread apart.
- **Lizard**: All fingers except the pinky are folded, with the thumb close to the pinky.

## How to Play
1. Ensure that your webcam is connected and working properly.
2. Run the Python program.
3. Position your hand in front of the camera and perform a recognizable gesture.
4. The computer will randomly choose a gesture.
5. The system will compare the gestures and display:
   - The player's gesture
   - The computer's gesture
   - The winner of the round
   - The cumulative scores
6. Continue playing as many rounds as you like!

## Controls
- **`q`**: Quit the game.

## Technical Requirements
- Python 3.x
- Required Python libraries:
  - OpenCV
  - MediaPipe
  - Random
  - Math
- A working webcam

Enjoy the game! 🎮

import cv2
import mediapipe as mp
import random
import time
import threading
import math

# Initialisation de MediaPipe Hand
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

def calculate_distance(p1, p2):
    """Calcule la distance entre deux points."""
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

# Fonction pour reconnaître le geste (Pierre-Feuille-Ciseaux-Spock-Lezard)
def recognize_rps_gesture(hand_landmarks):
    """Reconnaît les gestes Pierre-Feuille-Ciseaux-Spock-Lezard."""
    finger_tips = [8, 12, 16, 20]
    finger_bases = [6, 10, 14, 18]

    # Déterminer si les doigts sont levés
    fingers_up = [hand_landmarks.landmark[tip].y < hand_landmarks.landmark[base].y for tip, base in zip(finger_tips, finger_bases)]

    # Vérifier si c'est Pierre
    if not any(fingers_up):
        return "Pierre"

    # Vérifier si c'est Feuille, Spock ou Lezard
    elif all(fingers_up):
        # Récupérer les landmarks des pointes des doigts et du pouce
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]

        # Calcul des distances entre le pouce et les autres doigts
        distance_thumb_index = calculate_distance(thumb_tip, index_tip)
        distance_thumb_middle = calculate_distance(thumb_tip, middle_tip)
        distance_thumb_ring = calculate_distance(thumb_tip, ring_tip)
        distance_thumb_pinky = calculate_distance(thumb_tip, pinky_tip)

        # Imprimer les distances
        #print(f"Distance Pouce-Index : {distance_thumb_index:.4f}")
        #print(f"Distance Pouce-Majeur : {distance_thumb_middle:.4f}")
        #print(f"Distance Pouce-Annulaire : {distance_thumb_ring:.4f}")
        #print(f"Distance Pouce-Auriculaire : {distance_thumb_pinky:.4f}")

        # Vérifier les conditions pour Lezard
        if distance_thumb_pinky <= 0.14:
            return "Lezard"

        # Vérifier les conditions pour Spock
        distance_index_middle = calculate_distance(index_tip, middle_tip)
        distance_middle_ring = calculate_distance(middle_tip, ring_tip)
        distance_ring_pinky = calculate_distance(ring_tip, pinky_tip)

        if distance_index_middle <= 0.07 and \
           distance_ring_pinky <= 0.08 and \
           distance_middle_ring >= 0.03:
            return "Spock"

        return "Feuille"

    # Vérifier si c'est Ciseaux
    elif fingers_up[0] and fingers_up[1] and not fingers_up[2] and not fingers_up[3]:
        return "Ciseaux"

    # Si aucun geste reconnu
    return "Inconnu"

# Fonction pour déterminer le gagnant
def determine_winner(player_gesture, computer_gesture):
    """Détermine le gagnant du jeu."""
    if player_gesture == computer_gesture:
        return "Egalite"
    elif (player_gesture == "Pierre" and computer_gesture in ["Ciseaux", "Lezard"]) or \
         (player_gesture == "Ciseaux" and computer_gesture in ["Feuille", "Lezard"]) or \
         (player_gesture == "Feuille" and computer_gesture in ["Pierre", "Spock"]) or \
         (player_gesture == "Spock" and computer_gesture in ["Pierre", "Ciseaux"]) or \
         (player_gesture == "Lezard" and computer_gesture in ["Feuille", "Spock"]):
        return "Vous gagnez !"
    else:
        return "L'ordinateur gagne !"

# Initialisation des scores
player_score = 0
computer_score = 0

# Gestes possibles pour l'ordinateur
rps_choices = ["Pierre", "Feuille", "Ciseaux", "Spock", "Lezard"]

# Chargement des icônes
icons = {
    "Pierre": cv2.imread("rock.png"),
    "Feuille": cv2.imread("paper.png"),
    "Ciseaux": cv2.imread("scissors.png"),
    "Spock": cv2.imread("spock.png"),
    "Lezard": cv2.imread("lizard.png")
}

# Initialisation de la webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

# Variables pour le délai entre manches
round_delay = 2
last_round_time = time.time()

# Variables globales pour la capture vidéo
frame = None
ret = False

# Thread pour la capture vidéo
def capture_video():
    global frame, ret
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

video_thread = threading.Thread(target=capture_video)
video_thread.start()

# Boucle principale
player_gesture = "Inconnu"
computer_gesture = random.choice(rps_choices)
winner = ""

while cap.isOpened():
    current_time = time.time()
    if frame is not None and ret:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if current_time - last_round_time > round_delay:
            last_round_time = current_time
            computer_gesture = random.choice(rps_choices)
            player_gesture = "Inconnu"
            winner = ""

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    player_gesture = recognize_rps_gesture(hand_landmarks)
                    winner = determine_winner(player_gesture, computer_gesture)

                    if winner == "Vous gagnez !":
                        player_score += 1
                    elif winner == "L'ordinateur gagne !":
                        computer_score += 1

        h, w, _ = frame.shape
        cv2.putText(frame, f"Votre choix: {player_gesture}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Choix ordi: {computer_gesture}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, f"Resultat: {winner}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"Score Joueur: {player_score} | Ordinateur: {computer_score}", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        if player_gesture in icons and icons[player_gesture] is not None:
            icon_player = cv2.resize(icons[player_gesture], (100, 100))
            frame[50:150, 300:400] = icon_player
        if computer_gesture in icons and icons[computer_gesture] is not None:
            icon_computer = cv2.resize(icons[computer_gesture], (100, 100))
            frame[50:150, 400:500] = icon_computer

        cv2.imshow("Pierre-Feuille-Ciseaux-Spock-Lezard", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
video_thread.join()

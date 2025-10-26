import time
import random
import pyautogui

# Configuration — modifie ici
INTERVAL = 5.0        # secondes entre actions
MOVE_RANGE = 50       # px amplitude des petits mouvements
CLICK_PROB = 0.02     # probabilité de clic par cycle (0-1)
JITTER = True         # True pour durée non nulle des mouvements
SAFE_CLICK = False    # True pour utiliser safe_click
SAFE_X = None         # X pour clic sûr (None -> centre écran)
SAFE_Y = None         # Y pour clic sûr (None -> centre écran)
DEBUG = False         # True pour afficher chaque action

pyautogui.FAILSAFE = True  # déplacer la souris en haut-gauche arrête le script

def safe_click(safe_x=None, safe_y=None):
    """Clique sur des coordonnées sûres (ou centre écran) puis restaure la position."""
    orig = pyautogui.position()
    try:
        screen_w, screen_h = pyautogui.size()
        tx = safe_x if safe_x is not None else screen_w // 2
        ty = safe_y if safe_y is not None else screen_h // 2
        tx = max(0, min(tx, screen_w - 1))
        ty = max(0, min(ty, screen_h - 1))
        pyautogui.moveTo(tx, ty, duration=0.08)
        pyautogui.click()
    finally:
        try:
            # pyautogui.Point a des attributs x,y
            pyautogui.moveTo(orig.x, orig.y, duration=0.05)
        except Exception:
            # fallback si orig est une tuple
            pyautogui.moveTo(orig, duration=0.05)

def run(interval=INTERVAL, move_range=MOVE_RANGE, click_prob=CLICK_PROB,
        jitter=JITTER, use_safe_click=SAFE_CLICK, safe_x=SAFE_X, safe_y=SAFE_Y,
        debug=DEBUG):
    print(f"Auto mouse démarré — interval={interval}s move_range={move_range}px click_prob={click_prob}")
    try:
        while True:
            dx = random.randint(-move_range, move_range)
            dy = random.randint(-move_range, move_range)
            dur = random.uniform(0.08, 0.30) if jitter else 0.02
            pyautogui.moveRel(dx, dy, duration=dur)
            if debug:
                print(f"moved rel ({dx},{dy}) dur={dur:.2f}")

            if random.random() < click_prob:
                if use_safe_click:
                    safe_click(safe_x, safe_y)
                    if debug:
                        print("safe click")
                else:
                    pyautogui.click()
                    if debug:
                        print("click")

            wait = random.uniform(interval * 0.85, interval * 1.15)
            if debug:
                print(f"sleep {wait:.2f}s")
            time.sleep(wait)
    except KeyboardInterrupt:
        print("Arrêt demandé par l'utilisateur.")
    except pyautogui.FailSafeException:
        print("Fail-safe déclenché : script arrêté (souris en coin).")

if __name__ == "__main__":
    run()
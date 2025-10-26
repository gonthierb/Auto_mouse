# ...existing code...
import time
import random
import argparse
import pyautogui

pyautogui.FAILSAFE = True  # déplace la souris en haut-gauche pour arrêter

def safe_click(safe_x=None, safe_y=None):
    """
    Effectue un clic sur des coordonnées sûres (si fournies) ou au centre de l'écran.
    Restaure ensuite la position de la souris.
    """
    orig = pyautogui.position()
    try:
        screen_w, screen_h = pyautogui.size()
        tx = safe_x if safe_x is not None else screen_w // 2
        ty = safe_y if safe_y is not None else screen_h // 2
        tx = max(0, min(tx, screen_w - 1))
        ty = max(0, min(ty, screen_h - 1))
        pyautogui.moveTo(tx, ty)
        pyautogui.click()
    finally:
        # restaurer la position d'origine
        try:
            pyautogui.moveTo(orig.x, orig.y)
        except Exception:
            # fallback si orig n'a pas les attributs attendus
            pyautogui.moveTo(orig)

def run(interval, move_range, click_prob, jitter, use_safe_click, safe_x, safe_y):
    try:
        print("Auto mouse démarré — boucles toutes les", interval, "s (CTRL+C pour arrêter)")
        while True:
            # petit mouvement aléatoire relatif
            dx = random.randint(-move_range, move_range)
            dy = random.randint(-move_range, move_range)
            # utiliser une durée non nulle pour rendre le mouvement visible
            dur = random.uniform(0.08, 0.30) if jitter else 0.08
            pyautogui.moveRel(dx, dy, duration=dur)

            # clic occasionnel
            if random.random() < click_prob:
                if use_safe_click:
                    safe_click(safe_x, safe_y)
                else:
                    pyautogui.click()

            # attente légèrement aléatoire pour paraître humain
            wait = random.uniform(interval * 0.85, interval * 1.15)
            time.sleep(wait)
    except KeyboardInterrupt:
        print("Arrêt demandé par l'utilisateur.")
    except pyautogui.FailSafeException:
        print("Fail-safe déclenché : script arrêté (souris en coin).")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Auto mouse mover")
    # valeurs par défaut plus visibles pour un double-clic sans arguments
    p.add_argument("--interval", type=float, default=5.0, help="Intervalle moyen en secondes entre actions")
    p.add_argument("--move-range", type=int, default=50, help="Amplitude (px) des petits mouvements")
    p.add_argument("--click-prob", type=float, default=0.02, help="Probabilité de clic à chaque cycle (0-1)")
    p.add_argument("--jitter", action="store_true", default=True, help="Ajouter durée aux mouvements pour les rendre plus humains (activé par défaut)")
    p.add_argument("--safe-click", action="store_true", help="Faire les clics dans un espace 'sûr' du bureau")
    p.add_argument("--safe-x", type=int, default=None, help="Coordonnée X pour clic sûr")
    p.add_argument("--safe-y", type=int, default=None, help="Coordonnée Y pour clic sûr")
    args = p.parse_args()

    run(args.interval, args.move_range, args.click_prob, args.jitter, args.safe_click, args.safe_x, args.safe_y)
# ...existing code...

# ...existing code...
import time
import random
import argparse
import pyautogui

pyautogui.FAILSAFE = True  # déplace la souris en haut-gauche pour arrêter

def run(interval, move_range, click_prob, jitter):
    try:
        while True:
            # petit mouvement aléatoire relatif
            dx = random.randint(-move_range, move_range)
            dy = random.randint(-move_range, move_range)
            dur = random.uniform(0.05, 0.4) if jitter else 0
            pyautogui.moveRel(dx, dy, duration=dur)

            # clic occasionnel
            if random.random() < click_prob:
                pyautogui.click()

            # attente légèrement aléatoire pour paraître humain
            wait = random.uniform(interval * 0.85, interval * 1.15)
            time.sleep(wait)
    except KeyboardInterrupt:
        print("Arrêt demandé par l'utilisateur.")
    except pyautogui.FailSafeException:
        print("Fail-safe déclenché : script arrêté (souris en coin).")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Auto mouse mover")
    p.add_argument("--interval", type=float, default=30.0, help="Intervalle moyen en secondes entre actions")
    p.add_argument("--move-range", type=int, default=10, help="Amplitude (px) des petits mouvements")
    p.add_argument("--click-prob", type=float, default=0.05, help="Probabilité de clic à chaque cycle (0-1)")
    p.add_argument("--jitter", action="store_true", help="Ajouter durée aux mouvements pour les rendre plus humains")
    args = p.parse_args()

    run(args.interval, args.move_range, args.click_prob, args.jitter)
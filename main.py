import time
import random
import argparse
import pyautogui

pyautogui.FAILSAFE = True  # déplace la souris en haut-gauche pour arrêter

# ...existing code...
# ajout : tentative d'import des modules Windows pour cliquer sur le "Desktop"
try:
    import win32gui
    import win32api
    import win32con
    WIN32_AVAILABLE = True
except Exception:
    WIN32_AVAILABLE = False

def safe_click(safe_x=None, safe_y=None):
    """
    Effectue un clic sur le fond de bureau si possible (pywin32),
    sinon sur des coordonnées sûres (si fournies) ou le centre de l'écran.
    Restaure ensuite la position de la souris.
    """
    orig = pyautogui.position()
    try:
        if WIN32_AVAILABLE:
            # handle Progman (Desktop)
            progman = win32gui.FindWindow("Progman", None)
            if progman:
                # client rect donne largeur/hauteur
                left, top, right, bottom = win32gui.GetClientRect(progman)
                w = right - left
                h = bottom - top
                cx = (safe_x if safe_x is not None else w // 2)
                cy = (safe_y if safe_y is not None else h // 2)
                # clamp
                cx = max(0, min(cx, w - 1))
                cy = max(0, min(cy, h - 1))
                # convertir coords client -> écran
                sx, sy = win32gui.ClientToScreen(progman, (cx, cy))
                win32api.SetCursorPos((sx, sy))
                # cliquer sur la fenêtre Desktop
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                return
        # fallback si pas de pywin32 ou progman introuvable
        screen_w, screen_h = pyautogui.size()
        tx = safe_x if safe_x is not None else screen_w // 2
        ty = safe_y if safe_y is not None else screen_h // 2
        tx = max(0, min(tx, screen_w - 1))
        ty = max(0, min(ty, screen_h - 1))
        pyautogui.moveTo(tx, ty)
        pyautogui.click()
    finally:
        pyautogui.moveTo(orig)  # revenir à la position initiale

def run(interval, move_range, click_prob, jitter, use_safe_click, safe_x, safe_y):
    try:
        while True:
            # petit mouvement aléatoire relatif
            dx = random.randint(-move_range, move_range)
            dy = random.randint(-move_range, move_range)
            dur = random.uniform(0.05, 0.4) if jitter else 0
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
    p.add_argument("--interval", type=float, default=30.0, help="Intervalle moyen en secondes entre actions")
    p.add_argument("--move-range", type=int, default=10, help="Amplitude (px) des petits mouvements")
    p.add_argument("--click-prob", type=float, default=0.05, help="Probabilité de clic à chaque cycle (0-1)")
    p.add_argument("--jitter", action="store_true", help="Ajouter durée aux mouvements pour les rendre plus humains")
    p.add_argument("--safe-click", action="store_true", help="Faire les clics dans un espace 'sûr' du bureau")
    p.add_argument("--safe-x", type=int, default=None, help="Coordonnée X (client desktop ou écran) pour clic sûr")
    p.add_argument("--safe-y", type=int, default=None, help="Coordonnée Y (client desktop ou écran) pour clic sûr")
    args = p.parse_args()

    run(args.interval, args.move_range, args.click_prob, args.jitter, args.safe_click, args.safe_x, args.safe_y)
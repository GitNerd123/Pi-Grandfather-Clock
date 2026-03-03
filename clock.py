import time
import pygame
import threading
import sys
import os
from datetime import datetime

# --- CONFIGURATION ---
NIGHT_START = 23  # 11 PM (24-hour format)
NIGHT_END = 7     # 7 AM
# ---------------------

# Initialize mixer
pygame.mixer.init()
chime_lock = threading.Lock()

# Detect Operating System for Keyboard Input
OS_TYPE = "windows" if os.name == 'nt' else "linux"

if OS_TYPE == "windows":
    import msvcrt
else:
    import select, termios, tty

def is_night():
    """Returns True if current time is within the silent window."""
    hour = datetime.now().hour
    if NIGHT_START > NIGHT_END:
        return hour >= NIGHT_START or hour < NIGHT_END
    return NIGHT_START <= hour < NIGHT_END

def play_test(sound_type):
    """Manual tests always work, even in Night Mode."""
    if not chime_lock.acquire(blocking=False):
        return
    try:
        print(f"\n[!] RUNNING TEST: {sound_type.upper()}")
        if sound_type == "melody":
            pygame.mixer.music.load("westminster.wav")
            pygame.mixer.music.play(fade_ms=2000)
            while pygame.mixer.music.get_busy(): time.sleep(0.1)
        elif sound_type == "strike":
            s = pygame.mixer.Sound("strike.wav")
            s.play()
            time.sleep(4) 
    finally:
        chime_lock.release()

def get_timer_bar():
    now = datetime.now()
    rem = 3600 - (now.minute * 60 + now.second)
    percent = (3600 - rem) / 3600
    bar = "█" * int(20 * percent) + "░" * (20 - int(20 * percent))
    
    status = "🌙 SILENT" if is_night() else "🔔 ACTIVE"
    return f"\r {now.strftime('%H:%M:%S')} |{bar}| {rem//60:02d}m {rem%60:02d}s until chime ({status})   "

def check_keyboard():
    if OS_TYPE == "windows":
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8').lower()
    else:
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1).lower()
    return None

def clock_thread():
    while True:
        now = datetime.now()
        if now.minute == 0 and now.second == 0:
            # Check Night Mode before chiming automatically
            if is_night():
                print(f"\n[🌙] Night Mode: Skipping chime at {now.hour}:00")
            else:
                if chime_lock.acquire(blocking=False):
                    try:
                        pygame.mixer.music.load("westminster.wav")
                        pygame.mixer.music.play(fade_ms=2000)
                        while pygame.mixer.music.get_busy(): time.sleep(0.1)
                        cnt = now.hour % 12 or 12
                        s = pygame.mixer.Sound("strike.wav")
                        for _ in range(cnt):
                            s.play()
                            time.sleep(3)
                    finally:
                        chime_lock.release()
            time.sleep(60)
        time.sleep(0.5)

# Start background clock
threading.Thread(target=clock_thread, daemon=True).start()

# Linux-only setup
old_settings = None
if OS_TYPE == "linux":
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

print(f"🕰️  UNIVERSAL CLOCK LOADED ({OS_TYPE.upper()})")
print(f"🌙 Night Mode: {NIGHT_START}:00 to {NIGHT_END}:00")
print("Tap '1' for Melody | Tap '2' for Strike | 'q' to Quit\n")

try:
    while True:
        sys.stdout.write(get_timer_bar())
        sys.stdout.flush()

        key = check_keyboard()
        if key == '1':
            threading.Thread(target=play_test, args=("melody",)).start()
        elif key == '2':
            threading.Thread(target=play_test, args=("strike",)).start()
        elif key == 'q' or key == '\x1b':
            break
        
        time.sleep(0.1)
except KeyboardInterrupt:
    # This catches the Ctrl+C so it doesn't show the Traceback
    pass 
finally:
    if OS_TYPE == "linux" and old_settings:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    print("\n[✔] Clock safely powered down. See you next time!")
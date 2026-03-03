# 🕰️ Pi-Grandfather-Clock (PiGfC)

> "I dreamed of owning a massive grandfather clock. Since I couldn't fit one in my room, I used AI to build this high-fidelity digital version for my Pi."

---

## 🚀 Quick Setup

### 1️⃣ Install Dependencies

**Windows**
```bash
pip install pygame-ce
```

**DietPi / Linux**
```bash
sudo apt install python3-pygame alsa-utils -y
```

---

### 2️⃣ Download & Cut Audio

Run these commands in order:

```bash
# 1. Download source audio
python -m yt_dlp -x --audio-format wav -o "master.wav" "https://www.youtube.com/watch?v=nj3hJ1OrLTw"

# 2. Cut Westminster melody
ffmpeg -i master.wav -ss 00:00:00 -t 00:00:19 -c copy westminster.wav

# 3. Cut strike sound
ffmpeg -i master.wav -ss 00:00:20 -t 00:00:05 -c copy strike.wav
```

---

### 3️⃣ Run It

```bash
python script.py
```

---

## 🎮 Controls & Features

- 🌙 **Night Mode**  
  Silent from 11 PM to 7 AM  
  (Edit `NIGHT_START` inside the script)

- 🔕 **Anti-Spam Protection**  
  Prevents overlapping sounds

- ⌨️ **Keyboard Controls**
  - `1` → Play Melody  
  - `2` → Play Strike  
  - `q` → Quit  

---

## 📂 Required Files (Same Folder)

```
script.py
westminster.wav
strike.wav
```

---

Created with passion & Gemini.

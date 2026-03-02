# 🕰️ Pi-Grandfather-Clock (PiGfC)

### *The dream of a classic chime, powered by code.*

---

## 📖 The Backstory
I always had this dream of owning a real, massive grandfather clock—the kind that fills a room with that deep, steady tick and a resonant chime. Since I couldn't fit a 7-foot wooden clock in my setup yet, I teamed up with AI to build the next best thing: a high-fidelity digital version that runs 24/7 on my Pi. 

**PiGfC** transforms any computer into a majestic timepiece with zero compromises on sound quality.

---

## 🚀 Features
* **Universal Core:** Runs on **Windows** and **Linux (DietPi/Raspberry Pi)** automatically.
* **Smooth Transitions:** Built-in **Fade-In** for melodies and **Fade-Out** for strikes.
* **Anti-Spam Protection:** Internal locking ensures audio doesn't overlap or glitch if keys are pressed rapidly.
* **Live Dashboard:** Real-time progress bar counting down to the next hour.

---

## 🛠️ Simple Setup

### 1. Install Dependencies
Ensure you have Python installed, then run the command for your system:

* **Windows:** `pip install pygame-ce`
* **DietPi/Linux:** `sudo apt install python3-pygame alsa-utils -y`

### 2. Prepare the Audio
We use `yt-dlp` and `ffmpeg` to get the perfect tones.

```bash
# 1. Download the high-quality master file
python -m yt_dlp -x --audio-format wav -o "master.wav" "[https://www.youtube.com/watch?v=nj3hJ1OrLTw](https://www.youtube.com/watch?v=nj3hJ1OrLTw)"

# 2. Extract the Westminster Melody
ffmpeg -i master.wav -ss 00:00:00 -t 00:00:19 -c copy westminster.wav

# 3. Extract the Single Strike Bong
ffmpeg -i master.wav -ss 00:00:20 -t 00:00:05 -c copy strike.wav

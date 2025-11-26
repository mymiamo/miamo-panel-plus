# Miamo Panel +

A console-based request automation tool with optional proxy rotation and SEO data extraction (page title & meta description).

---
░███     ░███ ░██                                         ░█████████                                   ░██            
░████   ░████                                             ░██     ░██                                  ░██            
░██░██ ░██░██ ░██ ░██████   ░█████████████   ░███████     ░██     ░██  ░██████   ░████████   ░███████  ░██      ░██   
░██ ░████ ░██ ░██      ░██  ░██   ░██   ░██ ░██    ░██    ░█████████        ░██  ░██    ░██ ░██    ░██ ░██    ░██████ 
░██  ░██  ░██ ░██ ░███████  ░██   ░██   ░██ ░██    ░██    ░██          ░███████  ░██    ░██ ░█████████ ░██      ░██   
░██       ░██ ░██░██   ░██  ░██   ░██   ░██ ░██    ░██    ░██         ░██   ░██  ░██    ░██ ░██        ░██            
░██       ░██ ░██ ░█████░██ ░██   ░██   ░██  ░███████     ░██          ░█████░██ ░██    ░██  ░███████  ░██    
---
## 🚀 Features

- Send multiple HTTP/HTTPS requests to a target URL
- Optional proxy support (built-in or custom)
- Extracts:
  - `<title>` tag
  - `<meta name="description">` or `og:description`
- Clean console output without terminal freezing on interrupt

---

## ⚙️ Installation

Install all required dependencies using the included `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## ▶️ Quick Usage (Windows)

Run `start.bat` for one-click fast launch:

```bat
start.bat
```

---

## 🧪 Manual Start (Alternative)

```bash
python main.py
```

---

## 📁 Project Files

| File | Description |
|------|-------------|
| `main.py` | Main Panel + |
| `requirements.txt` | Dependency list |
| `start.bat` | One-click launcher |
| Proxy list | Built-in rotating proxies (HTTP recommended) |

---

## ✅ Recommended Workflow

1. Open the project folder  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start using:
   ```bat
   start.bat
   ```

---

## 🪟 Windows Notes

- Pressing **CTRL + C** returns to `main.py` instantly without freezing the console.
- If the `py` launcher does not work, use `python main.py` instead.

---

## 📜 License

Free for educational use.  
Unauthorized commercial distribution or republishing is prohibited.

---

## 🤝 Contribution

Pull requests are welcome.  
You can help improve:

- Proxy sources
- Console UI feedback (sounds, progress bars, animations)
- Request error handling and retries

---

### Optional legacy batch command example:

```bat
@echo off
py main.py
```

### SMS Bomb by. @tingirifistik

[GITHUB](https://github.com/tingirifistik/Enough-Reborn)



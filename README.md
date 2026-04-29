# Prompt Generator with Gemini API

A web application that generates optimized prompt variations using the Gemini API via OpenClaw integration.

## 📋 Prerequisites

- Python 3.10+
- Virtual environment (`.venv`) already set up
- Gemini API key configured in `app.py`

## 🚀 Quick Start (Two-Terminal Setup)

### Terminal 1: Start the Gemini Adapter

This is the API backend that connects to Gemini.

```powershell
cd c:\Users\swintern\gemini-adapter
.\.venv\Scripts\Activate.ps1
python app.py
```

**Expected output:**
```
==================================================
  Gemini Adapter  →  http://127.0.0.1:5000
  Model          : gemini-2.5-flash
==================================================
 * Running on http://127.0.0.1:5000
```

✅ Leave this terminal running.

---

### Terminal 2: Start the Prompt Generator

This is the web interface where you'll generate and test prompts.

```powershell
cd c:\Users\swintern\gemini-adapter
.\.venv\Scripts\Activate.ps1
python prompt_generator.py
```

**Expected output:**
```
============================================================
  Prompt Generator (OpenClaw Integration)
  → http://127.0.0.1:3001
  Powered by Gemini API
============================================================
 * Running on http://127.0.0.1:3001
```

✅ Leave this terminal running.

---

## 🌐 Access the Application

Open your browser and go to:

```
http://127.0.0.1:3001
```

## 📖 How to Use

### 1. **Generate Prompt Variations**
   - Enter your base prompt in the "Original Prompt" box
   - Set the number of variations (1-10)
   - Click **"Generate Variations"**
   - Wait for Gemini to generate optimized versions

### 2. **Copy Variations**
   - Click **"Copy"** on any variation to copy it to your clipboard
   - Use in your own projects or tools

### 3. **Test Variations**
   - Click **"Test"** on any variation to send it to Gemini
   - See the response in real-time
   - Or paste any prompt in the "Test Prompt Variations" section and click **"Test Prompt"**

## 🔧 Configuration

### Change the Model
Edit `prompt_generator.py` or `app.py` to change the Gemini model:

```python
MODEL_NAME = "gemini-2.5-flash"  # Change this
```

Available models:
- `gemini-2.5-flash` (Fast, recommended)
- `gemini-2.5-pro` (More powerful)

### Change the Port
Edit the last line of `prompt_generator.py`:

```python
app.run(host="127.0.0.1", port=3001, debug=True)  # Change port here
```

## 📁 File Structure

```
gemini-adapter/
├── app.py                      # Gemini API adapter (port 5000)
├── prompt_generator.py         # Web server for prompt generator (port 3001)
├── prompt_generator.html       # Web UI (loaded by Flask)
├── .venv/                      # Virtual environment
└── README.md                   # This file
```

## ⚡ Troubleshooting

### "Connection refused" on port 5000
- Make sure `app.py` is running in Terminal 1
- Check that port 5000 is not in use: `netstat -ano | findstr :5000`

### "Connection refused" on port 3001
- Make sure `prompt_generator.py` is running in Terminal 2
- Check that port 3001 is not in use: `netstat -ano | findstr :3001`

### "No module named 'flask'" or "No module named 'google.generativeai'"
- Activate the virtual environment:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- Install packages:
  ```powershell
  pip install flask google-generativeai requests
  ```

### Variations not showing up
- Check that `app.py` (Gemini adapter) is running
- Check browser console for errors (F12 → Console tab)

## 🔐 Security Notes

- The Gemini API key is stored in `app.py` - keep it private!
- Don't share your API key with others
- This is a development setup - use proper authentication for production

## 📊 Architecture

```
Your Browser (http://127.0.0.1:3001)
        ↓
   Prompt Generator (port 3001)
        ↓
   Gemini Adapter (port 5000)
        ↓
   Gemini API (Google)
```

## 🎯 Example Workflows

### Workflow 1: Generate & Test
1. Enter: "Write a blog post about AI"
2. Click "Generate Variations"
3. Review the 5 variations
4. Click "Test" on your favorite
5. See Gemini's response

### Workflow 2: Copy for External Use
1. Generate variations
2. Click "Copy" on the best one
3. Paste it in ChatGPT, Claude, or another tool
4. Compare results between different AI models

### Workflow 3: Batch Optimization
1. Generate 5 variations
2. Test each one
3. Keep the one with the best output
4. Use that for production

## 💡 Tips

- **Start simple**: Begin with short prompts, then add complexity
- **Test variations**: Don't assume the first one is best
- **Copy & compare**: Test the same variation in different AI models
- **Iterate**: Use Gemini's responses to refine your original prompt

## 🛑 Stopping the Application

1. **Terminal 1** (Adapter): Press `Ctrl+C`
2. **Terminal 2** (Generator): Press `Ctrl+C`

Both servers will shut down cleanly.

---

**Ready to generate prompts? Let's go! 🚀**

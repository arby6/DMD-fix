# DMD-fix – Discord Message Deleter

DMD-fix is a faster and more stable fork of DMD (Discord Message Deleter) originally created by TheRealMrDjango.

This version is maintained and modified by Arby (rby6). It improves performance and reliability while keeping the same core idea: automatically deleting Discord messages from channels or DMs the downside is that it is not gonna come pre-compiled so you'll either have to manually compile it or just run the script.

---

## What it does

DMD-fix automates:

- Fetching messages from Discord channels or DMs
- Bulk deleting messages
- Handling rate limits automatically
- Running everything locally on your computer

---

## Key improvements in DMD-fix

Compared to the original DMD, this fork includes:

- Faster deletion loop
- More stable handling of rate limits
- Reduced delays between actions
- Improved reliability during long sessions

---

## Security and privacy

- Runs entirely on your local machine
- No data is sent to external servers
- Uses RAM only (no files saved to disk)
- All session data is cleared when the app is closed

Note: The tool uses your Discord authentication from a browser request. Keep it private and never share it.

---

## Download

Prebuilt versions are available (no Python required).

### Windows
1. Go to the Releases page  
2. Download `DMD.exe`  
3. Run the application  

### macOS
1. Go to the Releases page  
2. Download `DMD.app` (zip)  
3. Unzip and open it  
   - You may need to allow it in system security settings

---

## How to use

### Step 1: Get the fetch request

1. Open Discord in your browser  
2. Open the channel or DM you want to clean  
3. Open Developer Tools (F12)  
4. Go to the Network tab  
5. Scroll to load messages  
6. Find `messages?limit=50`  
7. Copy it as a fetch request  

---

### Step 2: Run DMD-fix

1. Paste the fetch request into the app  
2. Start the cleaning process  
3. The tool will automatically delete messages in a loop  

---

### Step 3: Finish

Close the app when done. Since it runs in RAM, nothing is saved to disk.

---

## Run from source (developers)

```bash
pip install -r requirements.txt
python gui.py

### This folder contains mini project of using voice assistant with online services

Create the venv
```bash
   get the Microsoft Visual Studio
   python -m venv venv
```

If strugles of creating venv theen execute this code:
```bash
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
   python -m venv venv
   # or
   C:\Users\vboxuser\AppData\Local\Programs\Python\Python311\python.exe -m venv venv
```

Now activate the venv
```bash
   ./venv/Script/activate
   # or
   .\venv\Scripts\activate
   # or
   ./venv/Scripts/Activate.ps1
```

To install necessary libraries:
```bash
pip install -r requirements_s.txt
```

To run the program:
```bash
python voice_assistant_online.py
```
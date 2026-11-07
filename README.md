# MICHAEL-LAUNCHER

**Michael Launcher** is a lightweight, high-performance, and secure custom Minecraft launcher. It allows users to instantly choose between a clean **Vanilla** game or a fully optimized **Fabric** modded environment.

This project is open-source and distributed under the **MIT License**.

## ✨ Features

* **Interactive Engine Menu:** Prompts the player at boot to select their preferred client setup (1 — Vanilla, 2 — Fabric).
* **Automated Mod Workflow:** If Fabric is selected, the launcher instantly generates and opens the `%appdata%\.michael_launcher\minecraft\mods` folder via Windows File Explorer. Or portable.
* **Zero-Admin Architecture:** Downloads all core assets and required Java runtimes directly into user profiles. Works seamlessly on shared, managed, or school PCs without demanding administrative privileges.
* **Live Progress Engine:** Reports accurate asset/library downloads and install steps inside the terminal.

## 🚀 How to Run

### Run from Source (Python)
1. Install the required client core dependency:
   pip install minecraft-launcher-lib
   
2. Execute the main script launcher file

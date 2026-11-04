# ====================================================================
# MICHAEL LAUNCHER — Strict 1.21.11 (Vanilla / Fabric Choice)
# License: MIT (Free to use, Open Source)
# ====================================================================

import os
import subprocess
import minecraft_launcher_lib

BASE_DIR = os.path.join(os.environ["APPDATA"], ".michael_launcher")
GAME_DIR = os.path.join(BASE_DIR, "minecraft") 
MODS_DIR = os.path.join(GAME_DIR, "mods")

# Зашиваем строго версию 1.21.11!
MINECRAFT_VERSION = "1.21.11"

max_val = 0

def set_status(status: str):
    print(f"[Status] {status}")

def set_maximum(value: int):
    global max_val
    max_val = value

def set_progress(value: int):
    global max_val
    if max_val > 0:
        percentage = int((value / max_val) * 100)
        print(f"\rDownloading game assets: [{value}/{max_val}] {percentage}%", end="", flush=True)

callback = {
    "setStatus": set_status,
    "setMaximum": set_maximum,
    "setProgress": set_progress
}

print("=========================================")
print("       WELCOME TO MICHAEL LAUNCHER       ")
print("=========================================")

# 1. Запрос никнейма
user_nickname = input("Enter your in-game nickname: ").strip()
if not user_nickname:
    user_nickname = "MichaelPlayer"

# 2. Выбор режима игры
print("\nChoose version type:")
print("1 - Vanilla (Clean Game)")
print("2 - Fabric (With Mods)")
choice = input("Enter 1 or 2: ").strip()

# Если игрок ошибся или ничего не ввёл, по умолчанию выберем ванилу
if choice != "2":
    choice = "1"

print(f"\n[Loading] Hello, {user_nickname}! Running setup...")

# Если выбрали Фабрик — создаем и автоматически открываем папку для модов
if choice == "2":
    os.makedirs(MODS_DIR, exist_ok=True)
    print("[Launcher] Opening mods folder for you...")
    os.startfile(MODS_DIR)

try:
    # Скачиваем базовую версию (нужна в обоих случаях)
    print("[Minecraft] Syncing base version 1.21.11 files...")
    minecraft_launcher_lib.install.install_minecraft_version(
        version=MINECRAFT_VERSION, 
        minecraft_directory=GAME_DIR, 
        callback=callback
    )

    # Если выбрали Фабрик, накатываем загрузчик модов
    if choice == "2":
        print("\n[ModLoader] Installing Fabric Loader for 1.21.11...")
        minecraft_launcher_lib.fabric.install_fabric(
            minecraft_version=MINECRAFT_VERSION,
            minecraft_directory=GAME_DIR,
            callback=callback
        )

except Exception as network_error:
    print(f"\n[Network Info] Switched to offline assets mode: {network_error}")

# Определение финальной версии для запуска
try:
    if choice == "2":
        installed_versions = minecraft_launcher_lib.utils.get_installed_versions(GAME_DIR)
        target_version = next((v["id"] for v in installed_versions if "1.21.11" in v["id"] and "fabric" in v["id"].lower()), None)
        
        if not target_version:
            print("\n[Launcher] Fabric failed to compile. Falling back to Vanilla.")
            target_version = MINECRAFT_VERSION
        else:
            print(f"[Launcher] Running Stable Fabric Engine: {target_version}")
    else:
        target_version = MINECRAFT_VERSION
        print(f"[Launcher] Running Vanilla {MINECRAFT_VERSION}")

    # Настройки параметров запуска
    options = {
        "username": user_nickname,
        "uuid": "00000000-0000-0000-0000-000000000000",
        "token": "0",
        "jvmArguments": ["-Xmx4G", "-Xms2G"]
    }

    launch_command = minecraft_launcher_lib.command.get_minecraft_command(target_version, GAME_DIR, options)
    
    print(f"\n[Launch] Initializing Minecraft {target_version} as {user_nickname}!")
    print("Enjoy your game!")
    subprocess.run(launch_command)

except Exception as launch_error:
    print(f"\n[Critical Error] Runtime crash: {launch_error}")
    input("\nPress Enter to close this window...")

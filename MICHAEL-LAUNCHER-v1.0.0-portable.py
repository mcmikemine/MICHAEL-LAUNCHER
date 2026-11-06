# ====================================================================
# MICHAEL LAUNCHER — Strict 1.21.11 (Vanilla / Fabric Choice)
# Portable Edition: игра и Java хранятся рядом со скриптом
# License: MIT (Free use, Open Source)
# ====================================================================

import os
import subprocess
import minecraft_launcher_lib

# --- Портативный режим: базовая папка = папка со скриптом ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GAME_DIR = os.path.join(BASE_DIR, "minecraft")
MODS_DIR = os.path.join(GAME_DIR, "mods")

# Зашиваем строго версию 1.21.11!
MINECRAFT_VERSION = "1.21.11"

# Официальный рантайм Mojang: Java 21 для версий 1.20.5+
JAVA_RUNTIME = "java-runtime-delta"

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
        print(f"\rDownloading: [{value}/{max_val}] {percentage}%", end="", flush=True)


callback = {
    "setStatus": set_status,
    "setMaximum": set_maximum,
    "setMax": set_maximum,
    "setProgress": set_progress
}


def ensure_java() -> str:
    """Возвращает путь к Java. Сначала смотрит в портативный рантайм,
    если его нет — скачивает. Если и это не вышло — системную Java."""
    try:
        java_path = minecraft_launcher_lib.runtime.get_executable_path(JAVA_RUNTIME, GAME_DIR)
        if java_path:
            print(f"[Java] Portable Java found: {java_path}")
            return java_path

        print("[Java] No portable Java found. Downloading official Mojang runtime...")
        minecraft_launcher_lib.runtime.install_jvm_runtime(
            jvm_version=JAVA_RUNTIME,
            minecraft_directory=GAME_DIR,
            callback=callback
        )

        java_path = minecraft_launcher_lib.runtime.get_executable_path(JAVA_RUNTIME, GAME_DIR)
        if java_path:
            print(f"[Java] Portable Java installed: {java_path}")
            return java_path
    except Exception as java_error:
        print(f"[Java] Portable runtime failed: {java_error}")

    print("[Java] Falling back to system Java...")
    return "java"


print("=========================================")
print("       WELCOME TO MICHAEL LAUNCHER       ")
print("=========================================")
print(f"[Launcher] Portable folder: {BASE_DIR}\n")

# 1. Запрос никнейма
user_nickname = input("Enter your in-game nickname: ").strip()
if not user_nickname:
    user_nickname = "MichaelPlayer"

# 2. Выбор режима игры
print("\nChoose version type:")
print("1 - Vanilla (Clean Game)")
print("2 - Fabric (With Mods)")
choice = input("Enter 1 or 2: ").strip()

# Если игрок ошибся или ничего не ввёл — по умолчанию ванила
if choice != "2":
    choice = "1"

print(f"\n[Loading] Hello, {user_nickname}! Running setup...")

# Если выбрали Фабрик — создаём и сразу открываем папку для модов
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

    # Если выбрали Фабрик — накатываем загрузчик модов
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
        target_version = next(
            (v["id"] for v in installed_versions if "1.21.11" in v["id"] and "fabric" in v["id"].lower()),
            None
        )

        if not target_version:
            print("\n[Launcher] Fabric failed to compile. Falling back to Vanilla.")
            target_version = MINECRAFT_VERSION
        else:
            print(f"[Launcher] Running Stable Fabric Engine: {target_version}")
    else:
        target_version = MINECRAFT_VERSION
        print(f"[Launcher] Running Vanilla {MINECRAFT_VERSION}")

    # Гарантируем наличие Java (портативной или системной)
    java_path = ensure_java()

    # Настройки параметров запуска
    options = {
        "username": user_nickname,
        "uuid": "00000000-0000-0000-0000-000000000000",
        "token": "0",
        "jvmArguments": ["-Xmx4G", "-Xms2G"],
        "executablePath": java_path
    }

    launch_command = minecraft_launcher_lib.command.get_minecraft_command(target_version, GAME_DIR, options)

    print(f"\n[Launch] Initializing Minecraft {target_version} as {user_nickname}!")
    print("Enjoy your game!")
    subprocess.run(launch_command, cwd=GAME_DIR)

except Exception as launch_error:
    print(f"\n[Critical Error] Runtime crash: {launch_error}")
    input("\nPress Enter to close this window...")

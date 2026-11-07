# ====================================================================
# MICHAEL LAUNCHER — Version 1.1.0
# ALL Minecraft releases starting with 1.X.X and 26.X (Mojang manifest)
# License: MIT (Free to use, Open Source)
# ====================================================================

import os
import json
import subprocess
import urllib.request
import minecraft_launcher_lib

LAUNCHER_VERSION = "1.1.0"
CHANGELOG = {
    "1.1.0": [
        "All Minecraft releases starting with 1.X.X and 26.X (Mojang manifest)",
        "Offline fallback: cached version list or built-in version list",
        "Direct manifest download if the library has no version-list function",
        "Update names and dates shown next to versions (English)",
        "Paged version selection: pick by number or type a full version",
        "Automatic Java requirement detection for every version",
        "Vanilla / Fabric choice for any version",
        "Separate mods folder for each game version",
        "Auto Java selection on the system",
        "Nickname database (JSON) — choose from saved or enter new",
    ],
    "1.0.0": [
        "Initial release: 1.21.11 only, Vanilla / Fabric choice",
    ],
}

# ------------------------- Paths -------------------------
# Standard storage: %APPDATA%\.michael_launcher
BASE_DIR = os.path.join(os.environ["APPDATA"], ".michael_launcher")
GAME_DIR = os.path.join(BASE_DIR, "minecraft")
NICK_DB = os.path.join(BASE_DIR, "nicknames.json")
VERSIONS_CACHE = os.path.join(BASE_DIR, "versions_cache.json")

MOJANG_MANIFEST = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

# Built-in list for the case when there is no network and no cache
FALLBACK_VERSIONS = [
    "1.21.11", "1.21.10", "1.21.9", "1.21.8", "1.21.5", "1.21.4", "1.21.1",
    "1.20.6", "1.20.4", "1.20.1",
    "1.19.4", "1.19.2",
    "1.18.2",
    "1.17.1",
    "1.16.5", "1.16.4", "1.16.1",
    "1.15.2", "1.14.4", "1.12.2", "1.8.9", "1.7.10",
]

# Java search paths (edit to match your system if auto-search fails)
JAVA_CANDIDATES = [
    r"C:\Program Files\Java",
    r"C:\Program Files\Eclipse Adoptium",
    r"C:\Program Files (x86)\Java",
    r"C:\Program Files\Microsoft\jdk-21",
    r"C:\Program Files\Microsoft\jdk-17",
    r"C:\Program Files\Microsoft\jdk-11",
]

# Starting nickname database — created empty on first run
DEFAULT_NICKNAMES = []

# Version history reference: key — major version, value — name and release date
VERSION_HISTORY = {
    "1.0":  ("Official release: The End and the Ender Dragon", "November 18, 2011"),
    "1.1":  ("Spawn eggs, superflat worlds", "January 2012"),
    "1.2":  ("Jungles, ocelots, iron golems", "March 2012"),
    "1.3":  ("Villager trading, emeralds", "August 2012"),
    "1.4":  ("Witches, item frames, carrots and potatoes", "October 2012"),
    "1.5":  ("Redstone Update: hoppers, comparators, daylight sensors", "March 2013"),
    "1.6":  ("Horse Update: horses, leads, coal blocks", "July 2013"),
    "1.7":  ("The Update that Changed the World: new biomes", "October 2013"),
    "1.8":  ("Bountiful Update: oceans, prismarine, armor stands", "September 2014"),
    "1.9":  ("Combat Update: shields, off-hand, elytra", "February 2016"),
    "1.10": ("Frostburn Update: polar bears, magma blocks, fossils", "June 2016"),
    "1.11": ("Exploration Update: woodland mansions, shulker boxes, llamas", "November 2016"),
    "1.12": ("World of Color Update: concrete, recipe book, parrots", "June 2017"),
    "1.13": ("Update Aquatic: dolphins, coral, tridents", "July 2018"),
    "1.14": ("Village & Pillage: villages, raids, crossbows", "April 2019"),
    "1.15": ("Buzzy Bees: bees, honey", "December 2019"),
    "1.16": ("Nether Update: netherite, new Nether biomes", "June 2020"),
    "1.17": ("Caves & Cliffs Part 1: new ores", "2021"),
    "1.18": ("Caves & Cliffs Part 2: new cave and mountain generation", "2021"),
    "1.19": ("The Wild Update: Deep Dark, Warden, mangrove swamps", "June 2022"),
    "1.20": ("Trails & Tales: archaeology, cherry biome, sniffers", "June 2023"),
    "1.21": ("Tricky Trials: trial chambers, breeze, copper blocks", "June 2024"),
    "1.21.4":  ("The Garden Awakens", "2024"),
    "1.21.5":  ("Spring to Life", "2025"),
    "1.21.9":  ("The Copper Age", "2025"),
    "1.21.11": ("Mounts of Mayhem", "December 2025"),
    "26":   ("2026 updates: new version numbering system", "2026"),
}


def get_version_info(version: str) -> str:
    """Returns 'Name (date)' for a version if it is in the reference."""
    if version in VERSION_HISTORY:
        name, date = VERSION_HISTORY[version]
        return f"{name} ({date})"
    if version.startswith("26."):
        name, date = VERSION_HISTORY["26"]
        return f"{name} ({date})"
    parts = version.split(".")
    if len(parts) >= 2:
        major_key = ".".join(parts[:2])
        if major_key in VERSION_HISTORY:
            name, date = VERSION_HISTORY[major_key]
            return f"{name} ({date})"
    return ""


# ------------------------- Nickname database -------------------------

def load_nick_db() -> list:
    if os.path.isfile(NICK_DB):
        try:
            with open(NICK_DB, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
        except (json.JSONDecodeError, OSError):
            pass
    save_nick_db(DEFAULT_NICKNAMES)
    return list(DEFAULT_NICKNAMES)


def save_nick_db(nicknames: list):
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(NICK_DB, "w", encoding="utf-8") as f:
        json.dump(nicknames, f, ensure_ascii=False, indent=2)


def add_nickname(nickname: str):
    nicknames = load_nick_db()
    if nickname not in nicknames:
        nicknames.append(nickname)
        save_nick_db(nicknames)


# ------------------------- Version list cache -------------------------

def save_versions_cache(versions: list):
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(VERSIONS_CACHE, "w", encoding="utf-8") as f:
        json.dump(versions, f, indent=2)


def load_versions_cache() -> list:
    if os.path.isfile(VERSIONS_CACHE):
        try:
            with open(VERSIONS_CACHE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list) and data:
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return []


# ------------------------- Download progress -------------------------

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

# ------------------------- Version list -------------------------

def fetch_versions_online() -> list:
    """Tries to fetch the version list: via the library first, then directly."""
    utils = minecraft_launcher_lib.utils

    # 1. Via the library — the function name depends on the library version
    for attr in ("get_minecraft_version_list", "get_minecraft_versions"):
        fn = getattr(utils, attr, None)
        if fn is None:
            continue
        try:
            data = fn()
        except Exception:
            continue
        if isinstance(data, dict) and "versions" in data:
            data = data["versions"]
        if isinstance(data, list):
            releases = [v["id"] for v in data
                        if isinstance(v, dict)
                        and v.get("type") == "release"
                        and str(v.get("id", ""))[:1].isdigit()]
            if releases:
                return releases

    # 2. Directly from the Mojang manifest — works with any library version
    try:
        with urllib.request.urlopen(MOJANG_MANIFEST, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        releases = [v["id"] for v in data.get("versions", [])
                    if v.get("type") == "release" and v["id"][:1].isdigit()]
        if releases:
            return releases
    except Exception:
        pass

    return []


def get_release_versions() -> list:
    """All 1.X.X and 26.X releases, newest first, with offline cache."""
    releases = fetch_versions_online()
    if releases:
        save_versions_cache(releases)
        return releases

    cached = load_versions_cache()
    if cached:
        print("[Launcher] Using cached version list (offline mode).")
        return cached

    print("[Launcher] No cache. Using built-in version list.")
    return list(FALLBACK_VERSIONS)


def get_required_java(version: str) -> int:
    """Heuristic: which major Java version is required."""
    if not version.startswith("1."):
        return 21          # new 26.x numbering — definitely Java 21+
    try:
        parts = version.split(".")
        minor = int(parts[1]) if len(parts) > 1 else 0
        patch = int(parts[2]) if len(parts) > 2 else 0
    except ValueError:
        return 8
    if minor > 20 or (minor == 20 and patch >= 5):
        return 21      # 1.20.5+ and all newer
    if minor >= 18:
        return 17      # 1.18 — 1.20.4
    if minor == 17:
        return 16      # 1.17.x
    return 8           # 1.16.5 and older


def choose_version() -> str:
    print("\nLoading version list from Mojang manifest...")
    versions = get_release_versions()
    print(f"[Launcher] Found {len(versions)} releases")

    page = 0
    per_page = 15
    while True:
        start = page * per_page
        chunk = versions[start:start + per_page]
        if not chunk:
            page = 0
            continue

        print(f"\n--- Page {page + 1} of {(len(versions) - 1) // per_page + 1} ---")
        for i, ver in enumerate(chunk, start=1):
            java_req = get_required_java(ver)
            info = get_version_info(ver)
            suffix = f" — {info}" if info else ""
            print(f"{i} - {ver} (Java {java_req}+){suffix}")
        print("'n' next page / 'p' previous page")

        print("\nOr type a full version (e.g. 1.20.1)")
        pick = input("Your choice: ").strip().lower()

        if pick == "n":
            if start + per_page < len(versions):
                page += 1
            continue
        if pick == "p":
            if page > 0:
                page -= 1
            continue
        if pick.isdigit() and 1 <= int(pick) <= len(chunk):
            return chunk[int(pick) - 1]
        if pick in versions:   # full version typed manually
            return pick

        print("Invalid choice, try again.")


# ------------------------- Java search -------------------------

def find_java_path(required_major: int):
    best = None
    for base in JAVA_CANDIDATES:
        if not os.path.isdir(base):
            continue
        for folder in os.listdir(base):
            digits = "".join(ch for ch in folder if ch.isdigit())
            if not digits:
                continue
            major = int(digits[:2]) if len(digits) >= 2 else int(digits)
            exe = os.path.join(base, folder, "bin", "javaw.exe")
            if not os.path.isfile(exe):
                exe = os.path.join(base, folder, "bin", "java.exe")
            if not os.path.isfile(exe):
                continue
            if major == required_major:
                return exe
            if major > required_major:
                best = exe
    return best


# ------------------------- Nickname selection -------------------------

def choose_nickname() -> str:
    nicknames = load_nick_db()

    if not nicknames:
        user_input = input("\nEnter your in-game nickname: ").strip()
        if not user_input:
            print("[Launcher] Empty nickname, using default.")
            return "MichaelPlayer"
        add_nickname(user_input)
        return user_input

    print("\nChoose nickname:")
    print("0 - Enter my own nickname")
    for i, nick in enumerate(nicknames, start=1):
        print(f"{i} - {nick}")
    pick = input("Enter number: ").strip()

    if pick.isdigit() and 0 < int(pick) <= len(nicknames):
        chosen = nicknames[int(pick) - 1]
        print(f"[Launcher] Nickname chosen: {chosen}")
        return chosen

    user_input = input("Enter your in-game nickname: ").strip()
    if not user_input:
        print("[Launcher] Empty nickname, using default.")
        return "MichaelPlayer"
    add_nickname(user_input)
    return user_input


# ------------------------- Main launch -------------------------

print("=========================================")
print("       WELCOME TO MICHAEL LAUNCHER       ")
print(f"              version {LAUNCHER_VERSION}               ")
print("=========================================")

# 1. Nickname
user_nickname = choose_nickname()

# 2. Version selection (all 1.X.X and 26.X releases)
MINECRAFT_VERSION = choose_version()
REQUIRED_JAVA = get_required_java(MINECRAFT_VERSION)

# 3. Game mode selection
print(f"\nChoose version type for {MINECRAFT_VERSION}:")
print("1 - Vanilla (Clean Game)")
print("2 - Fabric (With Mods)")
mode_choice = input("Enter 1 or 2: ").strip()

if mode_choice != "2":
    mode_choice = "1"

# Mods folder — separate for each game version
MODS_DIR = os.path.join(GAME_DIR, "mods", MINECRAFT_VERSION)

print(f"\n[Loading] Hello, {user_nickname}! Running setup for {MINECRAFT_VERSION}...")

if mode_choice == "2":
    os.makedirs(MODS_DIR, exist_ok=True)
    print(f"[Launcher] Mods folder: {MODS_DIR}")
    print("[Launcher] Opening mods folder for you...")
    os.startfile(MODS_DIR)

# Auto Java selection
java_path = find_java_path(REQUIRED_JAVA)
if java_path:
    print(f"[Launcher] Using Java: {java_path}")
else:
    print(f"[Launcher] Warning: Java {REQUIRED_JAVA}+ not found, using system default.")

try:
    print(f"[Minecraft] Syncing base version {MINECRAFT_VERSION} files...")
    minecraft_launcher_lib.install.install_minecraft_version(
        version=MINECRAFT_VERSION,
        minecraft_directory=GAME_DIR,
        callback=callback
    )

    if mode_choice == "2":
        print(f"\n[ModLoader] Installing Fabric Loader for {MINECRAFT_VERSION}...")
        minecraft_launcher_lib.fabric.install_fabric(
            minecraft_version=MINECRAFT_VERSION,
            minecraft_directory=GAME_DIR,
            callback=callback
        )

except Exception as network_error:
    print(f"\n[Network Info] Switched to offline assets mode: {network_error}")

# Final version detection for launch
try:
    if mode_choice == "2":
        installed_versions = minecraft_launcher_lib.utils.get_installed_versions(GAME_DIR)
        target_version = next((v["id"] for v in installed_versions
                               if MINECRAFT_VERSION in v["id"] and "fabric" in v["id"].lower()), None)

        if not target_version:
            print("\n[Launcher] Fabric failed to compile. Falling back to Vanilla.")
            target_version = MINECRAFT_VERSION
        else:
            print(f"[Launcher] Running Stable Fabric Engine: {target_version}")
    else:
        target_version = MINECRAFT_VERSION
        print(f"[Launcher] Running Vanilla {MINECRAFT_VERSION}")

    options = {
        "username": user_nickname,
        "uuid": "00000000-0000-0000-0000-000000000000",
        "token": "0",
        "jvmArguments": ["-Xmx4G", "-Xms2G"]
    }

    if java_path:
        options["executablePath"] = java_path

    launch_command = minecraft_launcher_lib.command.get_minecraft_command(target_version, GAME_DIR, options)

    print(f"\n[Launch] Initializing Minecraft {target_version} as {user_nickname}!")
    print("Enjoy your game!")
    subprocess.run(launch_command)

except Exception as launch_error:
    print(f"\n[Critical Error] Runtime crash: {launch_error}")
    input("\nPress Enter to close this window...")

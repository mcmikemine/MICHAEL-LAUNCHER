# ====================================================================
# MICHAEL LAUNCHER / МАЙКЛ ЛАУНЧЕР — Version 1.3.0.0 (PORTABLE)
# Windows / macOS / Linux. Vanilla / Fabric / Forge / Forge+OptiFine / NeoForge
# License: MIT
# ====================================================================

import os
import sys
import subprocess
import platform

SYSTEM = platform.system()  # 'Windows', 'Darwin', 'Linux'


# ==================== LANGUAGE / ЯЗЫК ====================
print("Choose language / Выберите язык:")
print("1 - English")
print("2 - Русский")
_lang_pick = input("Your choice / Ваш выбор [1-2, Enter = 1]: ").strip()
LANG = "ru" if _lang_pick == "2" else "en"


STRINGS = {
    "en": {
        "launcher_name": "MICHAEL LAUNCHER",

        "setup_header": "MICHAEL LAUNCHER — first-run setup",
        "setup_missing": "[Setup] Missing packages: {pkgs}",
        "setup_installing": "[Setup] Installing automatically, please wait...",
        "setup_running": "[Setup] Running: {cmd}",
        "setup_no_python": "[Setup] ERROR: no Python interpreter found to run pip.",
        "setup_manual": "[Setup] Install manually: {cmd}",
        "setup_pip_failed": "[Setup] pip exit code: {code}",
        "setup_still_missing": "[Setup] ERROR: still missing after install: {err}",
        "setup_error": "[Setup] ERROR: {err}",
        "setup_done": "[Setup] Done! Continuing...",
        "press_enter": "Press Enter to close...",

        "version_line": "      version {v}       ",
        "system_line": "      system: {s}       ",
        "portable_folder": "[Portable] Data folder: {path}",

        "source_title": "\n=== Where to download Minecraft files from? ===",
        "source_1": "1 - Official Mojang (may be blocked)",
        "source_2": "2 - BMCLAPI (mirror #1, recommended)",
        "source_3": "3 - FastMinecraftMirror (mirror #2)",
        "source_4": "4 - MCLib (mirror #3)",
        "source_5": "5 - All mirrors in order (safest)",
        "source_prompt": "Your choice [1-5, Enter = 5]: ",
        "source_official": "[Source] Official Mojang (no mirrors)",
        "source_mirrors": "[Source] Mirrors: {names}",
        "mirror_ok": "[Mirror] {name}: {url} -> {mirrored}",
        "mirror_status": "[Mirror] {name} returned {code}, trying next...",
        "mirror_no_response": "[Mirror] {name} did not respond ({err}), trying next...",
        "mirror_failed": "[Mirror] All mirrors failed, downloading directly: {url}",

        "nick_enter": "\nEnter your in-game nickname: ",
        "nick_empty": "[Launcher] Empty nickname, using default.",
        "nick_choose": "\nChoose nickname:",
        "nick_own": "0 - Enter my own nickname",
        "nick_prompt": "Enter number: ",
        "nick_chosen": "[Launcher] Nickname chosen: {nick}",

        "ver_loading": "\nLoading version list...",
        "ver_found": "[Launcher] Found {n} releases",
        "ver_page": "\n--- Page {p} of {total} ---",
        "ver_nav": "'n' next page / 'p' previous page",
        "ver_or_type": "\nOr type a full version (e.g. 1.20.1)",
        "ver_prompt": "Your choice: ",
        "ver_invalid": "Invalid choice, try again.",
        "ver_cache": "[Launcher] Using cached version list (offline mode).",
        "ver_no_cache": "[Launcher] No cache. Using built-in version list.",

        "java_portable": "[Launcher] Using portable Java: {path}",
        "java_using": "[Launcher] Using Java: {path}",
        "java_sys": "[Launcher] Fallback to system Java: {path}",
        "java_warn": "[Launcher] Warning: Java {v}+ not found, using system default.",

        "mode_title": "\nChoose version type for {v}:",
        "mode_1": "1 - Vanilla (Clean Game)",
        "mode_2": "2 - Fabric (With Mods)",
        "mode_3": "3 - Forge (With Mods) — VPN required",
        "mode_4": "4 - Forge + OptiFine (With Mods + Shaders) — VPN required",
        "mode_5": "5 - NeoForge (With Mods) — VPN required",
        "mode_prompt": "Enter 1, 2, 3, 4 or 5: ",

        "loading_hello": "\n[Loading] Hello, {nick}! Running setup for {v}...",
        "mods_folder": "[Launcher] Mods folder: {path}",
        "mods_note": "[Launcher] Note: this folder is shared between all modded versions.",
        "mods_opening": "[Launcher] Opening mods folder for you...",
        "mods_open_fail": "[Launcher] Could not open folder automatically: {err}",

        "vpn_header": "{loader} — SYSTEM VPN REQUIRED",
        "vpn_downloads": "{loader} downloads files directly from:",
        "vpn_blocked": "These servers are often blocked or slow in Russia.",
        "vpn_browser_no": "A BROWSER VPN (extension in Chrome/Opera/Firefox) will NOT help!",
        "vpn_only_system": "Only a SYSTEM-WIDE VPN or proxy that redirects ALL PC traffic works:",
        "vpn_opt1": "   - WireGuard / OpenVPN / AmneziaVPN / ProtonVPN (desktop app)",
        "vpn_opt2": "   - Or a system proxy set in OS Settings -> Network",
        "vpn_tip1": "Turn on your VPN, make sure it is active for the whole system,",
        "vpn_tip2": "then continue. Installation may take several minutes.",
        "vpn_prompt": "Continue with VPN ON? [Y/n]: ",
        "vpn_cancel": "[Launcher] Cancelled by user. Falling back to Vanilla.",

        "mc_sync": "[Minecraft] Syncing base version {v} files...",
        "fabric_setup": "\n[ModLoader] Installing Fabric Loader for {v}...",
        "fabric_using": "[Launcher] Using Fabric: {v}",
        "fabric_failed": "[Launcher] Fabric install failed. Falling back to Vanilla.",
        "fabric_error": "[Launcher] Fabric error: {err}. Falling back to Vanilla.",

        "forge_setup": "\n[ModLoader] Setting up Forge for {v}...",
        "forge_none": "[Launcher] No Forge version found for {v}. Falling back to Vanilla.",
        "forge_recommended": "[ModLoader] Recommended Forge: {v}",
        "forge_using": "[Launcher] Using Forge: {v}",
        "forge_error": "[Launcher] Forge error: {err}. Falling back to Vanilla.",

        "fo_setup": "\n[ModLoader] Setting up Forge + OptiFine for {v}...",
        "fo_none": "[Launcher] No OptiFine version found for {v}.",
        "fo_try_forge": "[Launcher] Trying Forge only...",
        "fo_found": "[ModLoader] Found OptiFine: {v}",
        "fo_installing": "[ModLoader] Installing OptiFine...",
        "fo_no_forge": "[Launcher] No Forge version found. Using OptiFine standalone.",
        "fo_using_of": "[Launcher] Using OptiFine: {v}",
        "fo_combined": "[ModLoader] Installing Forge: {v} (combined with OptiFine)",
        "fo_using_both": "[Launcher] Using Forge+OptiFine: {v}",
        "fo_error": "[Launcher] Forge+OptiFine error: {err}. Falling back to Vanilla.",

        "neoforge_setup": "\n[ModLoader] Setting up NeoForge for {v}...",
        "neoforge_unavailable": "[Launcher] NeoForge module is not available in your minecraft-launcher-lib.",
        "neoforge_update": "[Launcher] Update it with: pip install --upgrade minecraft-launcher-lib",
        "neoforge_none": "[Launcher] No NeoForge version found for {v}. Falling back to Vanilla.",
        "neoforge_recommended": "[ModLoader] Recommended NeoForge: {v}",
        "neoforge_using": "[Launcher] Using NeoForge: {v}",
        "neoforge_error": "[Launcher] NeoForge error: {err}. Falling back to Vanilla.",

        "running_vanilla": "[Launcher] Running Vanilla {v}",
        "net_error": "\n[Network Info] Error during setup: {err}",
        "launch_init": "\n[Launch] Initializing Minecraft {v} as {nick}!",
        "launch_enjoy": "Enjoy your game!",
        "crit_error": "\n[Critical Error] Runtime crash: {err}",

        "status_prefix": "[Status] {s}",
        "downloading": "\rDownloading game assets: [{cur}/{max}] {pct}%",
    },
    "ru": {
        "launcher_name": "МАЙКЛ ЛАУНЧЕР",

        "setup_header": "МАЙКЛ ЛАУНЧЕР — первая настройка",
        "setup_missing": "[Установка] Отсутствуют пакеты: {pkgs}",
        "setup_installing": "[Установка] Устанавливаю автоматически, подождите...",
        "setup_running": "[Установка] Запуск: {cmd}",
        "setup_no_python": "[Установка] ОШИБКА: Python не найден для запуска pip.",
        "setup_manual": "[Установка] Установите вручную: {cmd}",
        "setup_pip_failed": "[Установка] pip завершился с кодом: {code}",
        "setup_still_missing": "[Установка] ОШИБКА: всё ещё отсутствует: {err}",
        "setup_error": "[Установка] ОШИБКА: {err}",
        "setup_done": "[Установка] Готово! Продолжаем...",
        "press_enter": "Нажмите Enter, чтобы закрыть...",

        "version_line": "      версия {v}       ",
        "system_line": "      система: {s}       ",
        "portable_folder": "[Портативно] Папка данных: {path}",

        "source_title": "\n=== Откуда качать файлы Minecraft? ===",
        "source_1": "1 - Официальный Mojang (может быть заблокирован)",
        "source_2": "2 - BMCLAPI (зеркало #1, рекомендуется)",
        "source_3": "3 - FastMinecraftMirror (зеркало #2)",
        "source_4": "4 - MCLib (зеркало #3)",
        "source_5": "5 - Все зеркала по порядку (безопаснее всего)",
        "source_prompt": "Твой выбор [1-5, Enter = 5]: ",
        "source_official": "[Источник] Официальный Mojang (без зеркал)",
        "source_mirrors": "[Источник] Зеркала: {names}",
        "mirror_ok": "[Зеркало] {name}: {url} -> {mirrored}",
        "mirror_status": "[Зеркало] {name} вернул {code}, пробую следующее...",
        "mirror_no_response": "[Зеркало] {name} не ответил ({err}), пробую следующее...",
        "mirror_failed": "[Зеркало] Все зеркала не сработали, качаю напрямую: {url}",

        "nick_enter": "\nВведите ваш игровой никнейм: ",
        "nick_empty": "[Лаунчер] Пустой никнейм, использую стандартный.",
        "nick_choose": "\nВыбор никнейма:",
        "nick_own": "0 - Ввести свой никнейм",
        "nick_prompt": "Введите номер: ",
        "nick_chosen": "[Лаунчер] Никнейм выбран: {nick}",

        "ver_loading": "\nЗагрузка списка версий...",
        "ver_found": "[Лаунчер] Найдено {n} релизов",
        "ver_page": "\n--- Страница {p} из {total} ---",
        "ver_nav": "'n' следующая страница / 'p' предыдущая",
        "ver_or_type": "\nИли введите полную версию (например, 1.20.1)",
        "ver_prompt": "Ваш выбор: ",
        "ver_invalid": "Неверный выбор, попробуйте снова.",
        "ver_cache": "[Лаунчер] Использую кэш версий (офлайн-режим).",
        "ver_no_cache": "[Лаунчер] Нет кэша. Использую встроенный список версий.",

        "java_portable": "[Лаунчер] Использую портативную Java: {path}",
        "java_using": "[Лаунчер] Использую Java: {path}",
        "java_sys": "[Лаунчер] Использую системную Java: {path}",
        "java_warn": "[Лаунчер] Внимание: Java {v}+ не найдена, использую системную по умолчанию.",

        "mode_title": "\nВыберите тип версии для {v}:",
        "mode_1": "1 - Vanilla (чистая игра)",
        "mode_2": "2 - Fabric (с модами)",
        "mode_3": "3 - Forge (с модами) — нужен VPN",
        "mode_4": "4 - Forge + OptiFine (с модами и шейдерами) — нужен VPN",
        "mode_5": "5 - NeoForge (с модами) — нужен VPN",
        "mode_prompt": "Введите 1, 2, 3, 4 или 5: ",

        "loading_hello": "\n[Загрузка] Привет, {nick}! Настраиваю {v}...",
        "mods_folder": "[Лаунчер] Папка модов: {path}",
        "mods_note": "[Лаунчер] Примечание: эта папка общая для всех модифицированных версий.",
        "mods_opening": "[Лаунчер] Открываю папку модов...",
        "mods_open_fail": "[Лаунчер] Не удалось открыть папку автоматически: {err}",

        "vpn_header": "{loader} — НУЖЕН СИСТЕМНЫЙ VPN",
        "vpn_downloads": "{loader} скачивает файлы напрямую с:",
        "vpn_blocked": "Эти серверы часто заблокированы или медленные в России.",
        "vpn_browser_no": "БРАУЗЕРНЫЙ VPN (расширение в Chrome/Opera/Firefox) НЕ поможет!",
        "vpn_only_system": "Поможет только СИСТЕМНЫЙ VPN или прокси, перенаправляющий ВЕСЬ трафик ПК:",
        "vpn_opt1": "   - WireGuard / OpenVPN / AmneziaVPN / ProtonVPN (десктоп-приложение)",
        "vpn_opt2": "   - Или системный прокси в настройках ОС -> Сеть",
        "vpn_tip1": "Включите VPN, убедитесь, что он активен для всей системы,",
        "vpn_tip2": "затем продолжите. Установка может занять несколько минут.",
        "vpn_prompt": "Продолжить с включённым VPN? [Y/n]: ",
        "vpn_cancel": "[Лаунчер] Отменено пользователем. Переключаюсь на Vanilla.",

        "mc_sync": "[Minecraft] Синхронизирую файлы базовой версии {v}...",
        "fabric_setup": "\n[Мод-лоадер] Устанавливаю Fabric Loader для {v}...",
        "fabric_using": "[Лаунчер] Использую Fabric: {v}",
        "fabric_failed": "[Лаунчер] Установка Fabric не удалась. Переключаюсь на Vanilla.",
        "fabric_error": "[Лаунчер] Ошибка Fabric: {err}. Переключаюсь на Vanilla.",

        "forge_setup": "\n[Мод-лоадер] Настраиваю Forge для {v}...",
        "forge_none": "[Лаунчер] Forge для {v} не найден. Переключаюсь на Vanilla.",
        "forge_recommended": "[Мод-лоадер] Рекомендуемый Forge: {v}",
        "forge_using": "[Лаунчер] Использую Forge: {v}",
        "forge_error": "[Лаунчер] Ошибка Forge: {err}. Переключаюсь на Vanilla.",

        "fo_setup": "\n[Мод-лоадер] Настраиваю Forge + OptiFine для {v}...",
        "fo_none": "[Лаунчер] OptiFine для {v} не найден.",
        "fo_try_forge": "[Лаунчер] Пробую только Forge...",
        "fo_found": "[Мод-лоадер] Найден OptiFine: {v}",
        "fo_installing": "[Мод-лоадер] Устанавливаю OptiFine...",
        "fo_no_forge": "[Лаунчер] Forge не найден. Использую OptiFine отдельно.",
        "fo_using_of": "[Лаунчер] Использую OptiFine: {v}",
        "fo_combined": "[Мод-лоадер] Устанавливаю Forge: {v} (вместе с OptiFine)",
        "fo_using_both": "[Лаунчер] Использую Forge+OptiFine: {v}",
        "fo_error": "[Лаунчер] Ошибка Forge+OptiFine: {err}. Переключаюсь на Vanilla.",

        "neoforge_setup": "\n[Мод-лоадер] Настраиваю NeoForge для {v}...",
        "neoforge_unavailable": "[Лаунчер] Модуль NeoForge недоступен в вашей minecraft-launcher-lib.",
        "neoforge_update": "[Лаунчер] Обновите её: pip install --upgrade minecraft-launcher-lib",
        "neoforge_none": "[Лаунчер] NeoForge для {v} не найден. Переключаюсь на Vanilla.",
        "neoforge_recommended": "[Мод-лоадер] Рекомендуемый NeoForge: {v}",
        "neoforge_using": "[Лаунчер] Использую NeoForge: {v}",
        "neoforge_error": "[Лаунчер] Ошибка NeoForge: {err}. Переключаюсь на Vanilla.",

        "running_vanilla": "[Лаунчер] Запускаю Vanilla {v}",
        "net_error": "\n[Сеть] Ошибка при настройке: {err}",
        "launch_init": "\n[Запуск] Запускаю Minecraft {v} от имени {nick}!",
        "launch_enjoy": "Приятной игры!",
        "crit_error": "\n[Критическая ошибка] Сбой: {err}",

        "status_prefix": "[Статус] {s}",
        "downloading": "\rСкачивание ресурсов: [{cur}/{max}] {pct}%",
    },
}


def t(key: str, **kwargs) -> str:
    s = STRINGS[LANG].get(key, STRINGS["en"].get(key, key))
    return s.format(**kwargs) if kwargs else s


# ------------------------- Dependency bootstrap -------------------------
def ensure_dependencies():
    missing = []
    try:
        import requests  # noqa: F401
    except ImportError:
        missing.append("requests")
    try:
        import minecraft_launcher_lib  # noqa: F401
    except ImportError:
        missing.append("minecraft-launcher-lib")

    if not missing:
        return

    print("=" * 55)
    print("  " + t("setup_header"))
    print("=" * 55)
    print(t("setup_missing", pkgs=", ".join(missing)))
    print(t("setup_installing"))

    if getattr(sys, "frozen", False):
        import shutil
        python_exe = (
            shutil.which("python")
            or shutil.which("python3")
            or shutil.which("py")
        )
        if not python_exe:
            print(t("setup_no_python"))
            print(t("setup_manual", cmd=f"pip install {' '.join(missing)}"))
            input(t("press_enter"))
            sys.exit(1)
        pip_base = [python_exe, "-m", "pip"]
    else:
        pip_base = [sys.executable, "-m", "pip"]

    pip_cmd = pip_base + ["install", "--upgrade"] + missing
    print(t("setup_running", cmd=" ".join(pip_cmd)))

    try:
        result = subprocess.run(pip_cmd)
    except Exception as e:
        print(t("setup_error", err=e))
        print(t("setup_manual", cmd=f"pip install {' '.join(missing)}"))
        input(t("press_enter"))
        sys.exit(1)

    if result.returncode != 0:
        print(t("setup_pip_failed", code=result.returncode))
        print(t("setup_manual", cmd=f"pip install {' '.join(missing)}"))
        input(t("press_enter"))
        sys.exit(1)

    try:
        import requests  # noqa: F401
        import minecraft_launcher_lib  # noqa: F401
    except ImportError as e:
        print(t("setup_still_missing", err=e))
        input(t("press_enter"))
        sys.exit(1)

    print(t("setup_done"))


ensure_dependencies()

import json
import urllib.request
import requests
from urllib.parse import urlparse
import minecraft_launcher_lib

# NeoForge module may be missing in older library versions
try:
    from minecraft_launcher_lib import neoforge as neoforge_lib
except ImportError:
    neoforge_lib = None


LAUNCHER_VERSION = "1.3.0.0"
CHANGELOG = {
    "1.3.0.0": [
        "Bilingual UI (English / Русский)",
        "Cross-platform: Windows / macOS / Linux",
        "macOS: JDK discovery, folder opening via 'open', portable JRE support",
        "Added NeoForge support (mode 5) — VPN required",
        "Forge + OptiFine support (mode 4)",
        "Auto dependency install on first run",
        "PORTABLE: all data in .michael_launcher next to the launcher",
    ],
}

# ------------------------- Portable paths -------------------------

def get_launcher_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


LAUNCHER_DIR = get_launcher_dir()
BASE_DIR = os.path.join(LAUNCHER_DIR, ".michael_launcher")
GAME_DIR = os.path.join(BASE_DIR, "minecraft")
NICK_DB = os.path.join(BASE_DIR, "nicknames.json")
VERSIONS_CACHE = os.path.join(BASE_DIR, "versions_cache.json")
PORTABLE_JRE = os.path.join(BASE_DIR, "jre")

MOJANG_MANIFEST = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

FALLBACK_VERSIONS = [
    "26.3", "26.2", "26.1.2", "26.1.1", "26.1",
    "1.21.11", "1.21.10", "1.21.9", "1.21.8", "1.21.7", "1.21.6",
    "1.21.5", "1.21.4", "1.21.3", "1.21.2", "1.21.1", "1.21",
    "1.20.6", "1.20.5", "1.20.4", "1.20.3", "1.20.2", "1.20.1", "1.20",
    "1.19.4", "1.19.3", "1.19.2", "1.19.1", "1.19",
    "1.18.2", "1.17.1", "1.16.5", "1.16.4", "1.16.1", "1.15.2", "1.14.4",
    "1.12.2", "1.8.9", "1.7.10",
]

if SYSTEM == "Windows":
    JAVA_CANDIDATES = [
        r"C:\Program Files\Java",
        r"C:\Program Files\Eclipse Adoptium",
        r"C:\Program Files (x86)\Java",
        r"C:\Program Files\Microsoft\jdk-21",
        r"C:\Program Files\Microsoft\jdk-17",
        r"C:\Program Files\Microsoft\jdk-11",
    ]
else:
    JAVA_CANDIDATES = [
        "/Library/Java/JavaVirtualMachines",
        "/System/Library/Java/JavaVirtualMachines",
        os.path.expanduser("~/Library/Java/JavaVirtualMachines"),
        "/opt/homebrew/opt",
        "/usr/local/opt",
        "/opt/homebrew/Cellar",
        "/usr/local/Cellar",
        "/usr/lib/jvm",
    ]

DEFAULT_NICKNAMES = []

VERSION_HISTORY = {
    "1.0":  ("Official release: The End and the Ender Dragon", "November 18, 2011"),
    "1.8":  ("Bountiful Update: oceans, prismarine, armor stands", "September 2014"),
    "1.12": ("World of Color Update: concrete, recipe book, parrots", "June 2017"),
    "1.13": ("Update Aquatic: dolphins, coral, tridents", "July 2018"),
    "1.16": ("Nether Update: netherite, new Nether biomes", "June 2020"),
    "1.17": ("Caves & Cliffs Part 1: new ores", "2021"),
    "1.18": ("Caves & Cliffs Part 2: new cave and mountain generation", "2021"),
    "1.19": ("The Wild Update: Deep Dark, Warden, mangrove swamps", "June 2022"),
    "1.20": ("Trails & Tales: archaeology, cherry biome, sniffers", "June 2023"),
    "1.21": ("Tricky Trials: trial chambers, breeze, copper blocks", "June 2024"),
    "26":   ("2026 updates: new version numbering system", "2026"),
}


# ==================== MIRRORS ====================
MIRRORS = [
    {
        "name": "BMCLAPI",
        "replacements": {
            "launchermeta.mojang.com": "bmclapi2.bangbang93.com",
            "piston-meta.mojang.com": "bmclapi2.bangbang93.com",
            "launcher.mojang.com": "bmclapi2.bangbang93.com",
            "resources.download.minecraft.net": "bmclapi2.bangbang93.com",
            "libraries.minecraft.net": "bmclapi2.bangbang93.com",
        },
        "special": {
            "resources.download.minecraft.net": lambda path: f"/assets/{path.split('/')[-1]}"
            if path.count('/') >= 2 else None,
            "libraries.minecraft.net": lambda path: f"/maven{path}",
        },
    },
    {
        "name": "FastMinecraftMirror",
        "replacements": {
            "launchermeta.mojang.com": "fastmcmirror.org",
            "piston-meta.mojang.com": "fastmcmirror.org",
            "launcher.mojang.com": "fastmcmirror.org",
            "resources.download.minecraft.net": "fastmcmirror.org",
            "libraries.minecraft.net": "fastmcmirror.org",
        },
        "special": {}
    },
    {
        "name": "MCLib",
        "replacements": {
            "launchermeta.mojang.com": "mclib.org",
            "piston-meta.mojang.com": "mclib.org",
            "launcher.mojang.com": "mclib.org",
            "resources.download.minecraft.net": "mclib.org",
            "libraries.minecraft.net": "mclib.org",
        },
        "special": {}
    },
]


def choose_download_source():
    print(t("source_title"))
    print(t("source_1"))
    print(t("source_2"))
    print(t("source_3"))
    print(t("source_4"))
    print(t("source_5"))
    choice = input(t("source_prompt")).strip()

    if choice == "1":
        return []
    if choice == "2":
        return [MIRRORS[0], MIRRORS[1], MIRRORS[2]]
    if choice == "3":
        return [MIRRORS[1], MIRRORS[0], MIRRORS[2]]
    if choice == "4":
        return [MIRRORS[2], MIRRORS[0], MIRRORS[1]]
    return list(MIRRORS)


def apply_mirror_patch(mirrors_to_use):
    if not mirrors_to_use:
        print(t("source_official"))
        return

    mojang_hosts = set()
    for m in mirrors_to_use:
        mojang_hosts.update(m["replacements"].keys())

    _original_requests_get = requests.get

    def patched_get(url, *args, **kwargs):
        parsed = urlparse(url)
        if parsed.netloc in mojang_hosts:
            for mirror in mirrors_to_use:
                if parsed.netloc not in mirror["replacements"]:
                    continue
                new_host = mirror["replacements"][parsed.netloc]
                new_path = parsed.path
                if parsed.query:
                    new_path += "?" + parsed.query
                if parsed.netloc in mirror.get("special", {}):
                    special_path = mirror["special"][parsed.netloc](parsed.path)
                    if special_path is not None:
                        new_path = special_path
                mirrored_url = f"https://{new_host}{new_path}"
                try:
                    resp = _original_requests_get(mirrored_url, *args, **kwargs)
                    if resp.status_code < 400:
                        print(t("mirror_ok", name=mirror['name'], url=url, mirrored=mirrored_url))
                        return resp
                    print(t("mirror_status", name=mirror['name'], code=resp.status_code))
                except requests.RequestException as e:
                    print(t("mirror_no_response", name=mirror['name'], err=e.__class__.__name__))
            print(t("mirror_failed", url=url))
        return _original_requests_get(url, *args, **kwargs)

    requests.get = patched_get
    names = ", ".join(m["name"] for m in mirrors_to_use)
    print(t("source_mirrors", names=names))
# =================================================


# ------------------------- Version info -------------------------

def get_version_info(version: str) -> str:
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


# ------------------------- Nickname DB -------------------------

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


# ------------------------- Progress -------------------------

max_val = 0

def set_status(status: str):
    print(t("status_prefix", s=status))

def set_maximum(value: int):
    global max_val
    max_val = value

def set_progress(value: int):
    global max_val
    if max_val > 0:
        percentage = int((value / max_val) * 100)
        print(t("downloading", cur=value, max=max_val, pct=percentage), end="", flush=True)

callback = {
    "setStatus": set_status,
    "setMaximum": set_maximum,
    "setProgress": set_progress
}


# ------------------------- Version list -------------------------

def fetch_versions_online() -> list:
    utils = minecraft_launcher_lib.utils

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

    try:
        resp = requests.get(MOJANG_MANIFEST, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        releases = [v["id"] for v in data.get("versions", [])
                    if v.get("type") == "release" and v["id"][:1].isdigit()]
        if releases:
            return releases
    except Exception:
        pass
    return []


def get_release_versions() -> list:
    releases = fetch_versions_online()
    if releases:
        save_versions_cache(releases)
        return releases

    cached = load_versions_cache()
    if cached:
        print(t("ver_cache"))
        return cached

    print(t("ver_no_cache"))
    return list(FALLBACK_VERSIONS)


def get_required_java(version: str) -> int:
    if not version.startswith("1."):
        return 21
    try:
        parts = version.split(".")
        minor = int(parts[1]) if len(parts) > 1 else 0
        patch = int(parts[2]) if len(parts) > 2 else 0
    except ValueError:
        return 8
    if minor > 20 or (minor == 20 and patch >= 5):
        return 21
    if minor >= 18:
        return 17
    if minor == 17:
        return 16
    return 8


def choose_version() -> str:
    print(t("ver_loading"))
    versions = get_release_versions()
    print(t("ver_found", n=len(versions)))

    page = 0
    per_page = 15
    while True:
        start = page * per_page
        chunk = versions[start:start + per_page]
        if not chunk:
            page = 0
            continue

        print(t("ver_page", p=page + 1, total=(len(versions) - 1) // per_page + 1))
        for i, ver in enumerate(chunk, start=1):
            java_req = get_required_java(ver)
            info = get_version_info(ver)
            suffix = f" — {info}" if info else ""
            print(f"{i} - {ver} (Java {java_req}+){suffix}")
        print(t("ver_nav"))
        print(t("ver_or_type"))
        pick = input(t("ver_prompt")).strip().lower()

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
        if pick in versions:
            return pick
        print(t("ver_invalid"))


# ------------------------- Java search (cross-platform) -------------------------

def find_portable_java():
    for exe_name in ("java", "javaw.exe", "java.exe"):
        exe = os.path.join(PORTABLE_JRE, "bin", exe_name)
        if os.path.isfile(exe):
            return exe
    return None


def find_java_path(required_major: int):
    portable = find_portable_java()
    if portable:
        print(t("java_portable", path=portable))
        return portable

    best = None
    for base in JAVA_CANDIDATES:
        if not os.path.isdir(base):
            continue
        try:
            entries = os.listdir(base)
        except PermissionError:
            continue
        for folder in entries:
            full = os.path.join(base, folder)
            if not os.path.isdir(full):
                continue
            candidates = [
                os.path.join(full, "bin", "java"),
                os.path.join(full, "Contents", "Home", "bin", "java"),
                os.path.join(full, "bin", "javaw.exe"),
                os.path.join(full, "bin", "java.exe"),
            ]
            for exe in candidates:
                if not os.path.isfile(exe):
                    continue
                digits = "".join(ch for ch in folder if ch.isdigit())
                if not digits:
                    continue
                major = int(digits[:2]) if len(digits) >= 2 else int(digits)
                if major == required_major:
                    return exe
                if major > required_major:
                    best = exe

    import shutil
    sys_java = shutil.which("java")
    if sys_java:
        print(t("java_sys", path=sys_java))
        return sys_java
    return best


# ------------------------- Open folder (cross-platform) -------------------------

def open_folder(path: str):
    try:
        if SYSTEM == "Windows":
            os.startfile(path)  # type: ignore[attr-defined]
        elif SYSTEM == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception as e:
        print(t("mods_open_fail", err=e))


# ------------------------- Nickname selection -------------------------

def choose_nickname() -> str:
    nicknames = load_nick_db()

    if not nicknames:
        user_input = input(t("nick_enter")).strip()
        if not user_input:
            print(t("nick_empty"))
            return "MichaelPlayer"
        add_nickname(user_input)
        return user_input

    print(t("nick_choose"))
    print(t("nick_own"))
    for i, nick in enumerate(nicknames, start=1):
        print(f"{i} - {nick}")
    pick = input(t("nick_prompt")).strip()

    if pick.isdigit() and 0 < int(pick) <= len(nicknames):
        chosen = nicknames[int(pick) - 1]
        print(t("nick_chosen", nick=chosen))
        return chosen

    user_input = input(t("nick_enter")).strip()
    if not user_input:
        print(t("nick_empty"))
        return "MichaelPlayer"
    add_nickname(user_input)
    return user_input


# ------------------------- VPN warning -------------------------

def print_vpn_warning(loader_name: str, sources):
    print()
    print("!" * 62)
    print("  " + t("vpn_header", loader=loader_name))
    print("!" * 62)
    print("  " + t("vpn_downloads", loader=loader_name))
    for src in sources:
        print(f"     - {src}")
    print("  " + t("vpn_blocked"))
    print()
    print("  " + t("vpn_browser_no"))
    print("  " + t("vpn_only_system"))
    print(t("vpn_opt1"))
    print(t("vpn_opt2"))
    print()
    print("  " + t("vpn_tip1"))
    print("  " + t("vpn_tip2"))
    print("!" * 62)
    print()

    answer = input(t("vpn_prompt")).strip().lower()
    if answer == "n":
        print(t("vpn_cancel"))
        return False
    return True


# ------------------------- Main -------------------------

print("=" * 45)
print("  " + t("launcher_name"))
print(t("version_line", v=LAUNCHER_VERSION))
print(t("system_line", s=SYSTEM))
print("=" * 45)
print(t("portable_folder", path=BASE_DIR))

os.makedirs(BASE_DIR, exist_ok=True)

chosen_mirrors = choose_download_source()
apply_mirror_patch(chosen_mirrors)

user_nickname = choose_nickname()
MINECRAFT_VERSION = choose_version()
REQUIRED_JAVA = get_required_java(MINECRAFT_VERSION)

print(t("mode_title", v=MINECRAFT_VERSION))
print(t("mode_1"))
print(t("mode_2"))
print(t("mode_3"))
print(t("mode_4"))
print(t("mode_5"))
mode_choice = input(t("mode_prompt")).strip()

if mode_choice not in ("2", "3", "4", "5"):
    mode_choice = "1"

if mode_choice == "3":
    if not print_vpn_warning("Forge", ["maven.minecraftforge.net"]):
        mode_choice = "1"
elif mode_choice == "4":
    if not print_vpn_warning("Forge + OptiFine",
                             ["maven.minecraftforge.net", "optifine.net"]):
        mode_choice = "1"
elif mode_choice == "5":
    if not print_vpn_warning("NeoForge", ["maven.neoforged.net"]):
        mode_choice = "1"

MODS_DIR = os.path.join(GAME_DIR, "mods")

print(t("loading_hello", nick=user_nickname, v=MINECRAFT_VERSION))

if mode_choice in ("2", "3", "4", "5"):
    os.makedirs(MODS_DIR, exist_ok=True)
    print(t("mods_folder", path=MODS_DIR))
    print(t("mods_note"))
    print(t("mods_opening"))
    open_folder(MODS_DIR)

java_path = find_java_path(REQUIRED_JAVA)
if java_path:
    print(t("java_using", path=java_path))
else:
    print(t("java_warn", v=REQUIRED_JAVA))

target_version = MINECRAFT_VERSION

try:
    print(t("mc_sync", v=MINECRAFT_VERSION))
    minecraft_launcher_lib.install.install_minecraft_version(
        version=MINECRAFT_VERSION,
        minecraft_directory=GAME_DIR,
        callback=callback
    )

    # ---------- Fabric ----------
    if mode_choice == "2":
        print(t("fabric_setup", v=MINECRAFT_VERSION))
        try:
            minecraft_launcher_lib.fabric.install_fabric(
                minecraft_version=MINECRAFT_VERSION,
                minecraft_directory=GAME_DIR,
                callback=callback
            )
            installed = minecraft_launcher_lib.utils.get_installed_versions(GAME_DIR)
            fabric_v = next((v["id"] for v in installed
                             if MINECRAFT_VERSION in v["id"] and "fabric" in v["id"].lower()), None)
            if fabric_v:
                target_version = fabric_v
                print(t("fabric_using", v=fabric_v))
            else:
                print(t("fabric_failed"))
        except Exception as e:
            print(t("fabric_error", err=e))

    # ---------- Forge ----------
    elif mode_choice == "3":
        print(t("forge_setup", v=MINECRAFT_VERSION))
        try:
            forge_ver = minecraft_launcher_lib.forge.find_forge_version(MINECRAFT_VERSION)
            if not forge_ver:
                print(t("forge_none", v=MINECRAFT_VERSION))
            else:
                print(t("forge_recommended", v=forge_ver))
                installed_name = minecraft_launcher_lib.forge.install_forge(
                    forge_ver, GAME_DIR, callback=callback, java=java_path
                )
                target_version = installed_name
                print(t("forge_using", v=installed_name))
        except Exception as e:
            print(t("forge_error", err=e))

    # ---------- Forge + OptiFine ----------
    elif mode_choice == "4":
        print(t("fo_setup", v=MINECRAFT_VERSION))
        try:
            optifine_ver = minecraft_launcher_lib.forge.find_optifine_version(MINECRAFT_VERSION)
            if not optifine_ver:
                print(t("fo_none", v=MINECRAFT_VERSION))
                print(t("fo_try_forge"))
                forge_ver = minecraft_launcher_lib.forge.find_forge_version(MINECRAFT_VERSION)
                if forge_ver:
                    installed_name = minecraft_launcher_lib.forge.install_forge(
                        forge_ver, GAME_DIR, callback=callback, java=java_path
                    )
                    target_version = installed_name
                    print(t("forge_using", v=installed_name))
                else:
                    print(t("forge_none", v=MINECRAFT_VERSION))
            else:
                print(t("fo_found", v=optifine_ver))
                print(t("fo_installing"))
                try:
                    minecraft_launcher_lib.forge.install_optifine(
                        optifine_ver, GAME_DIR, callback=callback, java=java_path
                    )
                except TypeError:
                    minecraft_launcher_lib.forge.install_optifine(
                        optifine_ver, GAME_DIR, callback=callback
                    )

                forge_ver = minecraft_launcher_lib.forge.find_forge_version(MINECRAFT_VERSION)
                if not forge_ver:
                    print(t("fo_no_forge"))
                    installed = minecraft_launcher_lib.utils.get_installed_versions(GAME_DIR)
                    optifine_v = next((v["id"] for v in installed
                                       if MINECRAFT_VERSION in v["id"]
                                       and "optifine" in v["id"].lower()), None)
                    if optifine_v:
                        target_version = optifine_v
                        print(t("fo_using_of", v=optifine_v))
                else:
                    print(t("fo_combined", v=forge_ver))
                    installed_name = minecraft_launcher_lib.forge.install_forge(
                        forge_ver, GAME_DIR, callback=callback, java=java_path
                    )
                    target_version = installed_name
                    print(t("fo_using_both", v=installed_name))
        except Exception as e:
            print(t("fo_error", err=e))

    # ---------- NeoForge ----------
    elif mode_choice == "5":
        print(t("neoforge_setup", v=MINECRAFT_VERSION))
        if neoforge_lib is None:
            print(t("neoforge_unavailable"))
            print(t("neoforge_update"))
            print(t("forge_none", v=MINECRAFT_VERSION))
        else:
            try:
                neoforge_ver = neoforge_lib.find_neoforge_version(MINECRAFT_VERSION)
                if not neoforge_ver:
                    print(t("neoforge_none", v=MINECRAFT_VERSION))
                else:
                    print(t("neoforge_recommended", v=neoforge_ver))
                    try:
                        installed_name = neoforge_lib.install_neoforge(
                            neoforge_ver, GAME_DIR, callback=callback, java=java_path
                        )
                    except TypeError:
                        installed_name = neoforge_lib.install_neoforge(
                            neoforge_ver, GAME_DIR, callback=callback
                        )
                    target_version = installed_name
                    print(t("neoforge_using", v=installed_name))
            except Exception as e:
                print(t("neoforge_error", err=e))

    else:
        print(t("running_vanilla", v=MINECRAFT_VERSION))

except Exception as network_error:
    print(t("net_error", err=network_error))
    target_version = MINECRAFT_VERSION

try:
    options = {
        "username": user_nickname,
        "uuid": "00000000-0000-0000-0000-000000000000",
        "token": "0",
        "jvmArguments": ["-Xmx4G", "-Xms2G"]
    }
    if java_path:
        options["executablePath"] = java_path

    launch_command = minecraft_launcher_lib.command.get_minecraft_command(
        target_version, GAME_DIR, options
    )

    print(t("launch_init", v=target_version, nick=user_nickname))
    print(t("launch_enjoy"))
    subprocess.run(launch_command)

except Exception as launch_error:
    print(t("crit_error", err=launch_error))
    input(t("press_enter"))

import sys
import traceback
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

print("=" * 50)
print("Soko Client - Test modułów")
print("=" * 50)
print(f"Katalog projektu: {ROOT}")
print()

modules = [
    "ui.app",
    "ui.home",
    "ui.mods",
    "ui.modpacks",
    "ui.settings",
    "ui.account",

    "core.minecraft",
    "core.install",
    "core.fabric",
    "core.forge",
    "core.neoforge",
    "core.java",
    "core.auth",
    "core.profiles",
    "core.versions",
    "core.downloader",

    "mods.search",
    "mods.install",
    "mods.update",
    "mods.remove",
    "mods.dependencies",

    "modpacks.create",
    "modpacks.install",
    "modpacks.export",
    "modpacks.importer",
    "modpacks.manager",

    "api.modrinth",
    "api.minecraft",
    "api.news",

    "utils.config",
    "utils.logger",
    "utils.paths",

    "services.launcher_service",
    "services.mod_service",
    "services.modpack_service",

    "database.database",

    "network.client",
    "network.api_client",

    "security.scanner",

    "updates.updater",

    "profiles.profile",

    "cache.cache",
    "storage.storage",
    "plugins.plugin"
]

ok = 0
bad = 0

for module in modules:
    try:
        importlib.import_module(module)
        print(f"[OK]    {module}")
        ok += 1
    except Exception:
        print(f"[BŁĄD] {module}")
        traceback.print_exc()
        bad += 1

print()
print("=" * 50)
print(f"Poprawne: {ok}")
print(f"Błędy:    {bad}")
print("=" * 50)

input("\nNaciśnij Enter, aby zakończyć...")
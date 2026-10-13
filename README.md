# Clear Rules

> 🛟 **Need help or found a bug?** Get support at [support.doodesch.de/clearrules](https://support.doodesch.de/clearrules).

Adds English rule explanations to existing cards in the cabin game. Read the extra instructions below the original card text. Random answers remain hidden.

Covers The Knight, Clovers of Doom, The Thief, The Visitor, Red Balloons, The Basement and Feeling Small? The explanations include balloon-event doors, breaker light rules and the train's changing shape task. The mod changes card descriptions and leaves event mechanics unchanged.

## Install

1. Close the game and install [UE4SS for the cabin game](https://www.nexusmods.com/thecabingame/mods/4).
2. Copy `Mods/CabinClearRules` from the ZIP into the game folder's `the_cabin_game/Binaries/Win64/ue4ss/Mods`.
3. Start the game and read a supported card.

Keep existing UE4SS files and shared settings. The included `enabled.txt` enables this mod.

## Settings

Use optional [Mod Settings](https://www.nexusmods.com/thecabingame/mods/6) in the main menu to enable or disable the added explanations. Apply saves the choice; Cancel discards unsaved changes. The mod works with its default enabled setting when Mod Settings is absent.

## Remove

Close the game and remove only `ue4ss/Mods/CabinClearRules`. Back up `Scripts/settings.dat` first if you want to keep your preference.

## Build and release

Use Python 3.13. Run `python -m pip install -r requirements-dev.txt`, `python -m unittest discover -s tests -v`, `python tests/check_lua.py`, then `python tools/package.py`.

The builder writes a deterministic ZIP and checksum in `dist`. Runtime Lua is covered by the acceptance fingerprint. `python tools/package.py --release` requires current game acceptance. The development baseline is Steam build `25553694`, Unreal 5.5 and UE4SS `v3.0.1-1164-g5e627997`.

CI checks Linux and Windows. See [publishing](docs/publishing.md) for the GitHub/Nexus flow and [Nexus description](docs/nexus.md) for the listing text. See [LICENSE.md](LICENSE.md) for the custom DooDesch license.

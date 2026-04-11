# BDCC Historical Mod Scanner

*Where did that one mod go?*

This python script scans https://github.com/Alexofp/BDCCMods for all mods that have ever been committed in the past and provides information on the most recent version available in the git history via a CSV file.
* Mods are keyed by name (two mods of the same exact name might replace on another, newest has preference)
* There's no indicator if a mod works or not
* There's no indicator if a mod has been replaced by another, newer mod

This is only mean to be an easier method to search for mods you may be interested in.

### *Just show me the mods!*
1. Open `allallmods.csv` in excel or google sheets yourself. 
2. Set the delimiter to `;` (semicolon). Google sheets does this automatically for you.
3. Optionally select all columns and click "Create a filter". You can then sort or filter as you want.
4. Search for mods you want. The download link to the latest (newest) version of the mod is provided on the right.

### *I'm security conscious...*
Good! Here's some info:
* If you're concerned, just stick with the CSV file.
* CSV is just like a pure text file. You can also search it with a text editor if you really want. It cannot contain macro exploits like typical excel documents.
* All URLs are static links to the BDCCMods repository. You can explore and search for the mods yourself if you want via github (the latest commit is provided too).
* All the source is here - you can read it, and its not too long! Maybe the most risky thing is this that the python script runs `git checkout` repeatedly in the directory you provide.

### *I want to generate the csv myself!*
1. Install git and python3
2. Run `git clone https://github.com/Alexofp/BDCCMods` somewhere
3. Run `python modscanner.py C:/path/to/BDCCMods`
4. It will then checkout all versions of `allmods.json` and compile them into `allallmods.csv` 
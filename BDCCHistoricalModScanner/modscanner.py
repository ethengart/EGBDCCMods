import argparse
import json
import subprocess


def get_file_history(cwd: str, path: str):
    result = subprocess.run(
        ["git", "log", "--follow", "--format=%H", "--", path],
        capture_output=True,
        text=True,
        check=False,
        cwd=cwd,
    )
    return result.stdout.splitlines()


def git_checkout(cwd: str, target: str):
    result = subprocess.run(["git", "checkout", "-q", target], check=False, cwd=cwd)
    if result.returncode != 0:
        print(f"Error checking out {target}")
        return False
    return True


def parse_json(reader):
    data = reader.read()
    for _ in range(20):
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON line {e.lineno}: {e}")

            # Attempt repair
            data = data.splitlines()
            if e.lineno - 1 < 0 or e.lineno - 1 >= len(data):
                print("Line number out of range, giving up")
                break
            data[e.lineno - 1] = ""
            data = "\n".join(data)

    print("Giving up")


def get_allmods_now(git_cwd: str, allmods_filename: str):
    with open(f"{git_cwd}/{allmods_filename}", "r", encoding="utf-8") as reader:
        return parse_json(reader)


def get_commit_download_url(commit: str, existing_url: str):
    # Change A to B for a specific commit
    # A: https://raw.githubusercontent.com/Alexofp/BDCCMods/main/mods/Horny_Bat_v1_.20.zip
    # B: https://raw.githubusercontent.com/Alexofp/BDCCMods/0dd6a1b8b2733f44339155cb00c4ca967fa53584/mods/Horny_Bat_v1_.20.zip
    if existing_url.startswith(
        "https://raw.githubusercontent.com/Alexofp/BDCCMods/main/"
    ):
        return existing_url.replace(
            "https://raw.githubusercontent.com/Alexofp/BDCCMods/main/",
            f"https://raw.githubusercontent.com/Alexofp/BDCCMods/{commit}/",
        )
    print(f"Unexpected URL format: {existing_url}")
    return "ERROR"


def sanitize_csv_field(value: str):
    return value.replace(";", ",").replace("\n", " ")


def main(git_cwd: str = None):
    allmods_filename = "allmods.json"

    git_checkout(git_cwd, "origin/main")
    try:
        allmods_list = []
        commits = get_file_history(git_cwd, allmods_filename)
        print(len(commits))
        for i, commit in enumerate(commits):
            # if i >= 20:
            #     # Stop for now for testing
            #     break

            print(f"Checking out {commit} ({i+1}/{len(commits)})")
            if not git_checkout(git_cwd, commit):
                continue

            allmods_list.append(
                {"mods": get_allmods_now(git_cwd, allmods_filename), "commit": commit}
            )

        print(len(allmods_list))

        everymod: dict[str, list[dict]] = {}
        latest = True
        for allmods_data in allmods_list:
            allmods = allmods_data["mods"]
            commit = allmods_data["commit"]
            if not allmods:
                continue
            if "mods" not in allmods:
                print("No 'mods' key in allmods, skipping")
                continue
            mods = allmods["mods"]
            for mod in mods:
                if "name" not in mod:
                    print("No 'name' key in mod, skipping")
                    continue
                mod_name = mod["name"]
                if mod_name not in everymod:
                    everymod[mod_name] = []

                mod_hash = hash(json.dumps(mod))
                if (
                    everymod[mod_name]
                    and everymod[mod_name][-1]["mod_hash"] == mod_hash
                ):
                    # Skip mods that haven't changed
                    continue

                everymod[mod_name].append(
                    {
                        "mod_detail": mod,
                        "mod_hash": mod_hash,
                        "commit": commit,
                        "is_latest": latest,
                    }
                )
            latest = False

        with open("allallmods.csv", "w", encoding="utf-8") as writer:
            writer.write(
                "Mod Name;Author;Description;Versions;Is Latest;Latest Commit;Latest Download\n"
            )
            for mod_name, mod_list in everymod.items():
                writer.write(
                    f"{sanitize_csv_field(mod_name)};"
                    f"{sanitize_csv_field(mod_list[0]['mod_detail'].get('author', 'N/A'))};"
                    f"{sanitize_csv_field(mod_list[0]['mod_detail'].get('description', 'N/A'))};"
                    f"{len(mod_list)};"
                    f"{mod_list[0]['is_latest']};"
                    f"{mod_list[0]['commit']};"
                    f"{get_commit_download_url(mod_list[0]['commit'], mod_list[0]['mod_detail'].get('download', 'N/A'))}\n"
                )

    finally:
        git_checkout(git_cwd, "origin/main")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "git_cwd",
        type=str,
        help="Path to the BDCCMods git repository (e.g. C:/BDCCMods)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    main(args.git_cwd)

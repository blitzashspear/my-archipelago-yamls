from pathlib import Path
import yaml

YAMLS_FOLDER = Path(__file__).parent.parent
ASYNC_FOLDER= Path(__file__).parent.parent/"async"

def valid_yaml():
    for path in sorted(YAMLS_FOLDER.rglob("*.yaml")):
        try:
            with path.open(encoding="utf-8") as file:
                data = yaml.safe_load(file) or {}
        except yaml.scanner.ScannerError:
            print("VALID YAML TEST FAILED")
            print(path.name)
            return False
    return True

def async_balancing():
    failed_yamls = []

    for path in sorted(ASYNC_FOLDER.glob("*.yaml")):
        with path.open(encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        game_options = data.get(data.get("game"), {})
        if game_options.get("progression_balancing") != "disabled":
            failed_yamls.append(path)

    if failed_yamls:
        print("ASYNC PROGRESSION BALACING TEST FAILED")
        for path in failed_yamls:
            print("\tasync/"+path.name)

def valid_name():
    failed_yamls = []

    for path in sorted(YAMLS_FOLDER.rglob("*.yaml")):
        with path.open(encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        if len(str(data.get("name", ""))) > 16:
            failed_yamls.append(path)

    if failed_yamls:
        print("VALID NAME TEST FAILED")
        for path in failed_yamls:
            print("\t" + str(path.relative_to(YAMLS_FOLDER)))

if __name__ == "__main__":
    if not valid_yaml():
        quit()
    async_balancing()
    valid_name()
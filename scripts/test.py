from pathlib import Path
import re
import yaml

YAMLS_FOLDER = Path(__file__).parent.parent

# This entire script is AI slopped because I don't fucking care.

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

    for path in sorted((YAMLS_FOLDER/"async").glob("*.yaml")):
        with path.open(encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        game_options = data.get(data.get("game"), {})
        if game_options.get("progression_balancing") != "disabled":
            failed_yamls.append(path)

    if failed_yamls:
        print("ASYNC PROGRESSION BALACING TEST FAILED")
        for path in failed_yamls:
            print("\tasync/"+path.name)
        return False
    return True

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
        return False
    return True

def ends_with_new_line():
    failed_yamls = []

    for path in sorted(YAMLS_FOLDER.rglob("*.yaml")):
        with path.open("rb") as file:
            if not file.read().endswith(b"\n"):
                failed_yamls.append(path)

    if failed_yamls:
        print("ENDS WITH NEW LINE TEST FAILED")
        for path in failed_yamls:
            print("\t" + str(path.relative_to(YAMLS_FOLDER)))
        return False
    return True

def no_non_empty_brackets():
    failed_yamls = []

    for path in sorted(YAMLS_FOLDER.rglob("*.yaml")):
        with path.open(encoding="utf-8") as file:
            if re.search(r"\[[^\[\]]+\]|\{[^\{\}]+\}", file.read()):
                failed_yamls.append(path)

    if failed_yamls:
        print("NO NON-EMPTY BRACKETS TEST FAILED")
        for path in failed_yamls:
            print("\t" + str(path.relative_to(YAMLS_FOLDER)))
        return False
    return True

def readable_comments():
    failed_comments = []

    for path in sorted(YAMLS_FOLDER.rglob("*.yaml")):
        with path.open(encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line_without_double_quoted_strings = re.sub(r'"(?:\\.|[^"\\])*"', "", line)
                if re.search(r"#[^#\s]", line_without_double_quoted_strings):
                    failed_comments.append((path, line_number))

    if failed_comments:
        print("READABLE COMMENTS TEST FAILED")
        for path, line_number in failed_comments:
            print(f"\t{path.relative_to(YAMLS_FOLDER)}:{line_number}")
        return False
    return True

def yaml_notated():
    failed_yamls = []

    expected_markers = {
        YAMLS_FOLDER / "async": "# ASYNC ONLY",
        YAMLS_FOLDER / "side": "# SIDE GAME",
    }
    for folder, expected_marker in expected_markers.items():
        for path in sorted(folder.glob("*.yaml")):
            with path.open(encoding="utf-8") as file:
                lines = file.readlines()

            marker = lines[2].rstrip("\r\n") if len(lines) > 2 else ""
            if (folder.name == "async" and not marker.startswith(expected_marker)) or (
                folder.name == "side" and marker != expected_marker
            ):
                failed_yamls.append(path)

    if failed_yamls:
        print("YAML NOTATION TEST FAILED")
        for path in failed_yamls:
            print("\t" + str(path.relative_to(YAMLS_FOLDER)))
        return False
    return True

if __name__ == "__main__":
    if not valid_yaml():
        quit()
    if not async_balancing():
        quit()
    if not valid_name():
        quit()
    if not ends_with_new_line():
        quit()
    if not no_non_empty_brackets():
        quit()
    if not readable_comments():
        quit()
    if not yaml_notated():
        quit()
    print("ALL TESTS PASSED")
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
import tomllib
from urllib.request import Request, urlopen

import yaml

YAMLS_FOLDER = Path(__file__).parent.parent
INDEX_API_URL = "https://api.github.com/repos/ionium-ap/Archipelago-index/contents/index"

# This entire script is AI slopped because I don't fucking care.

def index_games(local_games):
	def index_game_name(entry):
		request = Request(entry["download_url"], headers={"User-Agent": "archipelago-yaml-stats"})
		with urlopen(request, timeout=10) as response:
			data = tomllib.loads(response.read().decode("utf-8"))
			return data.get("name")
		
	request = Request(INDEX_API_URL, headers={"User-Agent": "archipelago-yaml-stats"})
	with urlopen(request, timeout=10) as response:
		entries = json.load(response)

	index_entries = [entry for entry in entries if entry["name"].endswith(".toml")]
	with ThreadPoolExecutor() as executor:
		indexed_games = list(executor.map(index_game_name, index_entries))
	return [game for game in local_games if game in indexed_games]

def yaml_paths_for_scope(scope):
	paths = [path for path in YAMLS_FOLDER.rglob("*.yaml")]
	if scope == "ready":
		paths = [
			path for path in paths
			if path.relative_to(YAMLS_FOLDER).parts and path.relative_to(YAMLS_FOLDER).parts[0] not in {"untested", "waiting"}
		]
	return paths

if __name__ == "__main__":
	scope_prompt = input("Run stats for all YAMLs or ready YAMLs only? [all/ready]: ").strip().lower()
	scope = "ready" if scope_prompt in {"ready", "r"} else "all"
	selected_paths = yaml_paths_for_scope(scope)

	total = 0
	games = []
	game_counts = []
	death_link_count = 0
	for path in selected_paths:
		with path.open(encoding="utf-8") as file:
			data = yaml.safe_load(file) or {}
		game = data.get("game")
		if not any(game == existing_game for existing_game in games):
			games.append(game)

		game_options = data.get(game, {}) if isinstance(game, str) else {}
		if game_options.get("death_link") is True:
			death_link_count += 1

		for existing_game, count in game_counts:
			if game == existing_game:
				game_counts[game_counts.index((existing_game, count))] = (existing_game, count + 1)
				break
		else:
			game_counts.append((game, 1))

	for folder in sorted(path for path in YAMLS_FOLDER.iterdir() if path.is_dir()):
		count = sum(1 for file_path in selected_paths if file_path.parent == folder)
		if not count:
			continue
		total += count
		print(f"{folder.name}: {count} YAMLS")

	len_games = len(games)
	print(f"TOTAL: {total} YAMLS")
	print(f"UNIQUE GAMES: {len_games}")
	print("GAMES WITH 2 OR MORE YAMLS:")
	for game, count in sorted(game_counts, key=lambda game_count: str(game_count[0])):
		if count > 1:
			print(f"\t{game}: {count}")
	print(f"DEATHLINK ENABLED: {death_link_count} YAMLS")
	index_prompt = input("Check Ionium compatibility? [Y/N]: ").strip().lower()
	if index_prompt in {"y", "yes"}:
		len_index_games = len(index_games(games))
		percentage_index_games = round(len_index_games / len_games * 100)
		print(f"{len_index_games} GAMES ({percentage_index_games}%) SUPPORTED BY IONIUM")

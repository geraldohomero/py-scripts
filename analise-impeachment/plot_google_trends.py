from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Gera grafico de serie temporal a partir de CSV do Google Trends."
	)
	parser.add_argument(
		"--input",
		default="bolsonaro-ustra-trends-google.csv",
		help="CSV de entrada com colunas Time, bolsonaro e ustra.",
	)
	parser.add_argument(
		"--output",
		default="bolsonaro-ustra-trends-google.png",
		help="Imagem de saida em PNG.",
	)
	parser.add_argument(
		"--title",
		default="Google Trends: Bolsonaro x Ustra",
		help="Titulo do grafico.",
	)
	parser.add_argument(
		"--show",
		action="store_true",
		help="Abre o grafico apos salvar.",
	)
	return parser.parse_args()


def load_trends_csv(csv_path: Path) -> tuple[list[datetime], list[int], list[int]]:
	dates: list[datetime] = []
	bolsonaro_values: list[int] = []
	ustra_values: list[int] = []

	with csv_path.open("r", encoding="utf-8", newline="") as handle:
		reader = csv.DictReader(handle)
		for row in reader:
			time_str = (row.get("Time") or "").strip().strip('"')
			b_str = (row.get("bolsonaro") or "").strip()
			u_str = (row.get("ustra") or "").strip()

			if not time_str or not b_str or not u_str:
				continue

			try:
				dates.append(datetime.strptime(time_str, "%Y-%m-%d"))
				bolsonaro_values.append(int(b_str))
				ustra_values.append(int(u_str))
			except ValueError:
				continue

	return dates, bolsonaro_values, ustra_values


def main() -> int:
	args = parse_args()
	input_path = Path(args.input)
	output_path = Path(args.output)

	if not input_path.exists():
		print(f"CSV nao encontrado: {input_path}", file=sys.stderr)
		return 1

	try:
		import matplotlib.dates as mdates
		import matplotlib.pyplot as plt
	except ImportError:
		print("Dependencia ausente: matplotlib. Instale com 'pip install matplotlib'.", file=sys.stderr)
		return 1

	dates, bolsonaro_values, ustra_values = load_trends_csv(input_path)
	if not dates:
		print("Nao foi possivel carregar dados validos do CSV.", file=sys.stderr)
		return 1

	fig, ax = plt.subplots(figsize=(14, 7))
	ax.plot(dates, bolsonaro_values, label="bolsonaro", color="#0b4f6c", linewidth=2)
	ax.plot(dates, ustra_values, label="ustra", color="#c1121f", linewidth=2)

	ax.set_title(args.title)
	ax.set_xlabel("Tempo")
	ax.set_ylabel("Interesse (0-100)")
	ax.legend()
	ax.grid(True, alpha=0.3)

	ax.xaxis.set_major_locator(mdates.YearLocator(2))
	ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
	fig.autofmt_xdate()
	fig.tight_layout()

	fig.savefig(output_path, dpi=300)
	print(f"Grafico salvo em: {output_path}")

	if args.show:
		plt.show()

	return 0


if __name__ == "__main__":
	raise SystemExit(main())
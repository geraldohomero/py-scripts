from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Gera grafico de frequencia de palavras a partir de CSV."
	)
	parser.add_argument(
		"--input",
		default="word_frequencies.csv",
		help="CSV de entrada com colunas 'word' e 'count'.",
	)
	parser.add_argument(
		"--top",
		type=int,
		default=20,
		help="Quantidade de palavras a mostrar no grafico.",
	)
	parser.add_argument(
		"--output",
		default="word_frequencies.png",
		help="Arquivo de imagem de saida.",
	)
	parser.add_argument(
		"--title",
		default="Frequencia de Palavras - Sessao Impeachment 17/04/2016",
		help="Titulo do grafico.",
	)
	parser.add_argument(
		"--show",
		action="store_true",
		help="Abre janela com o grafico apos salvar o arquivo.",
	)
	return parser.parse_args()


def read_frequency_csv(csv_path: Path, top_n: int) -> tuple[list[str], list[int]]:
	words: list[str] = []
	counts: list[int] = []

	with csv_path.open("r", encoding="utf-8", newline="") as handle:
		reader = csv.DictReader(handle)
		for row in reader:
			word = (row.get("word") or "").strip()
			count_raw = (row.get("count") or "").strip()
			if not word or not count_raw:
				continue
			try:
				count = int(count_raw)
			except ValueError:
				continue

			words.append(word)
			counts.append(count)

	if top_n > 0:
		words = words[:top_n]
		counts = counts[:top_n]

	return words, counts


def main() -> int:
	args = parse_args()
	input_path = Path(args.input)
	output_path = Path(args.output)

	if not input_path.exists():
		print(f"CSV nao encontrado: {input_path}", file=sys.stderr)
		return 1

	try:
		import matplotlib.pyplot as plt
	except ImportError:
		print("Dependencia ausente: matplotlib. Instale com 'pip install matplotlib'.", file=sys.stderr)
		return 1

	words, counts = read_frequency_csv(input_path, args.top)
	if not words:
		print("CSV vazio ou sem dados validos nas colunas 'word' e 'count'.", file=sys.stderr)
		return 1

	plt.style.use("ggplot")
	fig, ax = plt.subplots(figsize=(14, 8))

	plot_words = list(reversed(words))
	plot_counts = list(reversed(counts))

	bars = ax.barh(plot_words, plot_counts, color="#2f6db3")
	ax.set_title(args.title)
	ax.set_xlabel("Frequencia")
	ax.set_ylabel("Palavra")

	for bar, count in zip(bars, plot_counts):
		ax.text(
			bar.get_width() + max(plot_counts) * 0.01,
			bar.get_y() + bar.get_height() / 2,
			str(count),
			va="center",
			fontsize=9,
		)

	fig.tight_layout()
	fig.savefig(output_path, dpi=300)
	print(f"Grafico salvo em: {output_path}")

	if args.show:
		plt.show()

	return 0


if __name__ == "__main__":
	raise SystemExit(main())
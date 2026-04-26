from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path


PORTUGUESE_STOPWORDS = {
	"a",
	"as",
	"ao",
	"aos",
	"aquela",
	"aquelas",
	"aquele",
	"aqueles",
	"aquilo",
	"com",
	"como",
	"da",
	"das",
	"de",
	"dela",
	"delas",
	"dele",
	"deles",
	"depois",
	"do",
	"dos",
	"e",
	"ela",
	"elas",
	"ele",
	"eles",
	"em",
	"entre",
	"era",
	"eram",
	"essa",
	"essas",
	"esse",
	"esses",
	"esta",
	"estas",
	"este",
	"estes",
	"eu",
	"foi",
	"foram",
	"ha",
	"isso",
	"isto",
	"ja",
	"la",
	"lhe",
	"lhes",
	"mais",
	"mas",
	"me",
	"mesmo",
	"meu",
	"meus",
	"minha",
	"minhas",
	"muito",
	"na",
	"nas",
	"nem",
	"no",
	"nos",
	"nossa",
	"nossas",
	"nosso",
	"nossos",
	"num",
	"numa",
	"o",
	"os",
	"ou",
	"para",
	"pela",
	"pelas",
	"pelo",
	"pelos",
	"por",
	"qual",
	"quando",
	"que",
	"quem",
	"se",
	"sem",
	"seu",
	"seus",
	"sua",
	"suas",
	"tambem",
	"te",
	"tem",
	"tendo",
	"tenho",
	"ter",
	"teu",
	"teus",
	"tu",
	"tua",
	"tuas",
	"um",
	"uma",
	"voces",
	"vos",
	"final",
	"deliberativa",
	"deputado",
	"presidente",
	"voto",
	"não",
	"sim",
	"votos",
	"total",
	"câmara",
	"eduardo",
	"beto",
	"tipo",
	"sessão",
	"deputados",
	"data",
	"número",
	"extraordinária",
	"detaq",
	"aqui"
	"são",
	"paulo",
	"minas",
	"felipe",
	"srs",
	"hoje",
	"quero",
	"estão",
	"neste",
	"vamos",
	"minas",
	"todos",
	"palmas",
	"aqui",
	"plenário",
	"são",
	"nome",
	"rio",
	"deputada",
	"porque",
	"sras",
	"vai",
	"ser",
	"gerais",
	"fazer",
	"janeiro",
	"bahia",
	"sra",
	"dizer",
	"mansur",
	"cunha",
	"redação",
	"bloco",
	"vota",
	"nesta",
    "psb",
	"pmdb",
	"pt",
	"psdb",
	"pdt",
	"prb",
	"psol",
    "psd",
	"cada",
	"deste",
	"ptb",
	"estamos",
	"votar",
	"favor",
	"dem",
	"joão",
	"bem",
	"exa",
	"paraná",
	"vou",
	"fora",
	"sou",	
	"votou",
	"bancada",
	"orador",
}


def build_stopwords_with_variants(base_stopwords: set[str]) -> set[str]:
	with_variants = set(base_stopwords)
	with_variants.update(
		"".join(
			char
			for char in unicodedata.normalize("NFD", token)
			if unicodedata.category(char) != "Mn"
		)
		for token in base_stopwords
	)
	return with_variants


PORTUGUESE_STOPWORDS_ALL = build_stopwords_with_variants(PORTUGUESE_STOPWORDS)


def remove_diacritics(text: str) -> str:
	normalized = unicodedata.normalize("NFD", text)
	return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def extract_text_from_pdf(pdf_path: Path) -> str:
	try:
		from pypdf import PdfReader
	except ImportError as exc:
		raise RuntimeError(
			"Dependencia ausente: pypdf. Instale com 'pip install pypdf'."
		) from exc

	reader = PdfReader(str(pdf_path))
	pages_text: list[str] = []
	for page in reader.pages:
		pages_text.append(page.extract_text() or "")
	return "\n".join(pages_text)


def tokenize(
	text: str,
	min_length: int = 3,
	remove_accents: bool = False,
	use_stopwords: bool = True,
	extra_excluded: set[str] | None = None,
) -> list[str]:
	clean_text = text.lower()
	if remove_accents:
		clean_text = remove_diacritics(clean_text)

	tokens = re.findall(r"[a-zA-ZÀ-ÿ]+", clean_text)

	excluded = set(extra_excluded or set())
	if remove_accents:
		excluded = {remove_diacritics(token.lower()) for token in excluded}
	else:
		excluded = {token.lower() for token in excluded}

	filtered: list[str] = []
	for token in tokens:
		normalized_token = remove_diacritics(token)
		if len(token) < min_length:
			continue
		if use_stopwords and normalized_token in PORTUGUESE_STOPWORDS_ALL:
			continue
		if token in excluded:
			continue
		filtered.append(token)

	return filtered


def save_frequencies_csv(counter: Counter[str], csv_path: Path, top_n: int) -> None:
	with csv_path.open("w", newline="", encoding="utf-8") as handle:
		writer = csv.writer(handle)
		writer.writerow(["word", "count"])
		for word, count in counter.most_common(top_n):
			writer.writerow([word, count])


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Analise de frequencia de palavras de um PDF."
	)
	parser.add_argument(
		"--input",
		default="doc.pdf",
		help="Arquivo PDF de entrada (padrao: doc.pdf).",
	)
	parser.add_argument(
		"--top",
		type=int,
		default=50,
		help="Quantidade de palavras mais frequentes para mostrar.",
	)
	parser.add_argument(
		"--min-length",
		type=int,
		default=3,
		help="Tamanho minimo da palavra para contar.",
	)
	parser.add_argument(
		"--remove-accents",
		action="store_true",
		help="Remove acentos antes da tokenizacao.",
	)
	parser.add_argument(
		"--no-stopwords",
		action="store_true",
		help="Nao remove stopwords em portugues.",
	)
	parser.add_argument(
		"--exclude",
		nargs="*",
		default=[],
		help="Lista extra de termos para excluir da contagem.",
	)
	parser.add_argument(
		"--output-csv",
		default="word_frequencies.csv",
		help="CSV de saida com as frequencias (padrao: word_frequencies.csv).",
	)
	parser.add_argument(
		"--no-csv",
		action="store_true",
		help="Nao gera arquivo CSV.",
	)
	return parser.parse_args()


def main() -> int:
	args = parse_args()
	input_path = Path(args.input)
	if not input_path.exists():
		print(f"Arquivo nao encontrado: {input_path}", file=sys.stderr)
		return 1

	try:
		text = extract_text_from_pdf(input_path)
	except RuntimeError as exc:
		print(str(exc), file=sys.stderr)
		return 1

	tokens = tokenize(
		text=text,
		min_length=args.min_length,
		remove_accents=args.remove_accents,
		use_stopwords=not args.no_stopwords,
		extra_excluded=set(args.exclude),
	)

	frequency = Counter(tokens)

	print(f"Arquivo analisado: {input_path}")
	print(f"Tokens validos: {len(tokens)}")
	print(f"Vocabulario unico: {len(frequency)}")
	print("\nTop palavras:\n")
	for word, count in frequency.most_common(args.top):
		print(f"{word:25} {count}")

	if not args.no_csv:
		csv_path = Path(args.output_csv)
		save_frequencies_csv(frequency, csv_path, args.top)
		print(f"\nCSV salvo em: {csv_path}")

	return 0


if __name__ == "__main__":
	raise SystemExit(main())

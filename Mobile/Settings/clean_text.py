import re

with open(
    r"C:\Projects\CorpID\Mock-HTML\Mobile\Settings\compiled_text.txt",
    "r",
    encoding="utf-8",
) as f:
    lines = f.readlines()

# Clean each line
output_lines = []
for line in lines:
    # Strip line number prefix like "123: "
    line = re.sub(r"^\d+:\s", "", line)

    # Remove image headers
    if re.match(r"^---\s*Image\s*\(\d+\)\.jpg\s*---", line):
        continue

    # Remove timestamp artifacts like "4:20 2 > @", "4:21 nw! > GO", "4:23 :! 全 20 |"
    line = re.sub(r"^\d+:\d+\s*[\w!@>\|&\.\s\u4e00-\u9fff]+$", "", line)
    line = re.sub(r"^\d+:\d+\s*[\w!@>\|&\.\s\u4e00-\u9fff]+", "", line)

    # Remove common OCR noise artifacts (uppercase garbage words)
    noise_words = [
        "SAB",
        "TARR",
        "WAP",
        "BAR",
        "BA",
        "7G",
        "MA BAG Bes",
        "RAUBER",
        "BORE",
        "FH",
        "RR",
        "TBA",
        "BS",
        "TEA",
        "BRA",
        "IMR",
        "SAG",
        "STEN",
        "HAG",
        "Sax HAG",
        "CEA",
        "Rint",
        "ESE",
        "SRG",
        "EAB",
        "BAB",
        "ABU",
        "SARs",
        "SAB it",
        "HAP",
        "HENS",
        "Sake",
        "ARMAEALI",
        "BNR",
        "MABE",
        "TS",
        "SAG",
        "SAB",
        "SAB",
        "SAB",
        "SAB",
        "SAB",
        "SAB",
    ]
    for noise in noise_words:
        line = re.sub(r"\b" + re.escape(noise) + r"\b", "", line)

    # Remove specific garbled strings
    line = re.sub(r"Sse eo ee 4 Ee ob OR \(cE", "", line)
    line = re.sub(r"Sse eo ee 4 Ee ob OR", "", line)
    line = re.sub(r"Sse eo ee", "", line)
    line = re.sub(r"Resa \(Sse eo ee 4 Ee ob OR \(cE", "", line)

    # Remove random single characters that are artifacts
    line = re.sub(r"^[oO]$", "", line)
    line = re.sub(r"^A!$", "", line)

    # Clean up whitespace
    line = line.strip()

    # Skip empty lines for now (we'll add them back as needed)
    if line:
        output_lines.append(line)

# Deduplicate: keep only first occurrence of each line, but only for short exact duplicates
# For longer content, we need to keep flowing text.
seen = set()
final_lines = []
for line in output_lines:
    if line in seen and len(line) < 80:
        continue
    seen.add(line)
    final_lines.append(line)

with open(
    r"C:\Projects\CorpID\Mock-HTML\Mobile\Settings\cleaned_text.txt",
    "w",
    encoding="utf-8",
) as f:
    f.write("\n".join(final_lines))

print(f"Processed {len(lines)} lines -> {len(final_lines)} lines")

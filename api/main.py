from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import re

app = FastAPI()

# Allow CORS for testing (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ICHIRAN_CLI_PATH = "/ichiran-bin/ichiran-cli"

SENSE_LINE = re.compile(r"^(\d+)\.\s+(?:\[(.+?)\]\s+)?(.+)$")

def _parse_cli_output(raw_output: str) -> dict:
    lines = [line.rstrip() for line in raw_output.splitlines() if line.strip()]
    if not lines:
        return {"romanized": "", "entries": []}

    romanized = lines[0].strip()
    entries = []
    current = None

    for line in lines[1:]:
        if line.startswith("* "):
            header = line[2:].strip()
            romaji = header
            written = None
            reading = None

            if "  " in header:
                romaji, rest = header.split("  ", 1)
                romaji = romaji.strip()
                rest = rest.strip()
            else:
                rest = ""

            if rest:
                if "【" in rest and "】" in rest:
                    start = rest.index("【")
                    end = rest.index("】", start)
                    reading = rest[start + 1:end].strip() or None
                    written_part = rest[:start].strip()
                    written = written_part or None
                else:
                    written = rest or None

            current = {
                "romanized": romaji,
                "written": written,
                "reading": reading,
                "senses": []
            }
            entries.append(current)
            continue

        if current:
            match = SENSE_LINE.match(line)
            if match:
                number = int(match.group(1))
                pos_raw = match.group(2)
                gloss = match.group(3).strip()
                pos = [item.strip() for item in pos_raw.split(",")] if pos_raw else []
                current["senses"].append({
                    "number": number,
                    "pos": pos,
                    "gloss": gloss
                })
            elif current["senses"]:
                current["senses"][-1]["gloss"] += f" {line.strip()}"
            else:
                current.setdefault("notes", []).append(line.strip())

    return {"romanized": romanized, "entries": entries}


@app.get("/parse")
def parse(text: str):
    try:
        result = subprocess.run(
            [ICHIRAN_CLI_PATH, "-i", text],
            capture_output=True,
            text=True,
            check=True
        )
        raw_output = result.stdout.strip()
        structured = _parse_cli_output(raw_output)
        return {
            "input": text,
            "romanized": structured["romanized"],
            "entries": structured["entries"],
            "raw": raw_output
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=e.stderr)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"{ICHIRAN_CLI_PATH} not found")

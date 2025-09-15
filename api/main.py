from fastapi import FastAPI, Query
import subprocess

app = FastAPI()

@app.get("/parse")
def parse(text: str = Query(..., description="Japanese text to analyze")):
    try:
        result = subprocess.run(
            ["ichiran-cli", "-i", text],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return {"error": result.stderr.strip()}
        return {"output": result.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}

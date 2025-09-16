from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess

app = FastAPI()

# Allow CORS for testing (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ICHIRAN_CLI_PATH = "/ichiran-bin/ichiran-cli"

@app.get("/parse")
def parse(text: str):
    try:
        result = subprocess.run(
            [ICHIRAN_CLI_PATH, "-i", text],
            capture_output=True,
            text=True,
            check=True
        )
        return {"result": result.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=e.stderr)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"{ICHIRAN_CLI_PATH} not found")

param(
    [ValidateSet("setup", "run", "lint")]
    [string]$Action = "run"
)

$ErrorActionPreference = "Stop"

function Ensure-Uv {
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        throw "uv не найден в PATH. Установите: pip install uv"
    }
}

function Setup-Project {
    Write-Host "Creating virtual environment with uv..."
    uv venv

    Write-Host "Installing dependencies..."
    uv pip compile pyproject.toml -o requirements.txt
    uv pip install -r requirements.txt

    if (-not (Test-Path ".env")) {
        Copy-Item ".env.example" ".env"
        Write-Host "Created .env from .env.example"
    }

    Write-Host "Setup complete."
}

function Run-App {
    Write-Host "Starting FastAPI app..."
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

function Run-Lint {
    Write-Host "Running ruff check..."
    uv run ruff check .
}

Ensure-Uv

switch ($Action) {
    "setup" { Setup-Project }
    "run"   { Run-App }
    "lint"  { Run-Lint }
}

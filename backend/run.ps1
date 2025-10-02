# run.ps1 - PowerShell equivalent for development server script

Write-Host "Starting RAG ChatBot Backend..." -ForegroundColor Green

# --- Activate virtual environment (Windows/PowerShell) ---
$venvPath = ".venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
} else {
    Write-Host "Virtual environment not found. Run 'uv venv' first." -ForegroundColor Red
    exit 1
}

# --- Ensure requirements.txt exists ---
if (-not (Test-Path "requirements.txt")) {
    Write-Host "requirements.txt not found." -ForegroundColor Red
    exit 1
}

# --- Install dependencies ---
Write-Host "Installing dependencies..." -ForegroundColor Yellow
uv pip install -r requirements.txt

# --- Run the FastAPI server with reload for development ---
Write-Host "Starting server on http://localhost:8000" -ForegroundColor Cyan
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
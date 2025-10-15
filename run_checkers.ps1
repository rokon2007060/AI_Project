# PowerShell script to run checkers game
Write-Host "Starting Checkers Game..." -ForegroundColor Green
& ".\pygame-env\Scripts\Activate.ps1"
python main.py
Read-Host "Press Enter to exit"


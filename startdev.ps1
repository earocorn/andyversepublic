Write-Host "Starting Django dev server..."
Set-Location "./andyversebackend"
Start-Process "python" "manage.py runserver"

Start-Sleep -Seconds 5

Set-Location ".."
Set-Location "./andyversesvelte"
Write-Host "Starting SvelteKit dev server..."
Start-Process "npm" "run dev -- --host"
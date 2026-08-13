param (
    [string]$GpgKeyId
)

if (-not $GpgKeyId) {
    Write-Host "[-] Error: GpgKeyId is required to enforce signed commits." -ForegroundColor Red
    Write-Host "Usage: .\enforce_gpg_signing.ps1 -GpgKeyId <YOUR_KEY_ID>" -ForegroundColor Yellow
    exit 1
}

git config local user.signingkey $GpgKeyId
git config local commit.gpgsign true
git config local tag.gpgsign true

Write-Host "[+] Sovereign GPG Commit Signing Enforced for Local Dome Repository." -ForegroundColor Green
Write-Host "[+] Key ID bound: $GpgKeyId" -ForegroundColor Cyan

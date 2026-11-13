# Quick verification script for Campus Lab Resources DevOps Project
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Campus Lab Resources Management - DevOps Project Checker " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check Git Branch History
Write-Host "`n[1/4] Checking Git Branch & Merge History..." -ForegroundColor Yellow
git log --graph --oneline --all

# 2. Package Artifact
Write-Host "`n[2/4] Testing Build & Packaging (package.py)..." -ForegroundColor Yellow
python package.py

# 3. Check Files Required by Rubric
Write-Host "`n[3/4] Verifying Assignment Deliverables..." -ForegroundColor Yellow
$requiredFiles = @(
    "src/app.py",
    "tests/test_app.py",
    "requirements.txt",
    "package.py",
    "Jenkinsfile",
    ".github/workflows/ci.yml",
    "Dockerfile",
    "ansible/inventory.ini",
    "ansible/playbook.yml",
    "ansible/roles/campus_lab_app/tasks/main.yml",
    "ansible/roles/campus_lab_app/handlers/main.yml",
    "k8s/configmap.yaml",
    "k8s/deployment.yaml",
    "k8s/service.yaml",
    "repo_link.txt",
    "report/DevOps_Project_Report.md"
)

$missing = 0
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  [OK] Found $file" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $file" -ForegroundColor Red
        $missing++
    }
}

if ($missing -eq 0) {
    Write-Host "`n[4/4] All required files exist and pass verification! (0 missing)" -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host " You are ready to push to GitHub and capture screenshots! " -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Cyan
} else {
    Write-Host "`n[!] Warning: $missing files are missing." -ForegroundColor Red
}

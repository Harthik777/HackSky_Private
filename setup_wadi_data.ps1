# PowerShell script to set up WADI dataset files
# Run this script from the project root directory

Write-Host "🔄 Setting up WADI dataset files..." -ForegroundColor Yellow

# Create the wadi data directory if it doesn't exist
$wadiDir = "ics-dashboard\data\wadi"
if (!(Test-Path $wadiDir)) {
    New-Item -ItemType Directory -Path $wadiDir -Force
    Write-Host "✅ Created directory: $wadiDir" -ForegroundColor Green
}

# Source files in Downloads
$sourceDir = "C:\Users\Harthik M V\Downloads\archive"
$file1 = "$sourceDir\WADI_14days_new.csv"
$file2 = "$sourceDir\WADI_attackdataLABLE.csv"

# Destination directory
$destDir = $wadiDir

# Copy files
try {
    if (Test-Path $file1) {
        Copy-Item $file1 $destDir -Force
        Write-Host "✅ Copied WADI_14days_new.csv" -ForegroundColor Green
    } else {
        Write-Host "❌ File not found: $file1" -ForegroundColor Red
    }
    
    if (Test-Path $file2) {
        Copy-Item $file2 $destDir -Force
        Write-Host "✅ Copied WADI_attackdataLABLE.csv" -ForegroundColor Green
    } else {
        Write-Host "❌ File not found: $file2" -ForegroundColor Red
    }
    
    Write-Host "🎉 WADI dataset setup complete!" -ForegroundColor Green
    Write-Host "Files are now in: $destDir" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ Error copying files: $($_.Exception.Message)" -ForegroundColor Red
}

# Verify files exist
Write-Host "`n📋 Verification:" -ForegroundColor Yellow
Get-ChildItem $destDir -Filter "*.csv" | ForEach-Object {
    $sizeInMB = [math]::Round($_.Length / 1MB, 2)
    Write-Host "  ✅ $($_.Name) - ${sizeInMB} MB" -ForegroundColor Green
} 
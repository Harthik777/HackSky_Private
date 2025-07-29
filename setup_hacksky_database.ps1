# setup_hacksky_database.ps1
# Complete HackSky MySQL Database Setup Script for Windows
# This script automates the entire database setup process

param(
    [switch]$Reset,
    [switch]$SkipDocker,
    [string]$Environment = "development"
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 HackSky MySQL Database Setup" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if command exists
function Test-Command($command) {
    try {
        Get-Command $command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Function to wait for MySQL to be ready
function Wait-ForMySQL {
    Write-Host "⏳ Waiting for MySQL to be ready..." -ForegroundColor Yellow
    $maxAttempts = 30
    $attempt = 0
    
    do {
        $attempt++
        Start-Sleep -Seconds 2
        
        try {
            $result = docker exec hacksky-mysql mysql -u hacksky -pmysecretpassword -e "SELECT 1" 2>$null
            if ($result) {
                Write-Host "✅ MySQL is ready!" -ForegroundColor Green
                return $true
            }
        } catch {
            # Continue waiting
        }
        
        Write-Host "   Attempt $attempt/$maxAttempts..." -ForegroundColor Gray
    } while ($attempt -lt $maxAttempts)
    
    Write-Host "❌ MySQL failed to start within timeout" -ForegroundColor Red
    return $false
}

# Step 1: Environment Check
Write-Host "📋 Step 1: Environment Check" -ForegroundColor Blue
Write-Host "----------------------------"

# Check Python
if (Test-Command python) {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found. Please install Python 3.8+ from python.org" -ForegroundColor Red
    exit 1
}

# Check Docker (if not skipping)
if (-not $SkipDocker) {
    if (Test-Command docker) {
        Write-Host "✅ Docker found" -ForegroundColor Green
        
        if (Test-Command docker-compose) {
            Write-Host "✅ Docker Compose found" -ForegroundColor Green
        } else {
            Write-Host "❌ Docker Compose not found. Please install Docker Desktop" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "❌ Docker not found. Please install Docker Desktop or use -SkipDocker flag" -ForegroundColor Red
        exit 1
    }
}

# Step 2: Setup Environment Configuration
Write-Host ""
Write-Host "🔧 Step 2: Environment Configuration" -ForegroundColor Blue
Write-Host "------------------------------------"

if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ Created .env file from template" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Creating default .env file" -ForegroundColor Yellow
        @"
DB_HOST=localhost
DB_PORT=3306
DB_USER=hacksky
DB_PASSWORD=mysecretpassword
DB_NAME=ics_monitoring
FLASK_ENV=$Environment
FLASK_DEBUG=true
"@ | Out-File -FilePath ".env" -Encoding UTF8
    }
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# Step 3: Start MySQL Database
if (-not $SkipDocker) {
    Write-Host ""
    Write-Host "🐳 Step 3: Start MySQL Database" -ForegroundColor Blue
    Write-Host "-------------------------------"
    
    try {
        # Check if containers are already running
        $mysqlRunning = docker ps --filter "name=hacksky-mysql" --filter "status=running" --quiet
        
        if ($mysqlRunning) {
            Write-Host "✅ MySQL container already running" -ForegroundColor Green
        } else {
            Write-Host "🚀 Starting MySQL and phpMyAdmin containers..." -ForegroundColor Yellow
            docker-compose up -d mysql phpmyadmin
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Containers started successfully" -ForegroundColor Green
                
                # Wait for MySQL to be ready
                if (-not (Wait-ForMySQL)) {
                    Write-Host "❌ MySQL setup failed" -ForegroundColor Red
                    exit 1
                }
            } else {
                Write-Host "❌ Failed to start containers" -ForegroundColor Red
                exit 1
            }
        }
        
        Write-Host "📊 Database Admin: http://localhost:8080" -ForegroundColor Cyan
        Write-Host "   Username: hacksky" -ForegroundColor Gray
        Write-Host "   Password: mysecretpassword" -ForegroundColor Gray
        
    } catch {
        Write-Host "❌ Docker setup failed: $_" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host ""
    Write-Host "⚠️ Step 3: Skipping Docker Setup (Manual MySQL Required)" -ForegroundColor Yellow
    Write-Host "--------------------------------------------------------"
    Write-Host "Please ensure MySQL is running with:" -ForegroundColor Yellow
    Write-Host "  - Host: localhost:3306" -ForegroundColor Gray
    Write-Host "  - Database: ics_monitoring" -ForegroundColor Gray
    Write-Host "  - User: hacksky" -ForegroundColor Gray
    Write-Host "  - Password: mysecretpassword" -ForegroundColor Gray
}

# Step 4: Install Python Dependencies
Write-Host ""
Write-Host "📦 Step 4: Install Python Dependencies" -ForegroundColor Blue
Write-Host "---------------------------------------"

try {
    Set-Location backend
    
    # Check if virtual environment should be used
    if (Test-Path "venv\Scripts\Activate.ps1") {
        Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
        & "venv\Scripts\Activate.ps1"
    }
    
    Write-Host "📦 Installing requirements..." -ForegroundColor Yellow
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        Set-Location ..
        exit 1
    }
    
    Set-Location ..
} catch {
    Write-Host "❌ Dependency installation failed: $_" -ForegroundColor Red
    Set-Location ..
    exit 1
}

# Step 5: Database Setup
Write-Host ""
Write-Host "🗄️ Step 5: Database Setup" -ForegroundColor Blue
Write-Host "-------------------------"

try {
    if ($Reset) {
        Write-Host "⚠️ RESETTING DATABASE (all data will be lost)" -ForegroundColor Red
        $confirm = Read-Host "Type 'YES' to confirm database reset"
        if ($confirm -ne "YES") {
            Write-Host "❌ Database reset cancelled" -ForegroundColor Yellow
            exit 1
        }
        python setup_database.py --reset
    } else {
        python setup_database.py
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Database setup completed successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Database setup failed" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Database setup error: $_" -ForegroundColor Red
    exit 1
}

# Step 6: Verification
Write-Host ""
Write-Host "✅ Step 6: Setup Verification" -ForegroundColor Blue
Write-Host "-----------------------------"

try {
    # Test API health endpoint
    Write-Host "🔍 Testing API health..." -ForegroundColor Yellow
    
    # Start server in background for testing
    $serverJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        Set-Location backend
        python server_v2.py
    }
    
    # Wait a moment for server to start
    Start-Sleep -Seconds 5
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -TimeoutSec 10
        if ($response.status -eq "healthy") {
            Write-Host "✅ API health check passed" -ForegroundColor Green
            Write-Host "✅ Database connection verified" -ForegroundColor Green
        } else {
            Write-Host "⚠️ API responded but status unclear" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠️ Could not verify API (server may need manual start)" -ForegroundColor Yellow
    }
    
    # Stop the test server
    Stop-Job $serverJob -ErrorAction SilentlyContinue
    Remove-Job $serverJob -ErrorAction SilentlyContinue
    
} catch {
    Write-Host "⚠️ Verification had issues: $_" -ForegroundColor Yellow
}

# Success Summary
Write-Host ""
Write-Host "🎉 HackSky Database Setup Complete!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Start the backend server:" -ForegroundColor White
Write-Host "      cd backend" -ForegroundColor Gray
Write-Host "      python server_v2.py" -ForegroundColor Gray
Write-Host ""
Write-Host "   2. Start the frontend (in new terminal):" -ForegroundColor White
Write-Host "      npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "🔗 Important URLs:" -ForegroundColor Cyan
Write-Host "   • Backend API: http://localhost:5000" -ForegroundColor White
Write-Host "   • API Health: http://localhost:5000/api/health" -ForegroundColor White
Write-Host "   • Database Admin: http://localhost:8080" -ForegroundColor White
Write-Host "   • Frontend: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "🛠️ Management Commands:" -ForegroundColor Cyan
Write-Host "   • Reset database: .\setup_hacksky_database.ps1 -Reset" -ForegroundColor Gray
Write-Host "   • Stop containers: docker-compose down" -ForegroundColor Gray
Write-Host "   • View logs: docker-compose logs mysql" -ForegroundColor Gray
Write-Host ""
Write-Host "📊 Database Credentials:" -ForegroundColor Cyan
Write-Host "   • Host: localhost:3306" -ForegroundColor Gray
Write-Host "   • Database: ics_monitoring" -ForegroundColor Gray
Write-Host "   • Username: hacksky" -ForegroundColor Gray
Write-Host "   • Password: mysecretpassword" -ForegroundColor Gray
Write-Host ""

# Final instructions
Write-Host "🚀 Ready to launch HackSky with MySQL backend!" -ForegroundColor Green
Write-Host ""

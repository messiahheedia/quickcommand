#!/usr/bin/env pwsh
# PowerShell demo script for QuickCommand AI Assistant

Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                QuickCommand AI Assistant Demo                   ║" -ForegroundColor Cyan  
Write-Host "║                  Natural Language → Smart Commands              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "🧠 What QuickCommand Does:" -ForegroundColor Green
Write-Host "=========================="
Write-Host "QuickCommand translates natural language into precise PowerShell and Python commands."
Write-Host "It uses AI to understand what you want to do and suggests the right command syntax."
Write-Host ""

Write-Host "💡 Example Translations:" -ForegroundColor Yellow
Write-Host "========================"

$examples = @(
    @{
        Query = "command for remote group policy update"
        Command = "gpupdate /force"
        Description = "Force Group Policy update on local machine"
        Shell = "PowerShell"
    },
    @{
        Query = "list all running services"
        Command = "Get-Service | Where-Object {`$_.Status -eq 'Running'}"
        Description = "List all services with 'Running' status"
        Shell = "PowerShell"
    },
    @{
        Query = "check disk space on all drives"
        Command = "Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID,Size,FreeSpace"
        Description = "Display disk space information for all drives"
        Shell = "PowerShell"
    },
    @{
        Query = "install python package for web scraping"
        Command = "pip install requests beautifulsoup4"
        Description = "Install popular web scraping packages"
        Shell = "Python"
    },
    @{
        Query = "create a new directory and navigate to it"
        Command = "mkdir new_project; cd new_project"
        Description = "Create directory and change to it"
        Shell = "PowerShell"
    }
)

for ($i = 0; $i -lt $examples.Count; $i++) {
    $example = $examples[$i]
    Write-Host ""
    Write-Host "$($i + 1). " -NoNewline -ForegroundColor Cyan
    Write-Host "User says: " -NoNewline -ForegroundColor White
    Write-Host "`"$($example.Query)`"" -ForegroundColor Yellow
    Write-Host "   QuickCommand suggests: " -NoNewline -ForegroundColor White
    Write-Host "$($example.Command)" -ForegroundColor Green
    Write-Host "   Description: $($example.Description)" -ForegroundColor Gray
    Write-Host "   Shell: $($example.Shell)" -ForegroundColor Magenta
}

Write-Host ""
Write-Host "🔧 Available Shell Information:" -ForegroundColor Green
Write-Host "==============================="

# Check PowerShell
Write-Host ""
Write-Host "PowerShell:" -ForegroundColor Cyan
try {
    $psVersion = $PSVersionTable.PSVersion.ToString()
    Write-Host "  ✅ Available: True" -ForegroundColor Green
    Write-Host "  Version: $psVersion"
    Write-Host "  Edition: $($PSVersionTable.PSEdition)"
    Write-Host "  Platform: $($PSVersionTable.Platform)"
} catch {
    Write-Host "  ❌ Available: False" -ForegroundColor Red
}

# Check Python  
Write-Host ""
Write-Host "Python:" -ForegroundColor Cyan
try {
    $pythonVersion = & python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Available: True" -ForegroundColor Green
        Write-Host "  Version: $pythonVersion"
    } else {
        Write-Host "  ❌ Available: False (not in PATH)" -ForegroundColor Red
    }
} catch {
    Write-Host "  ❌ Available: False" -ForegroundColor Red
}

Write-Host ""
Write-Host "⚙️ Configuration Options:" -ForegroundColor Green
Write-Host "========================="
Write-Host "  AI Model: gpt-3.5-turbo (configurable)"
Write-Host "  Default Shell: PowerShell (configurable)"  
Write-Host "  Safety: Confirmation required before execution"
Write-Host "  Colors: Enabled for better UX"
Write-Host "  Clipboard: Copy commands without executing"

Write-Host ""
Write-Host "🚀 How to Get Started:" -ForegroundColor Green
Write-Host "======================"
Write-Host "  1. Ensure Python is installed and in PATH"
Write-Host "  2. Run setup.bat to install dependencies"
Write-Host "  3. Copy .env.example to .env"
Write-Host "  4. Add your OpenAI API key to .env"
Write-Host "  5. Run: python quickcommand.py"
Write-Host "  6. Start typing natural language commands!"

Write-Host ""
Write-Host "💬 Example Session:" -ForegroundColor Yellow
Write-Host "==================="
Write-Host "  ❯ " -NoNewline -ForegroundColor Blue
Write-Host "command for remote group policy update" -ForegroundColor White
Write-Host "  Thinking..." -ForegroundColor Yellow
Write-Host "  Suggested command: " -NoNewline -ForegroundColor Green
Write-Host "gpupdate /force" -ForegroundColor Cyan
Write-Host "  Description: Force Group Policy update" -ForegroundColor Yellow
Write-Host "  Execute this command? (y/n/copy): " -NoNewline -ForegroundColor Magenta
Write-Host "y" -ForegroundColor White
Write-Host "  Executing command..." -ForegroundColor Green
Write-Host "  Updating policy..." -ForegroundColor Gray

Write-Host ""
Write-Host "🎯 Perfect for:" -ForegroundColor Green
Write-Host "==============="
Write-Host "  • System administrators who know what they want but not the exact syntax"
Write-Host "  • Developers learning PowerShell or Python"
Write-Host "  • Anyone who wants to be more productive in the command line"
Write-Host "  • Teams who want to standardize command usage"
Write-Host "  • Learning new tools and commands through AI assistance"

Write-Host ""
Write-Host "Ready to try QuickCommand? Install Python and run setup.bat!" -ForegroundColor Green
Write-Host ""

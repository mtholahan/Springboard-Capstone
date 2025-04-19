# list_capstone_python_scripts.ps1
# Lists all Python scripts in the current script directory
# Saves the list to capstone_python_script_list.txt in the same folder

$scriptPath = "C:\Projects\Springboard_Capstone\scripts"
$outputFile = Join-Path $scriptPath "capstone_python_script_list.txt"

Get-ChildItem -Path $scriptPath -Filter *.py -File |
    Sort-Object Name |
    Select-Object Name |
    Out-File -FilePath $outputFile -Encoding UTF8

Write-Host "✅ Python script list saved to: $outputFile"

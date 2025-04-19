# list_capstone_data_files.ps1
# Recursively lists all folders and files in D:\Capstone_Staging\data
# Includes empty folders
# Outputs to: capstone_data_file_list.txt in the same directory

$sourcePath = "D:\Capstone_Staging\data"
$outputFile = Join-Path $sourcePath "capstone_data_file_list.txt"

$allItems = Get-ChildItem -Path $sourcePath -Recurse -Force -ErrorAction SilentlyContinue |
    Sort-Object FullName |
    Select-Object FullName

# Add base directories manually in case they have no contents
$allDirs = Get-ChildItem -Path $sourcePath -Recurse -Directory -Force |
    Where-Object { $_.GetFileSystemInfos().Count -eq 0 } |
    Select-Object FullName

$combined = ($allItems + $allDirs) | Sort-Object FullName -Unique
$combined | Out-File -FilePath $outputFile -Encoding UTF8

Write-Host "✅ Folder + file list saved to: $outputFile"

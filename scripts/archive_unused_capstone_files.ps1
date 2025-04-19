# archive_unused_capstone_files.ps1
# Moves unused or legacy files to D:\Capstone_Staging\archive for cleanup review

$basePath     = "D:\Capstone_Staging"
$dataPath     = Join-Path $basePath "data"
$archivePath  = Join-Path $basePath "archive"

# Make sure archive folder exists
New-Item -ItemType Directory -Path $archivePath -Force | Out-Null

# Files we plan to archive
$filesToArchive = @(
    "$dataPath\musicbrainz_raw\release_group_clean.tsv",
    "$dataPath\musicbrainz_raw\release_group_secondary_type_clean.tsv",
    "$dataPath\musicbrainz_raw\release_group_secondary_type_join_clean.tsv",
    "$dataPath\raw\Soundtracks_Master.csv"
)

# Directories that appear unused
$foldersToArchive = @(
    "$dataPath\processed"
)

# Move files
foreach ($file in $filesToArchive) {
    if (Test-Path $file) {
        Move-Item -Path $file -Destination $archivePath -Force
        Write-Host "📦 Moved file to archive: $file"
    } else {
        Write-Host "⚠️ File not found (already gone?): $file"
    }
}

# Move folders
foreach ($folder in $foldersToArchive) {
    if (Test-Path $folder) {
        $folderName = Split-Path $folder -Leaf
        Move-Item -Path $folder -Destination (Join-Path $archivePath $folderName) -Force
        Write-Host "📦 Moved folder to archive: $folder"
    } else {
        Write-Host "⚠️ Folder not found (already gone?): $folder"
    }
}

Write-Host "`n✅ Archiving complete. Review contents at: $archivePath"

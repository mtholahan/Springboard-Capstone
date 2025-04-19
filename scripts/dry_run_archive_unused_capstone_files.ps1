# dry_run_archive_unused_capstone_files.ps1
# Simulates moving unused or legacy files to D:\Capstone_Staging\archive
# Outputs what would be moved without making any changes

$basePath     = "D:\Capstone_Staging"
$dataPath     = Join-Path $basePath "data"
$archivePath  = Join-Path $basePath "archive"

# Files we plan to archive
$filesToArchive = @(
    "$dataPath\musicbrainz_raw\release_group_clean.tsv",
    "$dataPath\musicbrainz_raw\release_group_secondary_type_clean.tsv",
    "$dataPath\musicbrainz_raw\release_group_secondary_type_join_clean.tsv",
    "$dataPath\raw\Soundtracks_Master.csv"
)

# Folders that appear unused
$foldersToArchive = @(
    "$dataPath\processed"
)

Write-Host "🧪 DRY RUN: The following files/folders *would* be moved to ${archivePath}:`n"

# List files
foreach ($file in $filesToArchive) {
    if (Test-Path $file) {
        Write-Host "📁 FILE: $file"
    } else {
        Write-Host "⚠️  File not found (already gone?): $file"
    }
}

# List folders
foreach ($folder in $foldersToArchive) {
    if (Test-Path $folder) {
        Write-Host "📂 FOLDER: $folder"
    } else {
        Write-Host "⚠️  Folder not found (already gone?): $folder"
    }
}

Write-Host "`n✅ DRY RUN complete. No files were moved."

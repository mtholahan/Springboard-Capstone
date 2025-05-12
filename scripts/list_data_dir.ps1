$root = "D:\Capstone_Staging\data"

Get-ChildItem -Path $root -Recurse | ForEach-Object {
    [PSCustomObject]@{
        Type = if ($_.PSIsContainer) { "Folder" } else { "File" }
        Name = $_.Name
        RelativePath = $_.FullName.Replace($root + "\", "")
        SizeKB = if (-not $_.PSIsContainer) { "{0:N1}" -f ($_.Length / 1KB) } else { "" }
    }
} | Sort-Object Type, RelativePath | Format-Table -AutoSize

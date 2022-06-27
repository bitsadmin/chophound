param ([Parameter(Mandatory)]$File, [int]$ChunkSize=5000)

# Banner
"ChopHoundPS v1.0 ( https://github.com/bitsadmin/chophound/ )"

# Read file into memory
Write-Warning "Reading file $File"
$name_no_ext = [System.IO.Path]::GetFileNameWithoutExtension($File)
$js = Get-Content -Raw $File | ConvertFrom-Json

if(-not $?)
{
	Write-Warning "Error while reading file. Quitting."
	return
}

# Determine data tag name
$tagname = $js.meta.type
if($js.meta.version -gt 3)
    { $tagname = 'data' }

# Calculate number of blocks
$numblocks = [Math]::Ceiling($js.data.Count / $ChunkSize)
Write-Warning "Splitting in $numblocks blocks of $ChunkSize elements"
$i = 0

# Perform splitting
while($i*$ChunkSize -lt $js.data.Count)
{
    $outname = "{0}_{1:0000}.json" -f $name_no_ext,$i

    # meta -> count
    $meta = $js.meta
    $meta.count = $ChunkSize
    if(($i+1)*$ChunkSize -gt $js.data.Count)
        { $meta.count = $js.data.Count - ($i*$ChunkSize)}

    Write-Warning "Writing file $outname"
    
    # Meta tag MUST be after the data, otherwise BloodHound won't find it
    '{{"{0}":{1},"meta":{2}}}' -f `
        $tagname, `
        ($js.data[($i*$ChunkSize)..((($i+1)*$ChunkSize)-1)] | ConvertTo-Json -Depth 100 -Compress), `
        ($meta | ConvertTo-Json -Compress) `
        | Out-File $outname -NoNewline -Encoding UTF8BOM
    
    $i++
}
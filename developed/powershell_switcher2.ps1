

# key obtained via Get-AudioDevice -list
$headset = '{0.0.0.00000000}.{7d877137-3112-4359-a515-2c2176884542}'
$speakers = '{0.0.0.00000000}.{50db2424-6718-4e48-bae0-82d3b532f5c2}'


$headset_id = Get-AudioDevice -id $headset
# $default = Get-AudioDevice	-Playback // default device

if ($headset_id.default){
    Set-AudioDevice -id $speakers
    Write-Output 'Speakers Active'
}
else{
    Set-AudioDevice -id $headset
    Write-Output 'Headset Active'
}
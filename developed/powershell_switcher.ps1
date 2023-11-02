

# key obtained via Get-AudioDevice -list
$headset = '{0.0.0.00000000}.{7f65aae3-724e-4326-8a92-3c525dc21d20}'
$speakers = '{0.0.0.00000000}.{0e902266-6e9f-4561-a602-e90f51ff9971}'


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
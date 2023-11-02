            ###### Swapper.Core #######
            $headset = '{0.0.0.00000000}.{077d7e7d-06c9-41b0-adcc-763727e14c4d}'
            $speakers = '{0.0.0.00000000}.{436c68cf-f799-4595-ba61-d71dfb3468c0}'

            $headset_id = Get-AudioDevice -id $headset

            if ($headset_id.default) {
                Set-AudioDevice -id $speakers
                Write-Output 'Speakers Active'
            } else {
                Set-AudioDevice -id $headset
                Write-Output 'Headset Active'
            }
            
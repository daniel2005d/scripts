$path ='HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender\'


function disableav(){
New-ItemProperty $path -Name 'DisableAntiSpyware' -Value 0
}


$disabled = (Get-ItemProperty -Path $path -Name DisableAntiSpyware).DisableAntiSpyware

if ($disabled -eq $NULL){
    write-host "Not Exists"
    disableav
}
elseif ($disabled -eq 0) {
   write-host "Av are Disabled"
}
else {
   write-host "Disabling AV..." -foregroundcolor Green
   Set-ItemProperty -Path $path -Name DisableAntiSpyware -Value 0

}

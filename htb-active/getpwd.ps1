﻿function getpwd([string]$Cpassword){
$pl = $Cpassword.length % 4
if($pl -eq 0){$pad = ""}
else{$Pad = "=" * (4 - ($Cpassword.length % 4))}
$Base64Decoded = [Convert]::FromBase64String($Cpassword + $Pad)
#Create a new AES .NET Crypto Object
$AesObject = New-Object System.Security.Cryptography.AesCryptoServiceProvider
#Static Key from http://msdn.microsoft.com/en-us/library/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be%28v=PROT.13%29#endNote2
[Byte[]] $AesKey = @(0x4e,0x99,0x06,0xe8,0xfc,0xb6,0x6c,0xc9,0xfa,0xf4,0x93,0x10,0x62,0x0f,0xfe,0xe8,0xf4,0x96,0xe8,0x06,0xcc,0x05,0x79,0x90,0x20,0x9b,0x09,0xa4,0x33,0xb6,0x6c,0x1b)
#Set IV to all nulls (thanks Matt) to prevent dynamic generation of IV value
$AesIV = New-Object Byte[]($AesObject.IV.Length)
$AesObject.IV = $AesIV
$AesObject.Key = $AesKey
$DecryptorObject = $AesObject.CreateDecryptor()
[Byte[]] $OutBlock = $DecryptorObject.TransformFinalBlock($Base64Decoded, 0, $Base64Decoded.length)

return [System.Text.UnicodeEncoding]::Unicode.GetString($OutBlock)
}

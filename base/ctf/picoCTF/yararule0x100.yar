rule packed_YaraRules0x100 {
    meta:
        description = "Detects the packed version of YaraRules0x100 challenge"
    strings:
        $upx1 = "UPX!" ascii
        $upx2 = "UPX0" ascii
        $upx3 = "UPX1" ascii
        $str1 = "YaraRules0x100" ascii
        $str2 = "LoadLibrary" ascii
        $str3 = "VirtualProtect" ascii
    condition:
        uint16(0) == 0x5A4D and  // MZ header (PE file)
        any of ($upx*) and
        all of ($str*)
}

rule unpacked_YaraRules0x100 {
    meta:
        description = "Detects the unpacked version of YaraRules0x100 challenge"
    strings:
        $str1 = "Welcome to the YaraRules0x100 challenge!" ascii
        $str2 = "Suspicious" wide ascii
        $str3 = "picoCTF" wide ascii
        $str4 = "This is a fake malware." wide ascii
    condition:
        uint16(0) == 0x5A4D and
        all of them
}
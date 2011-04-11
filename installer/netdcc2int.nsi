
;--------------------------------

; The name of the installer
Name "Networked DCC to Intermediate Converter"

; The file to write
OutFile "netdcc2int.exe"

; The default installation directory
InstallDir $DESKTOP\netdcc2int

; Request application privileges for Windows Vista
RequestExecutionLevel user

;--------------------------------

; Pages

Page directory
Page instfiles

;--------------------------------

; The stuff to install
Section "" ;No components page, name is not important

  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Copy client
  SetOutPath $INSTDIR\client
  File /x *.pyc /x .git /x .gitignore ..\client\* 
  ; Copy server
  SetOutPath $INSTDIR\server
  File /x *.pyc /x .git /x .gitignore  ..\server\*
  ; Copy common
  SetOutPath $INSTDIR\common
  File /x *.pyc /x .git /x .gitignore  ..\common\*
  ; Copy third party
  SetOutPath $INSTDIR\third_party
  File /x *.pyc /x .git /x .gitignore  ..\third_party\nvdxt.exe
  ; Copy input drop
  SetOutPath $INSTDIR\input_drop
  File /x *.pyc /x .git /x .gitignore  ..\input_drop\README.TXT
  ; Copy output drop
  SetOutPath $INSTDIR\output_drop
  File /x *.pyc /x .git /x .gitignore  ..\output_drop\README.TXT


  
SectionEnd ; end the section

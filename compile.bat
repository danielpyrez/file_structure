@echo off

REM Empaqueta el script con PyInstaller
pyinstaller --onefile --console --icon=icon.ico --distpath="D:\Python Codes\File Structure\dist" file_structure.py

REM Pausa para ver mensajes de error o confirmación
pause

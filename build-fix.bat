@echo off
echo Cleaning previous builds...
rmdir /s /q dist 2>nul
rmdir /s /q node_modules\.cache 2>nul

echo Installing dependencies...
npm install

echo Building for Windows...
npm run build-win

echo Build complete! Check dist folder.
pause
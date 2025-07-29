@echo off
echo Installing electron-builder...
npm install electron-builder --save-dev

echo Building for all platforms...
npm run build-all

echo Build complete! Check the dist folder for executables.
pause
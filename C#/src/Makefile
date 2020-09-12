all:
	resources\MSBuild.exe
run:
	IVS\bin\Debug\Kalkulacka.exe
pack:
	resources\zip.exe -r src.zip ..\*
help:
	echo Makefile pro aplikaci Kalkulacka
	echo Makefile nepotrebuje pro praci zadne zavislosti, vse potrebne je obsazeno ve slozce resources
	echo Cil all preklada projekt Visual Studio 2017 pomoci utlity msbuild, predpoklada nainstalovany .NET Framework 4
	echo Cil run spusti aplikaci vytvorenou cilem 
	echo Cil pack zabali cely obsah adresare src do zip
	echo Cil clean smaze spustitelne a objektove soubory
clean:
	rmdir IVS\bin IVS\obj /S /Q
	rmdir "Smerodatna odhylka\bin" "Smerodatna odhylka\obj" /S /Q
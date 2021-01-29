# Prog_Solitaire

Prog projekt Pasziánsz

A pygame és a pygame_cards package-k segítségével készült. Jelenleg a futtatásához mindkét package-re szükség van.A projekt során alapvetően az internetre, a logikára és a package-ben található file-okra támaszkodtam.

A program futtatható Pythonban (Terminal) a pygame és a pygame_cards packagek jelenléte mellett. Ezzel párhuzamosan a program standalone verzióban is futtatható. Ehhez a mellékelt setup.py file-t kell futtatni.

## Setup.py

A mellékelt setup.py file macOS, Windows és (elvileg - ezt nem tudtam tesztelni) rendszereken is működőképes executable-t készít. Ehhez sajnos szükség van macOS esetén a py2app, windows esetén a py2exe extensionökre. (Nem sikerült self-bootstrapping telepítőt létrehoznom)

### Használat

#### macOS

Terminálban a következő parancs futtatása:

python3 setup.py py2app

#### Windows

CMD-ben/PowerShellben a következő parancs futtatása:

python3 setup.py py2exe

#### Futtatás
A parancs futtatását követően, ha minden elkészült, a program gyökérkönyvtárában megjelenik egy "dist" mappa. A setup ebben a mappában helyezi el az executable-t.

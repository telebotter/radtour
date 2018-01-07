# Radtour
Software rund um Radtour mit Website und Telegrambot

## Website - Django
Da wir das ganze auf Django aufbauen, ist es sinnvoll die Grundzüge und
Ordnerstrukturen von Django zu verstehen.

Unter der url https://tour.sarbot.de/ wird die website erreichbar sein. Auf dem
Server liegt das Projekt (dieses Repo) in `/home/django/tour/`. 

### Hintergrund
Für größere Webprojekte können verschiedene apps in unterordnern organisiert
werden, für uns reicht es vielleicht vorerst eine app `main/` zu verwenden. Im
Ordner `tour/` ist sozusagen die root-app darin liegt eine wsgi.py die beim
Aufruf jeder `tour.sarbot.de/*` url ausgeführt wird und die settings.py die
alle projekt-relevanten Einstellungen beinhaltet. Diese Datei enthält
unteranderem einen Token und andere sensible Informationen und sollte unbedingt
in der .gitignore stehen.

Im Projekt Ordner liegt eine manage.py das ist ein Script zur serverseitigen
Verwaltung des Projekts, damit können zum Beispiel neue apps erstellt oder
Datenbanktabellen geschrieben werden.

### Relevant
Inhalte werden entweder statisch (Bilder, PDFs, ggf. Tracks etc) im Ordner `statics/` 
abgelegt, oder als dynamische Daten in die Datenbank db.sqllite3 (ebenfalls in
.gitignore) geschrieben. Die Datenbank verwaltung funktioniert dabei ähnlich
wie bei sqalchemy, über model klassen in der models.py. Diese Models sind sehr
mächtig, da django damit ne menge geilen scheiß machen kann, zB admin Seiten
mit autmatisch generierten Formularen um Einträge zu bearbeiten... 

Jeder durch UrLs aufgerufenen Seite wird eine Python Funktion in `views.py`
zugeordnet. In der URL können auch direkt Paramter für die Funktion stehen.
Welche URLs wie mit den Funktionen verknüpft sind steht in den `urls.py`.
In den Funktionen/Views kommuniziert man mit der Datenbank und gibt das
Resultat (alle infos die angezeigt werden sollen) zusammen mit einem Layout
(html Template, in dem die Infos an den entsprechenden Stellen mit ensprechendem
Design eingefügt werden) an den Nutzer zurück.

Diese models können genauso von externen python programmen importiert und
verwendet werden so können daten App übergreifend gespeichert werden, zB für
den Telegram Bot. 

## Telegram Bot
Theoretisch würde eine bot.py im Projektverzeichnis reichen, aber da ich davon
ausgehe, das wir irgendwann eh zusätzliche Dateien zum auslagern anlegen
werden, habe ich direkt ein Ordner erstellt: `telebot/`.


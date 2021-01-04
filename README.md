## Appunti sul Rasptank della Adeept

Attenzione: tutte le informazioni sono seguenti rivestono carattere di **appunti personali** per cui potrebbero essere sbagliati: non faccio affermazioni sicure ma deduzioni che ho fatto leggendo schemi e codici.

### Funzionamento di base

Lo script python di setup crea un file bash chiamato `startup.sh` in `/home/pi`. In tale file viene richiamato l'interprete python che esegue il file `/home/pi/adeept_rasptank/server/webServer.py`. Il file bash verrà richiamato sempre all'avvio del sistema dal momento che viene inclusa la chiamata in `rc.local` (contenuto in `etc/`). 

> Per ulteriori informazioni su come si crea uno script di avvio si può fare riferimento a [questo mio appunto](https://github.com/Cyb3rn0id/TIL/blob/master/raspberry/eseguire_script_python_avvio.md).

Lo script `webServer.py` avvia un socket Flask sulla porta 5000 che permette una comunicazione bidirezionale tra client (il nostro browser) e server (che gira sul ROV). Tutta la roba che il socket Flask deve servire all'utente su richiesta http si trova nel file `/server/app.py`. Quando ci colleghiamo alla porta `5000` dell'indirizzo IP del nostro Raspberry Pi (es.: <kbd>http://192.168.1.13:5000</kbd>) viene servita la pagina `/server/dist/index.html`.

> Un tutorial interessante su come eseguire uno streaming utilizzando Flask si trova [qui](https://www.twilio.com/docs/voice/tutorials/consume-real-time-media-stream-using-websockets-python-and-flask).

In tale pagina HTML non c'è praticamente nulla perchè tutta l'interfaccia è realizzata dal javascript che si trova in `/server/dist/js/app.js` (`app.75ae363b.js` nel repository originale della Adeept). Tale Javascript che genera l'interfaccia è realizzato con [vue.js](https://vuejs.org/) e Adeept ha anche messo a disposizione i [sorgenti nel suo forum](https://www.adeept.com/forum/forum.php?mod=viewthread&tid=280). 

> E' possibile lavorare con vue.js anche da [Visual Studio](https://docs.microsoft.com/it-it/visualstudio/javascript/quickstart-vuejs-with-nodejs?view=vs-2019)  

La comunicazione tra il javascript e gli script python avviene tramite websocket mediante lo script `server.py`su diverse porte (`10123` per motori/servo, `2256` per inviare le informazioni CPU/RAM). Lo script `server.py` gestisce tutta la parte di ricetrasmissione delle informazioni inviate tramite websocket tra Javascript e Python. I file di test, non realmente utilizzati dall'applicazione, li ho rinominati mettendo un underscore prima del nome.

> Il programma non parte se non è collegato l'HAT dal momento che la prima cosa che viene fatta è portare i servocomandi in posizione di default per cui se non c'è comunicazione verso il PCA9685 viene sollevata un'eccezione e il programma si arresta. Dopo di ciò viene avviato il server con Flask che prova ad avviare pr prima cosa la telecamera, se la telecamera non è collegata o non c'è comunicazione, il programma si arresta. A tal proposito, se si verificano problemi con la telecamera, seguite questi [miei appunti](https://github.com/Cyb3rn0id/TIL/blob/master/raspberry/test_raspberry_pi_camera.md). 

Per fare modifiche _rapide_ all'interfaccia è possibile modificare il file Javascript. Io ho utilizzato [beautifier](https://beautifier.io/) per poter aggiungere nuovamente spazi e tabulazioni che, per questioni di compressione, vengono eliminati nei files originali (togliendo tutti i caratteri inutilizzati si velocizza il caricamento del Javascript dato che se ne riduce la dimensione anche di oltre il 50%). In questo modo i files diventano più leggibili ed è più agevole lavorarci.

Nelle cartelle `originals` di questo repository, all'interno di ogni sotto-cartella, sono contenuti i files originali della Adeept. Il readme originale della Adeept, con le istruzioni per l'installazione, l'ho rinominato in [adeept_readme.md](adeept_readme.md).  

Ho eliminato tutti i files inutilizzati e rinominato quelli utilizzati. L'interfaccia web è tutta contenuta nella cartella `/server/dist/`.  
I Files realmente utilizzati per la generazione dell'interfaccia, nel repository originale della Adeept (al commit [f4a9dab](https://github.com/adeept/Adeept_RaspTank/commit/f4a9dab2d65206cc856a4dcdd2033425fb3de9b5) del 10 Settembre 2020), sono questi:  

- `/css/app.ab2c2e5d.css`
- `/css/chunk-vendors.a639f090.css`
- `/js/app.75ae363b.js`
- `/js/chunk-vendors.3007e197.js`

In particolare l'interfaccia è generata dal file `app.ab2c2e5d.js`. Ho rinominato tale file eliminando la stringa esadecimale tra nome file ed estensione (che probabilmente identifica la versione del file) sempre per snellire la lettura: il file nel mio repository si chiama quindi `app.js`. Allo stesso modo ho rinominato gli altri files. Nel file `/server/dist/index.html`, che viene caricato alla richiesta del browser, ho quindi fatto riferimento ai nuovi nomi di files.  

### Indicazione RAM e CPU

L'indicazione di RAM e CPU è contenuta nelle righe da `470` a `472` di `app.js` ed è così strutturata:
```
["CPU", "Temp", 50, "°C", 55, 70],
```
- `"CPU"`: etichetta mostrata
- `"Temp"`: etichetta mostrata
- `50`: valore di default, mostrato al caricamento in attesa che lo script python restituisca il valore
- `"°C"`: unità di misura
- `55`: sotto questo valore, l'etichetta assume sfondo di colore verde 
- `70`: sotto questo valore, l'etichetta assume sfondo di colore arancione, da questo valore compreso in su, l'etichetta assume sfondo di colore rosso

Questi valori vengono richiesti dal javascript allo script python, mediante websocket, passando il valore `get_info` (riga `496` di `app.js`). Lo script `webServer.py` rileva tale valore a riga `435` e prepara i valori da passare mediante la funzione `info_get()` (si, si chiama al contrario rispetto al valore passato) definita in `server.py` a riga `219`, che sfrutta le funzioni definite in `info.py`. Infine `webServer.py` ritorna un array che viene rilevato da `app.js` a riga `485`, con il quale compila le etichette mostrate sull'interfaccia. 

### Tasti movimento

Nel file `app.js` i tasti per eseguire le funzioni sono definiti, ad esempio, in questo modo:
```
[!0, "mdi-arrow-up-thick", "backward", 87, "DS"]
```
- `!0` : (ovvero `true`) non so a cosa serve questo flag
- `"mdi-arrow-up-thick"` : descrizione che compare sul tasto (in questo caso freccia in alto, altri tasti hanno una descrizione estesa)
- `"backward"` : nome della funzione (inviata a `webServer.py`) da eseguire alla pressione del tasto (es.: _muovi il servo_)
- `87` : codice _ASCII_ del tasto sulla tastiera del PC associata al tasto 
- `DS` : nome della funzione (richiamata in _webServer.py_) da eseguire al rilascio del tasto (es.: _ferma il movimento del servo_)

I comandi del braccio e del movimento della telecamera si trovano nelle righe di `app.js` da `664` a `671`, ho cambiato le lettere associate mettendone di più congeniali per me e cambiando soprattutto il comando `handdown`, che era associato al codice ascii `186` che per quelli della Adeept era il tasto <kbd>;</kbd>, mentre per me non funzionava. Nel paragrafo successivo ho fatto una tabella con le modifiche che ho fatto.

> Per esperienza direi che è bene non utilizzare codici ASCII superiori al `127` dal momento che non sono gestiti in maniera uguale per tutte le culture.

### Servocomandi

I servocomandi sono gestiti in _I2C_ mediante il circuito integrato [PCA9685](https://www.nxp.com/products/power-management/lighting-driver-and-controller-ics/ic-led-controllers/16-channel-12-bit-pwm-fm-plus-ic-bus-led-controller:PCA9685) che nasce per il controllo in _PWM_ dei led ma è in realtà in grado di generare segnali _PWM_ utilizzabili anche con i servocomandi e viene utilizzata una libreria [Adafruit](https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython) per tale scopo (<kbd>Adafruit_PCA9685</kbd>).

Le funzioni che muovono i servocomandi sono contenute in `RPIservo.py` e richiamate da `webServer.py` nella funzione `robotCtrl()` a partire da riga `232`. Quando si muove il braccio in avanti o indietro, due servocomandi (quelli collegati a <kbd>12</kbd> e <kbd>13</kbd>) vengono gestiti insieme per fare in modo che la parte terminale della pinza (mossa dal servocomando <kbd>13</kbd>) sia sempre parallela al suolo. Non è quindi possibile, ad esempio, estendere il braccio completamente in verticale.

Nella seguente tabella ho riportato alcune informazioni sui servocomandi indicando i comandi originali della Adeept e come li ho ridefiniti in `app.js`:

| Comando                         | Nome funzione | Servocomando | Tasto originale (ASCII) | Tasto nuovo (ASCII) |
|---------------------------------|---------------|--------------|-------------------------|---------------------|
| Apri pinza                      | loose         | 15           | O (79)                  | O (79)              |
| Chiudi pinza                    | grab          | 15           | U (85)                  | P (80)              |
| Telecamera in alto              | up            | 11           | I (73)                  | R (82)              |
| Telecamera in basso             | down          | 11           | K (75)                  | F (70)              |
| Ruota pinza in senso antiorario | lookleft      | 14           | J (74)                  | K (75)              |
| Ruota pinza in senso orario     | lookright     | 14           | L (76)                  | L (76)              |
| Piega braccio in avanti         | handdown      | 12 e 13      | (186)                   | N (78)              |
| Piega braccio all'indietro      | handup        | 12 e 13      | P (80)                  | M (77)              |

Si consiglia di non utilizzare i tasti sull'interfaccia per il movimento ma le lettere sulla tastiera: capita infatti che a volte i tasti sull'interfaccia si blocchino e il servocomando non si ferma, ma questo potrebbe essere un problema che ho soltanto io e magari dipendente dal PC o dal browser utilizzato.

### Motore

I comandi del movimento del robot sono contenuti nelle righe di `app.js` da `745` a `747` e le funzioni definite in `move.py`. I tasti per il movimento in avanti e indietro a me risultavano invertiti nonostante abbia seguito scrupolosamente le istruzioni di montaggio, mentre il movimento a destra e sinistra era giusto: se si fosse trattato di un batch diverso di motori mi sarei aspettato che fossero invertiti anche i movimenti destra/sinistra. Ad ogni modo nel forum della Adeept in molti hanno lamentato questo stesso identico comportamento. Nel forum dicono di aigre in `move.py` alle righe `22` e `23` mettendo `Dir_forward=1` anzichè `Dir_forward=0` e facendo allo stesso modo nella riga successiva per la direzione opposta. In realtà così facendo si aggiusta il movimento avanti/indietro ma si inverte quello destra/sinistra. Per tale motivo ho deciso di lasciare inalterato `move.py` e agire invece in `app.js` invertendo le funzioni `forward` e `backward` a riga `745` e `746`.

In `move.py` a riga `31` c'era scritto `pwn_A=0` anzichè `pwm_A=0`, questo non causava nessun problema ma ho corretto lo stesso.

Viene utilizzato il classico ponte H _L298N_ per il pilotaggio di potenza dei motoriduttori: il motore A (sinistro guardando il ROV dalla parte posteriore) è gestito dai GPIO 4 (Enable), 14 e 15 (pin1, pin2); il motore B (destro) è gestito dai GPIO 17 (Enable), 27 e 18 (pin1, pin2). 

La variazione della velocità viene eseguita mandando il segnale _PWM_ sul pin di Enable mentre la direzione di rotazione è gestita invertendo lo stato dei pin1 e 2 del motore. Il motore è quindi pilotato in modalità __Sign-Magnitude__ ovvero il cambio di direzione è gestito dall'inversione dei due pin del motore e la velocità variata con l'enable. I motori si spengono completamente portando tutti i pin a GND.

> La modalità __Locked Anti-Phase__, invece, prevede che sia direzione che velocità del motore siano determinati dal segnale PWM inviato, in opposizione di fase, sui due pin di controllo del motore (un PWM del 50% corrisponde a motori fermi, maggiore del 50% fa ruotare i motori in un verso, minore del 50% li fa ruotere nel verso opposto). L'enable consente invece di spegnere totalmente i motori per non fargli assorbire corrente.

### Modulo Ultrasuoni

Il Modulo ultrasuoni è collegato ai GPIO11 (trigger) e GPIO8 (echo). Le funzioni per gestirlo si trovano nello script `ultra.py`. In `server.py`, a riga `243`, c'è la funzione `ultra_send_client()` che serve ad inviare la distanza rilevata. Gli ultrasuoni vengono utilizzati quando il ROV viene messo in modalità automatica: a questo punto il controllo passa alla funzione `automaticProcessing` in `functions.py` (riga `179`)

### Leds

Le funzioni per il controllo dei led WS2818 sono contenute nello script `robotLight.py` (gli script `LED.py` e `LEDapp.py` sono script di test e non vengono usati dal programma principale).

In tale script è possibile notare che, oltre ai Leds pilotati tramite il GPIO12 (gestiti dalla libreria `rpi_ws281x`, il pin utilizzato è definito a riga `15`), sono inizializzati tre GPIO a partire da riga 31: GPIO5, GPIO6 e GPIO13. 

Su tali GPIO, da [schema elettrico dell'HAT](docs/schematic_AdeeptMotorShield_v2.pdf) sono collegati 3 led: rispettivamente LED0 (rosso), LED1 (verde) e LED2 (blu) che si accendono portando i GPIO a livello basso. Probabilmente negli altri prodotti Adeept, come la RPI Car, questi GPIO vengono utilizzati per pilotare le luci frontali (i fari) dato che sono presenti delle funzioni chiamate `frontLight`, `switch`, `set_all_switch_off`, `headLight` nonchè lo script `switch.py` che utilizzano tali GPIO.

Nello script `switch.py` è definita una funzione `switch(port, status)` in cui `port` da 1 a 3 identifica i GPIO 5,6,13 mentre `status` identifica 1=led spento, 0=led acceso. Un richiamo a questa funzione si trova anche in `webServer.py` a riga `128`

Nello script `robotLight.py` a riga `14` erano definiti 16 led anzichè 12: ho corretto anche se questo non comporta nulla.

All'inizio le funzioni di breathing led e police light mi funzionavano correttamente. Inspiegabilmente, dopo un po', hanno cominciato a non funzionare più: all'avvio la funzione del breathing mi faceva due lampeggi corretti dopodichè si interrompeva con il primo led che impazziva e il secondo led che lo seguiva con intensità minore mentre gli altri rimanevano fissi a blu. Avviando il webServer manualmente anzichè in automatico all'avvio, questo malfunzionamento non si presentava. Dopo vari tentativo ho risolto il problema aggiungendo un ritardo di 2 secondi all'avvio del `main` in `webServer.py`. 

### Line Following

Ci sono due modalità di line following: con i fotoaccoppiatori o con la visione artificiale.

I fotoaccoppiatori per il line tracking sono collegati ai GPIO 19 (destro), 16 (centrale) e 20 (sinistro). Lo script che li gestisce è `findline.py`. Il modulo line follower è fatto per rilevare una linea nera (spessa 1cm) su uno sfondo bianco e la sensibilità si può aggiustare agendo sul trimmer posto sul modulo. La modalità in questione si attiva premendo il tasto <kbd>TRACK</kbd> Line nel riquadro <kbd>ACTIONS</kbd> dell'interfaccia.

La modalità di line following con la visione artificiale si fa dal riquadro <kbd>CVFL Control</bkd> (che ho rinominato in _Line Following Visuale_) e si attiva premendo il tasto <kbd>START</kbd> ivi contenuto. 

Il tasto <kbd>COLOR</kbd> serve per switchare tra due modalità di ricerca linea: linea bianca su sfondo nero (default) o linea nera su sfondo bianco. La funzionalià di line follower visiva confronta due pixel adiacenti: i controlli <kbd>L1</kbd> e <kbd>L2</kbd> servono a definire la posizione dei due pixel. Il controllo <kbd>SP</kbd> regola la soglia di intervento per la virata: valori troppo piccoli possono fare in modo che il robot non si muova più. Quando viene attivata questa funzionalità, lo schermo diventa in bianco e nero.

### Indicazione carica batteria

La tensione risultante dalle 2 batterie messe in serie (8.4V) viene misurata mediante una serie di partitori resistivi e comparatori contenuti nell'LM324: quando tutti e 4 i led rossi (LED 6,7,8,9) sono accesi, le batterie sono completamente cariche (tensione maggiore di 7.6V, ovvero batterie con tensione a partire da 3.8V). Con un solo LED acceso le batterie vanno rimosse e ricaricate (batteria singola a 3V). 

Purtroppo sull'interfaccia web non c'è indicazione della carica. Si sarebbero potute utilizzare le 4 uscite dei comparatori che pilotano i led per triggerare 4 GPIO inutilizzati (ad esempio quelli dei connettori RGB che su questo modello di ROV non sono utilizzate) e dare indicazione di carica anche sull'interfaccia Web.

### Altro

Le istruzioni che compaiono sull'interfaccia sono contenute dalla riga `1290` di `app.js`, il nome <kbd>Controlli</kbd> che ho tradotto è utilizzato anche come segnaposto per le funzioni di espansione del menù, per cui è necessario cambiarlo anche in altre parti del codice altrimenti quella parte di interfaccia non viene visualizzata.

Sull'HAT sono disponibili altri due connettori denominati RGB1 e RGB2, pensati, probabilmente per collegare strisce di led RGB per le quali i colori vengono gestiti singolarmente.
Sul connettore RGB1 sono collegati (partendo da pin1): 3.3V, GPIO22, 23 e 24. Sul connettore RGB2: 3.3V, GPIO10, 9 e 25. La cosa strana è che un richiamo a questi pin è presente, commentato, in `findline.py` e personalmente ho pensato che in origine la Adeept abbia pensato di illuminare la linea da seguire in vari colori per misurare la riflessione di ogni colore e quindi riuscire anche a distinguere il colore della linea per eseguire varie funzioni. Fatto sta che questi 6 GPIO sono liberi e dotati di resistenze di pull-up.

### Note per i meno esperti

Ogni volta che si fa una modifica ai javascript, per poter apprezzare il cambiamento è necessario svuotare la cache del browser, chiuderlo, riaprirlo e ridigitare l'indirizzo, altrimenti il browser carica sempre il javascript presente nella cache e non vediamo nessun cambiamento.

Le modifiche ai files python da windows andrebbero fatte con delle precauzioni. Da Notepad++ selezionare queste opzioni:

- <kbd>Modifica > Converti carattere di fine linea > UNIX</kbd>
- <kbd>Visualizza > Simboli > Mostra spazi bianchi e tabulazioni</kbd>

Python sfrutta le indentazioni per distinguere i blocchi di codice (gli `IF`, ad esempio, non hanno, come in altri linguaggi di programmazione, un corrispondente `end if` nè sono racchiusi tra parentesi graffe: tutto quello che va in un blocco `IF` è indentato al di sotto di esso). 

Per indentare i blocchi utilizzare una serie di 4 spazi anzichè la tabulazione. In Notepad++, quando viene attivata la funzione illustrata poco prima, gli spazi bianchi verranno indicati con dei puntini arancioni, mentre le tabulazioni con una freccia lunga verso destra: se ci sono delle tabulazioni, eliminatele e sostituitele con spazi oppure sfruttare la funzione apposita di Notepad++ per convertitore le tabulazioni in spazi:

<kbd>Modifica > Operazioni sugli spazi > Converti TAB in spazi</kbd>

### Problemi vari sul Raspberry Pi

Io ho utilizzato un Raspberry Pi4 con 2Gb di RAM e una microSD da 16Gb eseguendo la mia installazione personalizzata che non rimuove alcuni programmi nè disattiva la scheda audio. 

Ho un repository in cui [ho appuntato varie esperienze](https://github.com/Cyb3rn0id/TIL/tree/master/raspberry) acquisite sul Raspberry. Volendo utilizzare una microSD più piccola (8GB) è necessario disinstallare il Wolfram Engine (che occupa circa 2GB) e LibreOffice (circa 310MB)
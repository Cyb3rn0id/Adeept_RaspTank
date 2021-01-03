## Appunti sul Rasptank della Adeept

Attenzione: tutte le informazioni sono seguenti rivestono carattere di appunti personali per cui potrebbero essere sbagliati: non faccio affermazioni sicure ma deduzioni che ho fatto leggendo schemi e codici.

### Funzionamento di base

Lo script python di setup crea un file bash chiamato _startup.sh_ in _/home/pi_. In tale file viene richiamato l'interprete python che esegue il file _/home/pi/adeept_rasptank/server/webServer.py_. Il file bash verrà richiamato sempre all'avvio del sistema dal momento che viene inclusa la chiamata in _rc.local_ (contenuto in _/etc_). 

> Per ulteriori informazioni su come si crea uno script di avvio si può fare riferimento a [questo mio appunto](https://github.com/Cyb3rn0id/TIL/blob/master/raspberry/eseguire_script_python_avvio.md).

Lo script _webServer.py_ avvia un socket Flask sulla porta 5000 che permette una comunicazione bidirezionale tra client (il nostro browser) e server (che gira sul ROV). Tutta la roba che il socket Flask deve servire all'utente si trova nel file _/server/app.py_. Quando ci colleghiamo alla porta 5000 dell'indirizzo IP del nostro Raspberry Pi (es.: _http://192.168.1.13:5000_) viene servita la pagina _/server/dist/index.html_.

> Un tutorial interessante su come eseguire uno streaming utilizzando Flask si trova [qui](https://www.twilio.com/docs/voice/tutorials/consume-real-time-media-stream-using-websockets-python-and-flask).

In tale pagina HTML non c'è praticamente nulla perchè tutta l'interfaccia è realizzata dal javascript che si trova in _/server/dist/js/app.js_ (_app.75ae363b.js_ nel repository originale della Adeept). Tale Javascript che genera l'interfaccia è realizzato con [vue.js](https://vuejs.org/) e Adeept ha anche messo a disposizione i [sorgenti nel suo forum](https://www.adeept.com/forum/forum.php?mod=viewthread&tid=280). 

> E' possibile lavorare con vue.js anche da [Visual Studio](https://docs.microsoft.com/it-it/visualstudio/javascript/quickstart-vuejs-with-nodejs?view=vs-2019).  

La comunicazione tra il javascript e gli script python avviene tramite websocket mediante lo script _server.py_ su diverse porte (10123 per motori/servo, 2256 per inviare le informazioni CPU/RAM). Lo script _server.py_ gestisce tutta la parte di ricetrasmissione delle informazioni inviate tramite websocket.

Per fare modifiche _rapide_ all'interfaccia è possibile modificare i files Javascript. Io ho utilizzato [beautifier](https://beautifier.io/) per poter aggiungere nuovamente spazi e tabulazioni che, per questioni di compressione, vengono eliminati nei files originali (togliendo tutti i caratteri inutilizzati si velocizza il caricamento del Javascript dato che se ne riduce la dimensione anche di oltre il 50%). In questo modo i files diventano più leggibili ed è più agevole lavorarci.

Nelle cartelle _originals_, all'interno di ogni sotto-cartella, sono contenuti i files originali della Adeept. Il readme originale della Adeept, con le istruzioni per l'installazione, l'ho rinominato in [adeept_readme.md](adeept_readme.md).  

Ho eliminato tutti i files inutilizzati e rinominato quelli utilizzati. L'interfaccia web è tutta contenuta nella cartella _/server/dist/_.  
I Files realmente utilizzati per la generazione dell'interfaccia, nel repository originale della Adeept (al commit [f4a9dab](https://github.com/adeept/Adeept_RaspTank/commit/f4a9dab2d65206cc856a4dcdd2033425fb3de9b5) del 10 Settembre 2020), sono questi:  

- _/css/app.ab2c2e5d.css_
- _/css/chunk-vendors.a639f090.css_
- _/js/app.75ae363b.js_
- _/js/chunk-vendors.3007e197.js_

In particolare l'interfaccia è generata dal file _app.js_. Ho eliminato la stringa esadecimale tra nome file ed estensione (che probabilmente identifica la versione del file) sempre per snellire la lettura. Nel file _/server/dist/index.html_, che viene caricato alla richiesta del browser, ho quindi fatto riferimento ai nuovi nomi di files.  

### Indicazione RAM e CPU

L'indicazione di RAM e CPU è contenuta nelle righe da 470 a 472 di _app.js_ ed è così strutturata:

    ["CPU", "Temp", 50, "°C", 55, 70],

- _"CPU"_: etichetta mostrata
- _"Temp"_: etichetta mostrata
- _50_: valore di default, mostrato al caricamento in attesa che lo script python restituisca il valore
- _"°C"_: unità di misura
- _55_: sotto questo valore, l'etichetta assume sfondo di colore verde 
- _70_: sotto questo valore, l'etichetta assume sfondo di colore arancione, da questo valore compreso in su, l'etichetta assume sfondo di colore rosso

Questi valori vengono richiesti dal javascript allo script python, mediante websocket, passando il valore _get_info_ (riga 496 di app.js). Lo script _webServer.py_ rileva tale valore a riga 435 e prepara i valori da passare mediante la funzione _info_get()_ definita in _server.py_ a riga 219, che sfrutta le funzioni definite in _info.py_. Infine _webServer.py_ ritorna un array che viene rilevato dal javascript (_app.js_) a riga 485, con il quale compila le etichette. 

### Tasti movimento

Nel file _app.js_ i tasti per eseguire le funzioni sono definiti, ad esempio, in questo modo:

    [!0, "mdi-arrow-up-thick", "backward", 87, "DS"]

- _!0_ : (true) non so
- _"mdi-arrow-up-thick"_ : descrizione che compare sul tasto (in questo caso freccia in alto, altri tasti hanno una descrizione estesa)
- _"backward"_ : nome della funzione (richiamata in _webServer.py_) da eseguire alla pressione del tasto (es.: muovi il servo)
- _87_ : codice ascii del tasto sulla tastiera del PC associata al tasto 
- _DS_ : nome della funzione (richiamata in _webServer.py_) da eseguire al rilascio del tasto (es.: ferma il movimento del servo)

I comandi del braccio e del movimento della telecamera si trovano nelle righe di _app.js_ da 664 a 671, ho cambiato le lettere associate mettendone di più congeniali per me e cambiando soprattutto il comando _handdown_, che era associato al codice ascii 186 che per quelli della Adeept era il tasto ";", mentre per me non funzionava. Nel paragrafo successivo ho fatto una tabella con le modifiche che ho fatto.

> Per esperienza direi che èbene non utilizzare codici ASCII superiori al 127 dal momento che non sono gestiti in maniera uguale per tutte le culture.

### Servocomandi

I servocomandi sono gestiti in I2C mediante il circuito integrato [PCA9685](https://www.nxp.com/products/power-management/lighting-driver-and-controller-ics/ic-led-controllers/16-channel-12-bit-pwm-fm-plus-ic-bus-led-controller:PCA9685) che nasce per il controllo in PWM dei led ma è in realtà in grado di generare segnali PWM utilizzabili anche con i servocomandi e viene utilizzata una libreria [Adafruit](https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython) per tale scopo (_Adafruit_PCA9685_).

Le funzioni che muovono i servocomandi sono contenute in _servo.py_ e gestite da _webServer.py_ nella funzione _robotCtrl()_ a partire da riga 232 (lo script _RPIservo.py_ non è utilizzato ed è di test). Quando si muove il braccio in avanti o indietro, due servocomandi (12 e 13) vengono gestiti insieme per fare in modo che la parte terminale della pinza (mossa dal servocomando 13) sia sempre parallela al suolo. Non è quindi possibile, ad esempio, estendere il braccio completamente in verticale.

Nella seguente tabella ho riportato alcune informazioni sui servocomandi indicando i comandi originali della Adeept e come li ho ridefiniti in _app.js_ come detto al paragrafo precedente:

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

I comandi del movimento del robot sono contenuti nelle righe di _app.js_ da 745 a 747 e le funzioni definite in _move.py_. I tasti per il movimento in avanti e indietro a me risultavano invertiti nonostante abbia seguito scrupolosamente le istruzioni di montaggio, mentre il movimento a destra e sinistra era giusto: se si fosse trattato di un batch diverso di motori mi sarei aspettato che fossero invertiti anche i movimenti destra/sinistra. Ad ogni modo nel forum della Adeept in molti hanno lamentato questo stesso identico comportamento. L'ho risolto semplicemente modificano in _move.py_ le righe 22 e 23 _Dir_forward=1_ anzichè _Dir_forward=0_ e così anche per la riga successiva.

Viene utilizzato il classico L298N per il pilotaggio di potenza dei motoriduttori: il motore A (sinistro guardando il ROV dalla parte posteriore) è gestito dai GPIO 4 (Enable), 14 e 15 (pin1, pin2); il motore B (destro) è gestito dai GPIO 17 (Enable), 27 e 18 (pin1, pin2). La variazione della velocità viene eseguita mandando il segnale PWM sul pin di Enable mentre la direzione di rotazione è gestita invertendo lo stato dei pin1 e 2 del motore. Il motore è quindi pilotato in modalità _Sign-Magnitude_ ovvero il cambio di direzione è gestito dall'inversione dei due pin del motore e la velocità variata con l'enable. I motori si spengono completamente portando tutti i pin a GND.

> La modalità _Locked Anti-Phase_ invece prevede che sia direzione che velocità del motore siano determinati dal segnale PWM inviato, in opposizione di fase, sui due pin di controllo del motore (un PWM del 50% corrisponde a motori fermi, maggiore del 50% fa ruotare i motori in un verso, minore del 50% li fa ruotere nel verso opposto). L'enable consente invece di spegnere totalmente i motori per non fargli assorbire corrente.

### Modulo Ultrasuoni

Il Modulo ultrasuoni è collegato ai GPIO11 (trigger) e GPIO8 (echo). Le funzioni per gestirlo si trovano nello script _ultra.py_. In _server.py_, a riga 243, c'è la funzione _ultra_send_client()_ che serve ad inviare la distanza rilevata ma in nè in _webSever.py_ nè in _app.js_ sono presenti funzioni per visualizzare la distanza sull'interfaccia web.

### Leds

Le funzioni per il controllo dei led WS2818 sono contenute nello script _robotLight.py_ (gli script _LED.py_ e _LEDapp.py_ sono script di test e non vengono usati dal programma principale).

In tale script è possibile notare che, oltre ai Leds pilotati tramite il GPIO12 (gestiti dalla libreria _rpi_ws281x_, il pin utilizzato è definito a riga 15), sono inizializzati tre GPIO a partire da riga 31: GPIO5, GPIO6 e GPIO13. Su tali GPIO, da [schema elettrico](docs/schematic_AdeeptMotorShield_v2.pdf) sono collegati 3 led: rispettivamente LED0 (rosso), LED1 (verde) e LED2 (blu) che si accendono portando i GPIO a livello basso. Le uniche istruzioni per pilotare questi 3 led si trovano soltanto in queste 3 righe: i led vengono accesi all'avvio dello script e basta.

### Modulo Line tracking

I fotoaccoppiatori per il line tracking sono collegati ai GPIO 19 (destro), 16 (centrale) e 20 (sinistro). Lo script che li gestisce è _findline.py_

### Indicazione carica batteria

La tensione risultante dalle 2 batterie messe in serie (8.4V) viene misurata mediante una serie di partitori resistivi e comparatori contenuti nell'LM324: quando tutti e 4 i led rossi (LED6,7,8,9) sono accesi, le batterie sono completamente cariche. Con un solo LED acceso le batterie vanno rimosse e ricaricate. Purtroppo sull'interfaccia non c'è indicazione della carica. Si sarebbero potute utilizzare le 4 uscite che pilotano i led per triggerare 4 GPIO inutilizzati e dare indicazione di carica anche sull'interfaccia Web.

### Altro

Le istruzioni che compaiono sull'interfaccia sono contenute dalla riga 1290 di _app.js_, il nome "Controlli" che ho tradotto è utilizzato anche come segnaposto per le funzioni di espansione del menù, per cui è necessario cambiarlo anche in altre parti del codice altrimenti quella parte di interfaccia non viene visualizzata.

Sull'HAT sono disponibili altri due connettori denominati RGB1 e RGB2, pensati, probabilmente per collegare strisce di led RGB per le quali i colori vengono gestiti singolarmente sul connettore RGB1 sono collegati (partendo da pin1): 3.3V, GPIO22, 23 e 24. Sul connettore RGB2: 3.3V, GPIO10, 9 e 25. La cosa strana è che un richiamo a questi pin è presente, commentato, in _findline.py_ e personalmente ho pensato che in origine la Adeept abbia pensato di illuminare la linea da seguire in vari colori per misurare la riflessione di ogni colore e quindi riuscire anche a distinguere il colore della linea per eseguire varie funzioni. Fatto sta che questi 6 GPIO sono liberi e dotati di resistenze di pull-up.

### Note

Ogni volta che si fa una modifica ai files, per poter apprezzare il cambiamento è necessario svuotare la cache del browser, chiuderlo, riaprirlo e ridigitare l'indirizzo, altrimenti il browser carica sempre il javascript presente nella cache e non vediamo nessun cambiamento.

### Problemi vari sul Raspberry.

Io ho utilizzato un Raspberry Pi4 da 2Gb di RAM e una microSD da 16Gb eseguendo la mia installazione personalizzata che non rimuove alcuni programmi nè disattiva la scheda audio. Ho un repository in cui [ho appuntato varie esperienze](https://github.com/Cyb3rn0id/TIL/tree/master/raspberry) acquisite sul Raspberry. Volendo utilizzare una microSD più piccola (8GB) è necessario disinstallare il Wolfram Engine (che occupa circa 2GB) e LibreOffice (circa 400MB)
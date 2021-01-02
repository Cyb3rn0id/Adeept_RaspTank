## Modifiche e appunti sul Rasptank della Adeept

L'interfaccia web di controllo del Robot è realizzata con [vue.js](https://vuejs.org/) e Adeept ha anche messo a disposizione i [sorgenti nel suo forum](https://www.adeept.com/forum/forum.php?mod=viewthread&tid=280). E' possibile lavorare con vue.js anche da [Visual Studio](https://docs.microsoft.com/it-it/visualstudio/javascript/quickstart-vuejs-with-nodejs?view=vs-2019).  

Per fare modifiche _rapide_ all'interfaccia è possibile modificare i files Javascript. Io ho utilizzato [beautifier](https://beautifier.io/) per poter aggiungere nuovamente spazi e tabulazioni che, per questioni di compressione, vengono eliminati nei files originali (togliendo tutti i caratteri inutilizzati si velocizza il caricamento del Javascript dato che se ne riduce la dimensione anche di oltre il 50%). In questo modo i files diventano più leggibili ed è più agevole lavorarci.

Nelle cartelle _originals_, all'interno di ogni sotto-cartella, sono contenuti i files originali della Adeept. Il readme originale della Adeept, con le istruzioni per l'installazione, l'ho rinominato in [adeept_readme.md](adeept_readme.md).  

Ho eliminato tutti i files inutilizzati e rinominato quelli utilizzati. L'interfaccia web è tutta contenuta nella cartella _/server/dist/_.  
I Files realmente utilizzati per la generazione dell'interfaccia, nel repository originale della Adeept (al commit [f4a9dab](https://github.com/adeept/Adeept_RaspTank/commit/f4a9dab2d65206cc856a4dcdd2033425fb3de9b5) del 10 Settembre 2020), sono questi:  

- /css/app.ab2c2e5d.css
- /css/chunk-vendors.a639f090.css
- /js/app.75ae363b.js
- /js/chunk-vendors.3007e197.js

In particolare l'interfaccia è generata dal file _app_. Ho eliminato la stringa esadecimale tra nome file ed estensione (che probabilmente identifica la versione del file) sempre per snellire la lettura. Nel file _/server/dist/index.html_ ho quindi fatto riferimento ai nuovi nomi di files.  

### Indicazione RAM e CPU

L'indicazione di RAM e CPU è contenuta nelle righe da 470 a 472 ed è così strutturata:

    ["CPU", "Temp", 50, "°C", 55, 70],

- _"CPU"_: etichetta mostrata
- _"Temp"_: etichetta mostrata
- _50_: valore di default, mostrato al caricamento in attesa che lo script python restituisca il valore
- _"°C"_: unità di misura
- _55_: sotto questo valore, l'etichetta assume sfondo di colore verde 
- _70_: sotto questo valore, l'etichetta assume sfondo di colore arancione, da questo valore compreso in su, l'etichetta assume sfondo di colore rosso

Questi valori vengono richiesti dal javascript allo script python, mediante websocket, passando il valore _get_info_ (riga 496 di app.js). Lo script _webServer.py_ rileva tale valore a riga 435 e ritorna un array che viene rilevato dal javascript a riga 485, con il quale compila le etichette

### Tasti movimento

Nel file _app.js_ i tasti per eseguire le funzioni sono definiti, ad esempio, in questo modo:

    [!0, "mdi-arrow-up-thick", "backward", 87, "DS"]

- _!0_ : (true) non so
- _"mdi-arrow-up-thick"_ : descrizione che compare sul tasto (in questo caso freccia in alto, altri tasti hanno una descrizione estesa)
- _"backward"_ : nome della funzione (richiamata in _webServer.py_) da eseguire alla pressione del tasto (es.: muovi il servo)
- _87_ : codice ascii del tasto sulla tastiera del PC associata al tasto 
- _DS_ : nome della funzione (richiamata in _webServer.py_) da eseguire al rilascio del tasto (es.: ferma il movimento del servo)

I comandi del braccio e del movimento della telecamera si trovano nelle righe di _app.js_ da 664 a 671, ho cambiato le lettere associate mettendone di più congeniali per me e cambiando soprattutto il comando _handdown_, che era associato al codice ascii 186 che per quelli della Adeept era il tasto ";", mentre per me non funzionava. 

>E' bene non utilizzare codici ASCII superiori al 127 dal momento che non sono renderizzati uguali per tutte le culture.

I servocomandi sono gestiti in I2C mediante il circuito integrato [PCA9685](https://www.nxp.com/products/power-management/lighting-driver-and-controller-ics/ic-led-controllers/16-channel-12-bit-pwm-fm-plus-ic-bus-led-controller:PCA9685) che nasce per il controllo in PWM dei led ma è in realtà in grado di generare segnali PWM utilizzabili anche con i servocomandi e viene utilizzata una libreria [Adafruit](https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython) per tale scopo.

Le funzioni che muovono i servocomandi sono contenute in _servo.py_ e gestite da _webServer.py_ nella funzione _robotCtrl_ a partire da riga 232. Quando si muove il braccio in avanti o indietro, due servocomandi vengono gestiti insieme per fare in modo che la parte terminale della pinza (servocomando 13) sia sempre parallela al suolo, non è quindi possibile, ad esempio, estendere il braccio completamente in verticale.

Nella seguente tabella ho riportato alcune informazioni sui servocomandi indicando i comandi originali della Adeept e come li ho ridefiniti:

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

I comandi del movimento del robot sono contenuti nelle righe di _app.js_ da 745 a 747 e le funzioni definite in _move.py_. I tasti per il movimento in avanti e indietro a me risultavano invertiti nonostante abbia seguito scrupolosamente le istruzioni di montaggio, mentre il movimento a destra e sinistra era giusto: se si fosse trattato di un batch diverso di motori mi sarei aspettato che fossero invertiti anche i movimenti destra/sinistra. Ad ogni modo nel forum della Adeept in molti hanno lamentato questo stesso identico comportamento. L'ho risolto semplicemente modificano in _move.py_ le righe 22 e 23 _Dir_forward=1_ anzichè _Dir_forward=0_ e così anche per la riga successiva.

>Ogni volta che si fa una modifica ai files, per poter apprezzare il cambiamento è necessario svuotare la cache del browser, chiuderlo, riaprirlo e ridigitare l'indirizzo, altrimenti il browser carica sempre il javascript presente nella cache e non vediamo nessun cambiamento.

### Altro

Le istruzioni sono contenute dalla riga 1290, il nome "Controlli" che ho tradotto è utilizzato anche come segnaposto per le funzioni di espansione del menù, per cui è necessario cambiarlo anche in altre parti del codice altrimenti quella parte di interfaccia non viene visualizzata.


### Problemi vari sul Raspberry.

Io ho utilizzato un Raspberry Pi4 da 2Gb e una microSD da 16Gb eseguendo la mia installazione personalizzata che non rimuove alcuni programmi nè disattiva la scheda audio. Ho un repository in cui [ho appuntato varie esperienze](https://github.com/Cyb3rn0id/TIL/tree/master/raspberry) acquisite sul Raspberry.
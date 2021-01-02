L'interfaccia web di controllo del Robot è realizzata con vue.js e adeept ha anche messo a disposizione i [sorgenti nel suo forum](https://www.adeept.com/forum/forum.php?mod=viewthread&tid=280).  
Per fare modifiche rapide all'interfaccia è possibile modificare i files Javascript utilizzando un servizio come quello offerto da [beautifier](https://beautifier.io/) per poter aggiungere nuovamente spazi e tabulazioni che, per questioni di compressione, sono stati eliminati nei files originali (togliendo tutti i caratteri inutilizzati si velocizza il caricamento del Javascript dato che se ne riduce la dimensione anche di oltre il 50%).  

Nelle cartelle _originals_, all'interno di ogni sotto-cartella, sono contenuti i files originali della Adeept.  
Ho eliminato tutti i files inutilizzati e rinominato quelli utilizzati. L'interfaccia web è tutta contenuta nella cartella _/server/dist/_.  
I Files realmente utilizzati per la generazione dell'interfaccia sono questi:  

- /css/app.ab2c2e5d.css
- /css/chunk-vendors.a639f090.css
- /js/app.75ae363b.js
- /js/chunk-vendors.3007e197.js

In particolare l'interfaccia è generata dal file _app_. Ho eliminato la stringa esadecimale tra nome file ed estensione (che probabilmente identifica la versione del file) sempre per snellire la lettura e il contenuto della cartella. Nel file _/server/dist/index.html_ ho quindi fatto riferimento ai nuovi files.  

Nel file _app.js_ i tasti per eseguire le funzioni sono definiti, ad esempio, in questo modo:

    [!0, "mdi-arrow-up-thick", "backward", 87, "DS"]

- _!0_ : (true) non so
- _"mdi-arrow-up-thick"_ : descrizione che compare sul tasto (in questo caso freccia in alto, altri tasti hanno una descrizione estesa)
- _"backward"_ : nome della funzione (richiamata in _webServer.py_) da eseguire alla pressione del tasto (es.: muovi il servo)
- _87_ : codice ascii del tasto sulla tastiera del PC associata al tasto 
- _DS_ : nome della funzione (richiamata in _webServer.py_) da eseguire al rilascio del tasto (es.: ferma il movimento del servo)
 
I comandi del braccio e del movimento della telecamera si trovano nelle righe da 664 a 671, ho cambiato le lettere associate mettendone di più congeniali per me e cambiando soprattutto il comando _handdown_, che era associato al codice ascii 186 che per quelli della Adeept era il tasto ";", mentre per me non funzionava.
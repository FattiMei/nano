# Gcode validation -- Specifica
Analisi a priori di un file gcode. Si vuole avere la certezza che un tal file gcode non sia dannoso per la propria macchina ancor prima di eseguirlo.


# Specifica gcode
Un file gcode è una file di testo che contiene commenti e comandi separati da spazi e newline.


## Encoding
ASCII (?)


## Commenti
  `;.*$`

I commenti sono ignorati dal firmware. Eliminare i commenti da un file gcode non ha effetto semantico, ma potrebbe beneficiare le prestazioni (vedi sezione "Troppi commenti").


## Newline
NL (preferito) oppure NL + CR


## Token
  `[FGMSXYZ](0|-?[1-9][0-9]*)(.[0-9]+)?`

Chiameremo *tipo* il primo carattere di ogni token e *valore* il numero immediatamente successivo.
Si individuano due classi di token in base al tipo:
  . Istruzioni: [GM]
  . Parametri: [FSXYZ]


## Linea
Ogni linea di gcode che non sia vuota, privata degli eventuali commenti, contiene un'instruzione seguita da zero o più parametri, separati da spazi. Ogni istruzione specifica quanti e quali parametri accettare. L'ordine dei parametri è irrilevante (?).


# 1001 modi per rompere la macchina
## Errori sintattici
Se la macchina riceve dei comandi sintatticamente errati a seconda del firmware potrebbe:

  * Ignorare i successivi comandi fino alla successiva linea corretta, con conseguente perdita di informazioni
  * Abortire l'esecuzione del programma


## Istruzioni non implementate dalla macchina
L'esecuzione di un'istruzione non supportata è *undefined behavior*


## Errori di floating point
Quando il valore di un token non è rappresentabile nel tipo float della macchina.


## Troppi commenti
Sebbene i commenti non siano rilevanti, la loro massiccia presenza potrebbe rallentare le operazioni di esecuzione delle istruzioni, ricordo che operiamo in un contesto di real-time application.


## Vincoli spaziali della macchina
Le istruzioni gcode potrebbero portare la macchina fuori dal volume di lavoro.


## Feed rate
Il feed rate per le istruzioni di movimento specifica la velocità della toolhead. Ogni macchina, in base al tipo di motori utilizzati e alla tecnologia di movimento, ammette una velocità massima oltre la quale è pericoloso operare.


## Temperature di utilizzo
Nel caso di stampanti 3d l'estrusione di filamento è instrinsecamente legata alla temperatura di esercizio. Tentare di estrudere materiale da una hotend fredda causa otturazioni dell'estrusore.


## Collisione con oggetti nel volume di stampa
(Per utenti esperti) La macchina potrebbe lavorare in presenza di oggetti esterni nel volume di lavoro, si verifica che non ci siano collisioni con questi.

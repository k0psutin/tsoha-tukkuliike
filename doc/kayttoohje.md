# Käyttöohjeet

### Heroku

Sovellus löytyy herokusta osoitteesta:

[https://sheltered-temple-19572.herokuapp.com/](https://sheltered-temple-19572.herokuapp.com/)

Sovelluksen aukeamisessa voi kestää hetken, jos sovelluksessa ei ole lähiaikoina käyty.

### Käyttäjätunnukset:

<br>
    
Logistiikka: `varasto/1234`  
Keräily: `keraily/1234`  
Osto: `osto/1234`  
Myynti: `myynti/1234`  
Kontrolleri: `admin/1234`  
Asiakas: `asiakas/1234`

<br>

Jokaisella tunnuksella on oma näkymä sekä omat toiminnot. Näkymissä on myös painikkeet `back` ja `logout`, millä voidaan palata edelliselle sivulle tai kirjautua ulos.

Mikäli ei jaksa kirjautua tunnuksilla edestakaisin, voi kirjautua sisään kontrollerin tunnuksilla. Kontrollerilla on pääsy joka näkymään.

Alapuolelta löytyvät ohjeet näkymien toimintoihin.

## Varasto

### Supply order list (aukeaa sisäänkirjautuessa)

Virtuaalinäkymä simuloi fyysisiä saapuvia tavaroita, ja näet siitä helposti esimerkiksi tilausnumeron `order_id` taikka tuotteen kappalemäärän `qty`.

Saapuvia tavaroida voidaan siirtää tukun varastoon syöttämällä tilauksen `order_id`, sekä kappalemäärä `qty` lomakkeeseen ja painamalla `send`.

Esimerkki:

```
Virtual view of supply orders

Order id  Supplier id   Supplier name   Countrycode   Order date   Item id  Item name  Item qty
2838343       19          Tiilipojat         FI    2019-10-08 15:03   3       Tiili       30

Logistics

Create new batch

Order id: 2838343
Quantity: 30
Send
```

```
Batch TI20191008FI created succesfully.
```

Järjestelmä ilmoittaa onnistumisesta (tai epäonnistumisesta) ilmoituksella.

Huom. Saapuneita tuotteida voidaan siirtää tukun varastoon enemmän kuin mitä on "ilmoitettu" tuotemäärässä. Tämä johtuu siitä, että tuotteita voi saapua enemmän (virhelasku) kuin on tilattu.

### Supply order inventory

Tässä näkymässä voidaan muuttaa saapuvien tuotteiden inventaarion määriä.

Saapuvaa tavaraa vastaanotettaessa huomataan, että tilattu määrä ja saapunut määrä poikkeaa toisistaan: Varastosiirron jälkeen tiiliä jäi tilaukseen vielä 5 kpl.

Esimerkki:

```
Virtual view of supply orders

Order id  Supplier id Supplier name  Countrycode   Order date   Item id  Item name  Item qty
2838343       19        Tiilipojat       FI    2019-10-08 15:03   3       Tiili       5
```

Päivitetään tuotetilauksen määrä nollaan:

```
Update order quantity

Order id: 2838343
Quantity: 0
Send
```

Lähetyksen jälkeen, järjestelmä ilmoittaa onnistuneesta päivityksestä, ja tuotetilaus häviää listauksesta.

```
Supply order 3874611 quantity updated.
```

### Batch inventory

Tässä näkymässä voidaan muuttaa tukun inventaarion määriä.

Esimerkki:

```
Virtual view of batches

----------------------------------------------------------
  Batch nr.       Company id        Quantity       Date
 TI180220FI         Tiili             100       2020-02-18
-----------------------------------------------------------
```

Nähdään, että inventaari näyttää että tiiliä on 100kpl, vaikka (hypoteettisesti) fyysisiä kappaleita löytyi 101kpl.

```
Update batch quantity

Batch nr: TI180220FI
Quantity: 101
Send
```

Täytetään eränumero, oikea määrä ja lähetetään tieto.

```
Batch TI180220FI quantity updated.
Update batch quantity

Batch nr:
Quantity:
Send
```

Viesti kertoo päivityksen onnistumisesta, ja huomataan, että inventaari näyttää myös 101kpl.

```
Virtual view of batches

----------------------------------------------------------
  Batch nr.       Company id        Quantity       Date
 TI180220FI         Tiili             101       2020-02-18
-----------------------------------------------------------
```

Tukun inventaari valmis.

Jos tuotetta ei löydy, voidaan määräksi syöttää 0 kappaletta, jolloin erä häviää listauksesta.

## Keräily

Virtuaalinäkymä simuloi tukun varastosaldoilla olevia tuotteita. Tuotteista on esillä eränumero (`batch_nr`), tuotteen nimi (`item name`) sekä määrä (`qty`) ja kirjauspäivämäärä (`date`).

Tilauksiin kerätään tavaroita, avaamalla `open orders` -osiosta jokin tilaus.

Tilausta klikattaessa tilaustiedot aukeavat näytölle, ja näet mitä tuotteita tilaus pitää sisällään.

Tuotteita "kerätään" kirjoittamalla (tai kopioimalla) `batch_nr` sekä kappalemäärä `qty` lomakkeeseen. Tämän jälkeen tuote vahvistetaan kerätyksi painamalla kohtaa `collect`.

Kun kaikki tuotteet ovat kerätty, voidaan tilaus merkitä valmistuneeksi painamalla kohdasta `complete shipment`.

Esimerkki:

```
Order id: 1239412 - Company: Pamlab - Route 5 - Qty: 20 - Order date 2020-09-09
```

Klikataan tilausta jolloin aukeaa tilauksen tiedot:

```
Order 123145 details

  item name         remaining qty   collected qty
    Tiili              10              0
```

Huomataan, että virtuaalinäkymässä näkyy saldoilla olevan tiiliä:

```
    Batch nr.       item name       qty     date
 TL030920FI         Tiili           100     2020-09-08
```

Syötetään eränumero ja tarvittavat määrät lomakkeeseen:

```
Collect item

Batch nr: TL030920FI
Collected: 10
Collect
```

Kun tuotteet ovat kerätty, päivittyy myös tilaustiedot:

```
Order 123145 details

  item name         remaining qty   collected qty
    Tiili              0              10
```

Nyt tilaus on täytetty ja se voidaan lopettaa. Painetaan kohdasta `complete shipment`:

```
Order 1239412 completed.
```

Sivu päivittyi automaattisesti aloitussivulle, ja tilaus hävisi tilausten joukosta.

Huom. Tilauksen voi myös sulkea, vaikka ei olisi kerätty ollenkaan tuotteita. Tämä on sentakia niin, koska jokin tuote saattaa loppua kesken keräilyn. Kerätty kuorma lähtee siis vajaana asiakkaalle.

## Osto

Ostossa päästään seuraamaan tukun varastosaldoja, saapuvia tilauksia sekä luomaan tuotetilauksia ja tuotteita.

- `list batches` avaa näkymän varastosaldoon. (Ei sisällä toimintoja)
- `list supply orders` avaa näkymän saapuviin tuotteisiin. (Ei sisällä toimintoja)
- `supply order form` avaa lomakkeen tuotetilauksille
- `add new item` avaa lomakkeen uuden tuotteen luomiselle

### Tuotetilaukset

Näkymään aukeaa lista tuotteista, joita valitaan ruksimalla tuotteet mitä halutaan tilata, sekä lisäämällä määrä (`quantity`), ostohinta (`price`) ja asiakkaan numero (`company id`), jolta tilaus tehdään.

```
Esimerkki:
[x] Tiili          Quantity: 100       Price: 2        Company id: 5
[X] Sementtisäkki   Quantity: 50        Price: 1.3      Company id: 3
```

Lopuksi tilaus lähetetään kohdasta `send`.

Tilausvahvistusta ei vielä toistaiseksi ole luotu, ja sivu vain päivittyy kun tilaus lähetetään.

### Uuden tuotteen lisäys

Lomakkeeseen syötetään lisättävän tuotteen nimi (`name`) sekä myyntihinta (`sell price`) ja luodaan kohdasta `send`.

Esimerkki:

```
Add new item:
Name: Tiili
Sell price: 1
Send
```

Luodaan uusi tuote kohdasta `send` ja järjestelmä ilmoittaa onnistumisesta:

```
Added new item Tiili
```

## Myynti

`List batches` - näyttää tukun varastossa olevat tuotteet.  
`List sale orders` - näyttää kaikki asiakkaiden tilaukset, täältä pääsee myös muuttamaan tilausta.  
`Create company user` - luo uusi käyttötili asiakkaalle.  
`Place company order` - luo uusi tilaus asiakkaalle.

### List sale orders

Tässä näkymässä on kaikki asiakkaiden kaikki keräämättömät tilaukset. Tilauksia voidaan vielä päivittää.

```
Sales view

Order id: 4219231 - Company: Raksapojat - Route: 5 - Qty: 102 - Order date: 2020-09-09
```

Valitsemalla tilaus, aukeaa tilauksen yhteenveto:

```
Order id: 4219231
[Delete order]

Customer: Raksapojat
Address: Raksapolku 10
Email: raksapojat@pl.pl
Country: FI

Item name           Quantity      Price     New qty
Tiili               102           102       [     ]
                    Total:        102

[Update order]

Add new item to order
Item id: [          ]
Quantity: [           ]
[Add item]
```

`delete order` poistaa tilauksen. Vaihtoehtoisesti jo tilattujen tuotteiden määriä voidaan vaihtaa, syöttämällä uusi tilausmäärä `new qty` kohtaan ja painamalla `[Update order]`.

Jos määräksi asetetaan `0`, poistuu tuote listalta kokonaan.

Tuotteita voidaan myös lisätä kohdasta `Add new item to order`, syöttämällä tuotteen koodi ja määrä, sekä painamalla `[Add item]`.

### Create company user

Tässä näkymässä voidaan tehdä uusi käyttötili asiakkaalle, jolla asiakas voi itse tilata tukulta löytyviä tuotteita.

Esimerkki:

```
Username: nakkila
Password: ******
Re-type password: ******
Company id: 13
Send
```

Lähettämisen jälkeen järjestelmä ilmoittaa käyttäjän onnistuneesta luonnista. Tai virheilmoituksella, jos nimi on jo käytösssä, salasanat eivät täsmää tai kyseisellä tunnisteella ei löydy yritystä.

### Place company order

Näkymässä voidaan kirjata hypoteettinen sähköpostitse tai puhelimitse saapunut asiakkaan tilaus.

Esimerkki:

```
Place order:
Company id: 13
   Item name      Price       Qty
      ------- muita tuotteita --------
[x] Tiili         [0.53]      [100]
[x] Laasti        [1.02]      [ 20]
      ------- muita tuotteita --------
Send
```

Onnistuneen tilauksen jälkeen näkyy tilauksen yhteenveto:

```
Order id: 0923484

Customer: Pamlab, L.L.C.

Address: 57 Muir Pass

Email: mtuffieldg@toplist.cz

Country: PLe

Item name	Quantity	Price
Tiili	    100 	      53
Total:	              53
back
```

Tilaus on tehty onnistuneesti, ja kirjattu järjestelmään.

## Kontrolleri

Kontrollerilla on kaikki samat toiminnot, kuin varastolla, keräilyllä, myynnillä ja ostolla.

## Asiakas

Sisäänkirjautumisen jälkeen, avautuu sivu, missä on tukun kaikki tuotteet ja hinnat. Täältä ruksitaan kaikki tuotteet mitä tukusta haluaa tilata.

Esimerkki:

```
[x] Olut  - 1.23e/pc [40                ]
[x] Tiili - 1e/pc    [100               ]
Send
```

Lähetetään tilaus kohdasta `send`. Seuraavaksi saamme tilausvahvistuksen:

```
Thank you for your order. Your order will be collected and shipped as soon as possible.
Customer: Pamlab, L.L.C.

Address: 57 Muir Pass

Email: mtuffieldg@toplist.cz

Country: PLe

Item name	Quantity	Price
Beer	40	49.2
Tiili	150	150
Total:	199.2
back
```

Tilaus on tehty onnistuneesti, ja kirjattu järjestelmään.

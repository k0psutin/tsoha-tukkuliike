# Käyttöohjeet

Jokaiselta sivulta löytyy joko `back` tai `logout` -painikkeet, millä päästään takaisinpäin, tai uloskirjautumaan.

## Varasto

Virtuaalinäkymä simuloi fyysisiä saapuvia tavaroita, ja näet siitä helposti esimerkiksi tilausnumeron `order_id` taikka tuotteen kappalemäärän `qty`.

Saapuvia tavaroida voidaan siirtää tukun varastoon syöttämällä tilauksen `order_id`, sekä kappalemäärä `qty` lomakkeeseen ja painamalla `send`.

Esimerkki:

```
Virtual view of incoming orders

Order id  Supplier id   Countrycode   Order date   Item id  Item name  Item qty
2838343       19             FI    2019-10-08 15:03   3       Tiili       30

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

Ei vielä toteutettu.

## Kontrolleri

Ei vielä toteutettu.

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

Tilaus onnistui siis.

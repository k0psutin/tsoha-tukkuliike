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
Kontrolleri: `kontrolleri/1234`  
Asiakas: `asiakas/1234`

<br>

Jokaisella tunnuksella on oma navigointipalkki millä voi liikkua vaivattomasti eri sivuilla.

Mikäli ei jaksa kirjautua tunnuksilla edestakaisin, voi kirjautua sisään kontrollerin tunnuksilla. Kontrollerilla on toimintoja joka osa-alueelta.

Alapuolelta löytyvät ohjeet näkymien toimintoihin.

## Varasto

- Supply orders
- Supply inventory
- Batch inventory

### Supply orders (aukeaa sisäänkirjautuessa)

Virtuaalinäkymä simuloi fyysisiä saapuvia tavaroita, ja näet siitä helposti esimerkiksi tilausnumeron `order_id` taikka tuotteen kappalemäärän `qty`.

Saapuvia tavaroida voidaan siirtää tukun varastoon valitsemalla tilauksen `order_id` valikosta, sekä näppäilemällä kappalemäärä `qty` lomakkeeseen ja painamalla `send`.

Esimerkki:

```
Supply orders

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

### Supply inventory

Tässä näkymässä voidaan muuttaa saapuvien tuotteiden inventaarion määriä.

Saapuvaa tavaraa vastaanotettaessa huomataan, että tilattu määrä ja saapunut määrä poikkeaa toisistaan: Varastosiirron jälkeen tiiliä jäi tilaukseen vielä 5 kpl.

Esimerkki:

```
Supply orders

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
Batches

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
Batches

----------------------------------------------------------
  Batch nr.       Company id        Quantity       Date
 TI180220FI         Tiili             101       2020-02-18
-----------------------------------------------------------
```

Tukun inventaari valmis.

Jos tuotetta ei löydy, voidaan määräksi syöttää 0 kappaletta, jolloin erä häviää listauksesta.

## Keräily

- Open orders

### Open orders

Virtuaalinäkymä simuloi tukun varastosaldoilla olevia tuotteita. Tuotteista on esillä eränumero (`batch_nr`), tuotteen nimi (`item name`) sekä määrä (`qty`) ja kirjauspäivämäärä (`date`).

Tilauksiin kerätään tavaroita, avaamalla `open orders` -osiosta jokin tilaus.

Tilausta klikattaessa tilaustiedot aukeavat näytölle, ja näet mitä tuotteita tilaus pitää sisällään.

Tuotteita "kerätään" valitsemalla valikosta `batch_nr` sekä kappalemäärä `qty` lomakkeeseen. Tämän jälkeen tuote vahvistetaan kerätyksi painamalla nappia `collect`.

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

- List inventory
- List supply orders
- Supply order form
- List all items/Add new item

### List inventory

Näyttää varastosaldot listana.

### List supply orers

Näyttää saapuvien tavaroiden saldot listana.

### Supply order form

Tässä näkymässä luodaan uusi tilaus saapuville tuotteille.

Valitse ensin yritys miltä tuote tilataan, sen jälkeen tilattava tuote ja määrä.

Painamalla `add` tuote lisätään ostoskoriin. `Show cart` näyttää myös ostoskorissa olevien tuotteiden lukumäärän (ei kappale).

`Show cart`-nappia painamalla päästään ostoskoriin. Ostoskorissa voit poistaa tuotteita, muuttaa niiden tilausmääriä tai tyhjentää ostoskorin.

Tilaus lähetetään `Order`-nappia painamalla, ja varmistamalla tilaus.

### List all items/Add new item

Kaikki myytävät/ostettavat tuotteet näkyvät listana, ja niitä voi luoda lisää.

## Uuden tuotteen luonti

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

- List inventory
- List sale orders
- Create new company
- Create new company user
- Place company order

### List inventory

Näyttää tukun varastosaldon listana.

### List sale orders

Tässä näkymässä on kaikki asiakkaiden kaikki keräämättömät tilaukset. Tilauksia voidaan vielä päivittää.

```
Sales view

Order id: 4219231 - Company: Raksapojat - Route: 5 - Qty: 102 - Order date: 2020-09-09
```

Valitsemalla tilaus, aukeaa tilauksen yhteenveto. Yhteenvedosta voidaan poistaa kyseinen tilaus, tai tuotteita tilauksesta. (Myöhemmin mahdollisuus lisätä tuotteita tai muuttaa määriä.)

### Create company

Tässä näkymässä voidaan luoda uusi asiakas järjestelmään.

```
Company name:
Esimerkki yritys
Email:
esimerkki@yritys.fi
Address:
Esimerkkikuja 5
Country:
FI
Route:
3
[     Create company      ]
```

Lomakkeeseen syötetään asiakkaan tiedot ja luodaan se `Create company`-napilla.

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

Tilaus luodaan keräämällä ostoskoriin tilattavat tuotteet. Ostokori aukeaa `Show cart`-painikkeella, ja korissa voidaan poistaa tuotteita ja/tai muokata tuotteiden määriä.

Kun tarvittavat tuotteet ovat valittu, valitaan asiakas valikosta, jolle tilaus tehdään. Tilaus lähetetään painamalla `Order`-painiketta.

## Kontrolleri

### Kontrollerin näkymät

Inventory -> Batches - Supply Orders - Place new supply order  
Orders -> List sale orders  
Items -> List all items/Create new items  
Users -> Create new user

Kontrollerilta löytyy samoja näkymiä kuin muilta käyttäjiltä. Erona on se, että voidaan luoda järjestelmään uusia käyttäjiä.

## Asiakas

- Your orders
- Create new order
- Info

### Your orders

Tässä näkymässä näkyvät kaikki asiakkaan tilaukset. Listalta voidaan valita tilaus, jolloin päästään tilauksen yhteenvetoon.

### Create new order

Tässä näkymässä voidaan luoda uusi tilaus järjestelmään kiinteillä hinnoilla. Valitse haluamasi tuotteet ostoskoriin ja `Order`-nappia painamalla tilaus on lähetetty järjestelmään.

### Info

Tässä näkymässä näkyy asiakkaan tiedot. Näkymässä voidaan myös vaihtaa salasanaa.

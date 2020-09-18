# Tukkuliikkeen tietokannanhallintajärjestelmä

Yksinkertaistettu tukkuliikkeen varaston, sekä osto/myyntitapahtumien hallintajärjestelmä. Järjestelmässä on käyttäjillä eri tasoja riippuen siitä, onko henkilö logistiikassa, myynnissä, ostossa, myyntierien keräilijänä tai kontrolleri. Kontrollerilla on korkein luokitus (admin), eli kontrollerilla pääsee käsiksi kaikkiin osa-alueisiin, sekä luomaan uusia käyttäjiä. Muuten toiminnot on rajattu niin, että nähdään vain tarvittavat asiat.

Hallintajärjestelmällä pystytään helposti tekemään yhteenvetoja annetun aikavälin tapahtumista ja seuraamaan realiaikaisesti varaston saldoja sekä eriä.

Tällä järjestelmällä on esimerkiksi mahdollista jäljittää toimintoja kuten että, kuka tilasi kuorman X, mikä tuottaja ja toimitusmaa oli tuotteella X sekä kuka on kerännyt ostajalle Y tuotetta X.

Myytävät tuotteet voidaan myös asettaa suljetuiksi asiakkailta.

### Toiminnot

Osto pystyy luomaan tilauksia muille tukkureille, luomaan uusia tuotteita, sekä luomaan uusia tukkuliikkeitä.

Logistiikka vastaa tuotteiden inventoinnista, sekä saapuneiden kuormien kirjaamisesta tukun tietokantaan.

Myynti luo uusia asiakkaita, sekä kirjaa asiakkailta saamiaan hypoteettisia tilauksia tietokantaan.

Keräily vastaa ostotilausten tuotteiden (oikein) keräämisestä, ja valmiiden tilausten kuittaamisesta.

Kontrolleri pystyy seuraamaan tukun joka osa-aluetta, ja pystyy tarvittaessa muuttamaan tilauksia, varastosaldoja, luomaan uusia myytäviä tavaroita sekä käyttäjiä.

Myös asiakas voi tilata suoraan tukusta omilla tunnuksillaan.

<br>

### Toteutuneet/suunnitellut toiminnot

Varasto:  
[x] Pystyy siirtämään saapuvia tuotteita tukun varastoon  
[x] Virtuaalinäkymä saapuvista tuotteista  
[x] Varaston inventointi  
<br>
Myynti:  
[x] Pystyy luomaan ostotilauksia  
[x] Näkee avoimet/suljetut asiakkaiden tilaukset  
[x] Näkee varastossa olevat tuotteet
[x] Pystyy luomaan tunnuksia asiakkaille
[x] Voi muokata myyntitilauksia

<br>

Osto:  
[x] Pystyy luomaan uusia tuotteita  
[x] Pystyy näkemään saapuvat tuotteet, sekä varaston tuotteet  
[x] Pystyy tekemään tilauksia tuotteille  
[x] Pystyy lisäämään uusia tuotteita
[ ] Näkee yhteenvedon saapuvista sekä varaston tuotteista annetulta ajalta

<br>

Keräily:  
[x] Pystyy keräämään tuotteita avoimiin tilauksiin  
[x] Virtuaalinäkymä tukun saldoilla olevista tuotteista  
[x] Pystyy luomaan lähetyksen kerätystä tilauksesta

<br>

Kontrolleri:  
[x] Pääsee joka osa-alueelle  
[x] Voi luoda käyttäjiä
[x] Voi muokata myyntitilauksia, varastosaldoja, tuotetilauksia  
[ ] Näkee yhteenvetoja myynneistä, ostoista jne.

<br>

Asiakas:  
[x] Voi luoda ostotilauksen  
[x] Saa myyntivahvistuksen tilauksen jättämisen jälkeen.

<br>

Sovellus:  
[x] Mahdollisuus luoda käyttäjä komentokehotteelta.

### Dokumentaation vaiheet

[x] Tietokanta osio  
[x] Käyttöohjeet  
[ ] Asennusohje  
[ ] Käyttötapaukset  
[ ] Englanninkielinen versio

### Sovelluksen vaiheet

[x] Runko valmiiksi  
[ ] Syötteiden validointi  
[ ] Ulkoasu kuntoon

### Suunniteltuja toimintoja

[ ] Transaktioloki varastosiirroille  
[ ] Roolien eriytys omaksi taulukseen

<br>

### Sovelluksen osoite:

[Heroku - sheltered-temple-19572](https://sheltered-temple-19572.herokuapp.com/)
<br>

### Käyttäjätunnukset:

<br>
    
Logistiikka: `varasto/1234`  
Keräily: `keraily/1234`  
Osto: `osto/1234`  
Myynti: `myynti/1234`  
Kontrolleri: `admin/1234`  
Asiakas: `asiakas/1234`

<br>

### Käyttäjätasot

| Taso | Rooli            |
| :--: | ---------------- |
|  1   | asiakas          |
|  2   | varasto          |
|  3   | keräily          |
|  4   | myynti           |
|  5   | osto             |
|  6   | kontroller/admin |

<br>

### Dokumentaatio

<br>

[Tietokanta](/doc/db.md)  
[Käyttöohjeet](/doc/kayttoohje.md)  
Asennusohje  
Käyttötapaukset

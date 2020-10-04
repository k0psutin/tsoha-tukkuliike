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
[x] Saapuvien tuotteiden inventointi  
[x] Varaston inventointi  
<br>
Myynti:  
[x] Pystyy luomaan ostotilauksia  
[x] Näkee kaikki tilaukset  
[x] Näkee varastossa olevat tuotteet  
[x] Pystyy luomaan uusia yrityksiä tietokantaan  
[x] Pystyy luomaan tunnuksia asiakkaille  
[x] Voi muokata myyntitilauksia (toistaiseksi vain tilauksen poisto ja/tai tuotteen poisto)  
[ ] Näkee tilastoja tilauksista annetulta ajalta

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
[x] Voi muokata varastosaldoja, saapuvien tuotteiden saldoja  
[ ] Näkee yhteenvetoja myynneistä, ostoista jne.

<br>

Asiakas:  
[x] Voi luoda ostotilauksen  
[x] Voi vaihtaa salasanansa  
[x] Saa myyntivahvistuksen tilauksen jättämisen jälkeen.

<br>

Sovellus:  
[x] Mahdollisuus luoda käyttäjä komentokehotteelta.

### Dokumentaation vaiheet

[x] Tietokanta osio  
[x] Käyttöohjeet  
[ ] Asennusohje  
[ ] Englanninkielinen versio

### Sovelluksen vaiheet

[x] Runko valmiiksi  
[x] Syötteiden validointi  
[x] Varmistusikkuna mm. tilaamiseen.  
[x] Ulkoasu kuntoon

### Suunniteltuja toimintoja

[ ] Graafisia esityksiä myynneistä yms.  
[ ] Transaktioloki varastosiirroille  
[ ] Roolien eriytys omaksi taulukseen  
<br>

### Sovelluksen osoite:

[https://sheltered-temple-19572.herokuapp.com/](https://sheltered-temple-19572.herokuapp.com/)
<br>

### Käyttäjätunnukset:

<br>
    
Logistiikka: `varasto/1234`  
Keräily: `keraily/1234`  
Osto: `osto/1234`  
Myynti: `myynti/1234`  
Kontrolleri: `kontrolleri/1234`  
Asiakas: `asiakas/1234`

<br>

### Käyttäjätasot

| Taso | Rooli       |
| :--: | ----------- |
|  1   | asiakas     |
|  2   | varasto     |
|  3   | keräily     |
|  4   | myynti      |
|  5   | osto        |
|  6   | kontrolleri |

<br>

### Dokumentaatio

<br>

[Tietokanta](/doc/db.md)  
[Käyttöohjeet](/doc/kayttoohje.md)  
Asennusohje

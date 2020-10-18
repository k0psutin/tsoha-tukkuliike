[English version](README_EN.md)

# Tukkuliikkeen tietokannanhallintajärjestelmä

Yksinkertaistettu tukkuliikkeen varaston, sekä osto/myyntitapahtumien hallintajärjestelmä. Järjestelmässä on käyttäjillä eri tasoja riippuen siitä, onko henkilö logistiikassa, myynnissä, ostossa, myyntierien keräilijänä tai kontrolleri. Kontrollerilla on korkein luokitus, eli kontrollerilla on muiden luokkien toimintojen lisäksi mahdollisuus mm. ludoa uusia käyttäjiä. Muuten toiminnot on rajattu niin, että nähdään vain tarvittavat asiat.

Hallintajärjestelmällä pystytään helposti tekemään yhteenvetoja valitsemastaan vuodesta ja seuraamaan realiaikaisesti varaston saldoja sekä eriä.

## Käyttäjien toiminnot

Osto pystyy luomaan tilauksia muille tukkureille, luomaan uusia tuotteita, sekä luomaan uusia tukkuliikkeitä.

Logistiikka vastaa tuotteiden inventoinnista, sekä saapuneiden kuormien kirjaamisesta tukun tietokantaan.

Myynti luo uusia asiakkaita, sekä kirjaa asiakkailta saamiaan hypoteettisia tilauksia tietokantaan.

Keräily vastaa ostotilausten tuotteiden (oikein) keräämisestä, ja valmiiden tilausten kuittaamisesta.

Kontrolleri pystyy seuraamaan tukun joka osa-aluetta, ja pystyy tarvittaessa muuttamaan varastosaldoja, luomaan uusia tavaroita sekä käyttäjiä.

Myös asiakas voi tilata suoraan tukusta omilla tunnuksillaan.

## Toteutuneet/suunnitellut toiminnot

Varasto:  
[x] Pystyy siirtämään saapuvia tuotteita tukun varastoon  
[x] Virtuaalinäkymä saapuvista tuotteista  
[x] Saapuvien tuotteiden inventointi  
[x] Varaston inventointi

Myynti:  
[x] Pystyy luomaan ostotilauksia  
[x] Näkee kaikki tilaukset  
[x] Näkee varastossa olevat tuotteet  
[x] Pystyy luomaan uusia yrityksiä tietokantaan  
[x] Pystyy luomaan tunnuksia asiakkaille  
[x] Voi muokata myyntitilauksia
[x] Näkee valitun vuoden myynnit

Osto:  
[x] Pystyy luomaan uusia tuotteita  
[x] Pystyy näkemään saapuvat tuotteet, sekä varaston tuotteet  
[x] Pystyy tekemään tilauksia tuotteille  
[x] Pystyy lisäämään uusia tuotteita  
[x] Näkee yhteenvedon saapuvista, varaston tuotteista sekä myydyistä tuotteista

Keräily:  
[x] Pystyy keräämään tuotteita avoimiin tilauksiin  
[x] Virtuaalinäkymä tukun saldoilla olevista tuotteista  
[x] Pystyy luomaan lähetyksen kerätystä tilauksesta

Kontrolleri:  
[x] Pääsee joka osa-alueelle  
[x] Voi luoda käyttäjiä  
[x] Voi muokata varastosaldoja, saapuvien tuotteiden saldoja  
[x] Näkee yhteenvetoja myynneistä, ostoista jne.

Asiakas:  
[x] Voi luoda ostotilauksen  
[x] Voi vaihtaa salasanansa  
[x] Saa myyntivahvistuksen tilauksen jättämisen jälkeen.

Sovellus:  
[x] Mahdollisuus luoda käyttäjä komentokehotteelta.

## Dokumentaation vaiheet

[x] Tietokanta osio  
[x] Käyttöohjeet  
[x] Asennusohje  
[x] Englanninkielinen versio dokumentaatiosta

## Sovelluksen vaiheet

[x] Runko valmiiksi  
[x] Syötteiden validointi  
[x] Varmistusikkuna mm. tilaamiseen.  
[x] Ulkoasu kuntoon  
[x] Graafisia esityksiä myynneistä yms.

## Sovelluksen osoite:

[https://sheltered-temple-19572.herokuapp.com/](https://sheltered-temple-19572.herokuapp.com/)

## Käyttäjätunnukset:

Logistiikka: `varasto/1234`  
Keräily: `keraily/1234`  
Osto: `osto/1234`  
Myynti: `myynti/1234`  
Kontrolleri: `kontrolleri/1234`  
Asiakas: `asiakas/1234`

## Käyttäjätasot

| Taso | Rooli       |
| :--: | ----------- |
|  1   | asiakas     |
|  2   | varasto     |
|  3   | keräily     |
|  4   | myynti      |
|  5   | osto        |
|  6   | kontrolleri |

## Dokumentaatio

[Tietokanta](/doc/db.md)  
[Käyttöohjeet](/doc/kayttoohje.md)  
[Asennusohje](/doc/asennusohje.md)

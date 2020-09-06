# Tukkuliikkeen tietokannanhallintajärjestelmä

Yksinkertaistettu tukkuliikkeen varaston, sekä osto/myyntitapahtumien hallintajärjestelmä. Järjestelmässä on käyttäjillä eri tasoja riippuen siitä, onko henkilö logistiikassa, myynnissä, ostossa, myyntierien keräilijänä tai kontrolleri. Kontrollerilla on korkein luokitus (admin), eli kontrollerilla pääsee käsiksi kaikkiin osa-alueisiin, sekä luomaan uusia käyttäjiä. Muuten toiminnot on rajattu niin, että nähdään vain tarvittavat asiat.

Hallintajärjestelmällä pystytään helposti tekemään yhteenvetoja annetun aikavälin tapahtumista ja seuraamaan realiaikaisesti varaston saldoja sekä eriä.

Tällä järjestelmällä on esimerkiksi mahdollista jäljittää toimintoja kuten että, kuka tilasi kuorman X, mikä tuottaja ja toimitusmaa oli tuotteella X sekä kuka on kerännyt ostajalle Y tuotetta X.

### Toiminnot

Osto pystyy luomaan tilauksia muille tukkureille, ja ostokuorman saapuessa tukkuliikkeeseen, logistiikka huolehtii kuormasta.

Logistiikka pystyy siirtämään saapuvat kuormat tukun saldolle, jolloin kuormalle luodaan sisäiseen käyttöön ja jäljitykseen käytettävä eränumero.

Myynti kirjaa saamansa hypoteettiset tilaukset järjestelmään, jolloin keräilijä pystyy keräämään asiakkaalle lähtevän kuorman, ja kuittaamaan tämän kerätyksi.

Keräily vastaa ostotilausten tuotteiden (oikein) keräämisestä, ja valmiiden tilausten kuittaamisesta.

Kontrolleri pystyy seuraamaan tukun joka osa-aluetta, ja pystyy tarvittaessa muuttamaan tilauksia, varastosaldoja, luomaan uusia myytäviä tavaroita sekä käyttäjiä.

Myös asiakas voi tilata suoraan tukusta omilla tunnuksillaan.

<br>

### Toteutuneet toiminnot

Ei vielä mitään.  
<br>

### Dokumentaation vaiheet

Tietokantaosio aloitettu, muut tekemättä.

### Jatkokehitysideoita

Ei vielä mitään.
<br>

### Sovelluksen osoite: <Ei vielä toteutettu>

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

### Dokumentaatio

<br>

[Tietokanta](/doc/db.md)  
Käyttöohjeet  
Asennusohje  
Käyttötapaukset

# Asennusohje

Kloonaa repository haluamaasi hakemistoon githubista komennolla:

```
git clone https://github.com/k0psutin/tsoha-tukkuliike
```  

Varmista, että sinulla on PostgreSQL versio 13.x asennettuna, sekä Python3.  
[https://www.postgresql.org/download/](https://www.postgresql.org/download/)  

Luo hakemistoon ```.env``` tiedosto seuraavilla muuttujilla:
```
SECRET_KEY=<secret>
DATABASE_URL=postgres+psycopg2://<username>:<password>@localhost:5433/<database>
```
Keksi jokin satunnainen merkkijono ```<secret>```-muuttujaan, tai generoi se jollain internetistä löytyvällä MD5 generaattorilla.  

Mikäli käytät PostgreSQL vakiotunnuksia ja tietokantaa, sijoita ```<username>``` ja ```<database>``` kohdalle ```postgres``` ja ```<password>``` salasana. Muuten korvaa kohdat niillä tiedoilla mitä asetit.

## Tietokannan käyttöönotto

Hakemistosta ```\db``` löytyy tietokannan skeema tiedostossa ```schema.sql```. Luo tietokantataulukot komennolla 
```
psql < db\schema.sql
```

Jos et halua testidataa käyttöön, hyppää seuraavan vaiheen yli.

## Testidata

Hakemisto sisältää myös vakiokäyttäjät (mitkä on listattu ohjeissa) sekä testidataa. Testidatassa on kaksi eri kokoa, pieni sekä iso.

Jos haluat testidataa käyttöön, aja tiedot tietokantaan komennoilla (esimerkkinä pienen datan vienti tietokantaan):
```
psql < db\users.sql
psql < db\mock_companies_small.sql
psql < db\mock_items_small.sql
psql < db\mock_supply_orders_small.sql
psql < db\mock_sale_orders_small.sql
```

Tässä järjestyksellä on väliä, koska osa taulukoista sisältää viiteavaimia, ja lisäykset antavat virheitä, jos osa taulukoista on tyhjiä.

## Ohjelman valmistaminen käynnistykseen

Luo hakemiston juuressa pythonin virtuaaliympäristö komennolla:
```
python 3 -m venv venv
```
Aktivoi virtuaaliympäristö:
```
source venv/bin/activate (linux)
```
tai
```
venv\Scripts\activate (windows)
```
Asenna tarvittavat kirjastot komennolla:
```
pip install -r requirements.txt
```

## Käyttäjän luonti

Suorita komentokehotteelta komento:
```
flask init
```

Täältä pääset luomaan uuden kontrolleri-luokan käyttäjän, millä pääset luomaan muita käyttäjiä sovelluksessa.

Suorita sovellus komennolla:
```
flask run
```

Avaa sovellus osoitteessa: [http://localhost:5000/](http://localhost:5000/)


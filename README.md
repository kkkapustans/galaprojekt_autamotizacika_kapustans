# galaprojekt_autamotizacika_kapustans
Projekta pārskats
Šī projekta mērķis ir izstrādāt automatizētu rīku, kas izgūst un apstrādā ziņu virsrakstus no Latvijas Sabiedrisko mediju (LSM) RSS plūsmas. Lietotāji var norādīt, cik jaunāko virsrakstu viņi vēlas skatīt (1–30 ieraksti), un skripts atgriež šo virsrakstu sarakstu kopā ar publicēšanas datumiem, saitēm un īsiem aprakstiem, kas tiek saglabāta excelī.
Galvenās funkcijas
•	Lejupielādēt RSS datus no https://www.lsm.lv/rss/?lang=lv&catid=14.
•	Analizēt RSS XML, lai iegūtu virsrakstu (), publicēšanas datumu (), saiti () un aprakstu ().
•	Lietotāju ievadē parādīt norādīto jaunāko virsrakstu skaitu.
•	Apstrādāt un ziņot par kļūdām: nederīgu lietotāja ievadi, HTTP pieprasījumu kļūmes un XML analīzes kļūdas.
•	Veikt izmaiņas rss_news.xlsx failā, atspoguļojot jaunāko informāciju.


Izmantotās Python bibliotēkas
•	requests – vienkārša un uzticama HTTP klienta bibliotēka pieprasījumu veikšanai RSS URL; nodrošina statusa koda validāciju un izņēmumu apstrādi.
•	xml.etree.ElementTree – iebūvētais XML analizētājs valodā Python, ko izmanto, lai droši un efektīvi konvertētu RSS XML Python objektu kokā.
•	sys – sistēmas modulis, ko izmanto kļūdu ziņošanai (sys.stderr) un skripta pārtraukšanai ar statusa kodu (sys.exit).

Datu struktūras

Pielāgota datu struktūra tiek izmantota, lai saglabātu ziņu informāciju:
class NewsItem:
    def __init__(self, title: str, link: str, date: str, description: str):
        self.title = title
        self.link = link
        self.date = date
        self.description = description

    def __repr__(self):
        return f"NewsItem(title={self.title!r}, date={self.date!r})"
•	NewsItem – klase, kurā ir ziņu ieraksta virsraksts, publicēšanas datums, saite un apraksts.
•	Katrs RSS XML elements <item> tiek pārveidots par NewsItem instanci un saglabāts Python sarakstā.

Programmas izmantošanas pamācība
1.	Koda atvēršana
2.	Jālejupielādē bibliotēka pip install requests, ja vēl tā nav, to var pie kontolpaneļa
3.	Programmas palaišana
4.	Lietotājs ievada skaitli no 1 līdz 30, kas norāda, cik virsrakstu vēlaties iegūt.
5.	Pēc ievades skripts ielādē RSS plūsmu un izdrukā atlasītos virsrakstus ar datumiem, saitēm un aprakstiem.
6.	Kļūdu apstrāde
o	Ja ievade nav skaitlis vai ir ārpus atļautā diapazona, skripts aizveras ar atbilstošu ziņojumu.
o	Ja HTTP pieprasījums neizdodas (piemēram, 403, 404) vai XML programma neizdodas, lietotājs saņem skaidru kļūdas aprakstu.
7.	Lietotājs atver excel failu rss_news.xlsx(ja tāds nav, tad tas tiek izveidots), kur kolonu skaits ir atkarīgs, cik liela bija ievade ziņu skaitam, rindās ir informācija par ziņas virsrakstu, 



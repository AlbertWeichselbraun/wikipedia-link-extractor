Extracts Wikipedia link text and link targets from Wikipedia XML dumps downloaded from the [wikimedia](https://meta.wikimedia.org/wiki/Data_dumps).

These data can then be used to improve named entity linking tasks as outlined in the paper *Weichselbraun, Albert, Kuntschik, Philipp and Brasoveanu, Adrian M.P.. (2019). Name Variants for Improving Entity Discovery and Linking., Leipzig, Germany.*.

### Usage

Generate a CSV file that contains a mapping from Wikipedia link text to the corresponding link targets.
```bash
python3 ./wikipedia-link-extractor.py enwiki-20190320-pages-articles.xml.bz2 link-file.csv.xz
```

Transform the created link mapping to the RDF format (turtle).
```bash
python3 ./get-unique-mappings.py link-file.csv.xz unique-links.n3.xz turtle
```

### Available datasets

The following datasets have been extracted with the method outlined above and are available for download.

 1. Wikipedia link text to link mapping based on the 
    - wikipedia dump from 2017-12-01: 
    - [wikimedia dump from 2019-03-20](https://drive.switch.ch/index.php/s/5Udixs8VzsrHaId)
 2. An RDF file containing unique link text to link mappings (i.e. mappings that are only used to refer to a single DBpedia resource):
    - wikipedia dump from 2017-12-01:
    - [wikimedia dump from 2019-03-20](https://drive.switch.ch/index.php/s/yUz45Mz6xHchCds)
    
    The files use `skos:altLabel` to link between the DBpedia resource and the unique link text.

    **Example data**
    ```turtle
    @prefix skos:<http://www.w3.org/2004/02/skos/core#>
    @prefix dbr:<http://dbpedia.org/resource/>
    dbr:Libertarian_socialism   skos:altLabel   "anti-authoritarian interpretations"
    dbr:Taoism   skos:altLabel   "Taoist philosophers"
    dbr:Cynicism_(philosophy)   skos:altLabel   "Cynics"
    dbr:Zoroastrianism   skos:altLabel   "Zoroastrian Prophet"
    dbr:Egalitarianism   skos:altLabel   "egalitarian society"
    dbr:Christian_anarchism   skos:altLabel   "religious anarchism"
    ```

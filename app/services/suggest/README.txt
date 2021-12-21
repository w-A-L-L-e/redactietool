This is initial import from the suggest library from Miel:
https://github.com/viaacode/skos-scripts-redactietool

Basically it fetches thesauri data to be used to populate some select's and multi-select boxes in redactietool
Already added the necessary requirements.txt here so that it works on my local machine but will further test this in
the docker image before merging (we will als change some hardcoded test urls into env vars to make it ready for a qas release).


```
from suggest.Suggest import Suggest

SPARQL_ENDPOINT = "http://example.org/query"
USER = "user"
PASSWORD = "password"

suggest = Suggest(SPARQL_ENDPOINT, USER, PASSWORD)

for r in suggest.suggest_by_label(['Recht'], ['Secundair 2de graad']):
    print(r)

for r in suggest.suggest(['https://data.meemoo.be/terms/ond/thema#nederlandse-taal'],['https://data.meemoo.be/terms/ond/graad#lager-1ste-graad']):
    print(r)

```
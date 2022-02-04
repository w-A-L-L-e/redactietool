import os
import re
from typing import List

from SPARQLWrapper import JSON, POST, SPARQLWrapper2

URI_REGEX = (
    "((http|https)://)(www.)?"
    + "[a-zA-Z0-9@:%._\\+~#?&//=]"
    + "{2,256}\\.[a-z]"
    + "{2,6}\\b([-a-zA-Z0-9@:%"
    + "._\\+~#?&//=]*)"
)

GET_LIST_QUERY = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?id ?label ?definition
WHERE {{

    BIND(URI('{scheme}') AS ?scheme)

    ?id a skos:Concept;
    skos:prefLabel ?label;
    skos:inScheme ?scheme.

    OPTIONAL {{
        ?id skos:definition ?definition .
    }}
}}
ORDER BY ASC(?label)
"""

GET_COLLECTION_QUERY = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?id ?label ?definition (count(?child) as ?children)
WHERE {{
    BIND(URI('{collection}') AS ?collection)
    ?collection skos:member ?id.

    ?id a skos:Concept;
    skos:prefLabel ?label.

    OPTIONAL {{
        ?id skos:definition ?definition .
    }}

    OPTIONAL {{
        ?id skos:narrower ?child.
    }}
}}
GROUP BY ?id ?label ?definition
"""

GET_CHILDREN_QUERY = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?id ?label ?definition ?parent
WHERE {{
    ?parent skos:narrower ?id.
    FILTER (?parent IN ({concept}))

    ?id a skos:Concept;
    skos:prefLabel ?label.

    OPTIONAL {{
        ?id skos:definition ?definition .
    }}
}}
ORDER BY ASC(?label)
"""

SUGGEST_BY_LABELS_QUERY = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?id ?label ?definition
WHERE {{
    BIND(URI('{thema_scheme}') AS ?thema_scheme)
    BIND(URI('{graad_scheme}') AS ?graad_scheme)
    BIND(URI('{vak_scheme}') AS ?vak_scheme)

    ?id a skos:Concept;
    skos:prefLabel ?label;
    skos:inScheme ?vak_scheme;
    skos:related ?thema, ?graad.

    ?thema skos:inScheme ?thema_scheme.
    ?graad_scheme skos:member ?graad.

    OPTIONAL {{
        ?id skos:definition ?definition .
    }}

    ?thema skos:prefLabel ?thema_label.
    ?graad skos:prefLabel ?graad_label.

    FILTER (
        STR(?thema_label) IN ({themas}) &&
        STR(?graad_label) IN ({graden}) )
}}
ORDER BY ASC(?label)
"""

SUGGEST_BY_IDS_QUERY = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?id ?label ?definition
WHERE {{
    BIND(URI('{thema_scheme}') AS ?thema_scheme)
    BIND(URI('{graad_scheme}') AS ?graad_scheme)
    BIND(URI('{vak_scheme}') AS ?vak_scheme)

    ?id a skos:Concept;
    skos:prefLabel ?label;
    skos:inScheme ?vak_scheme;
    skos:related ?thema, ?graad.

    ?thema skos:inScheme ?thema_scheme.
    ?graad_scheme skos:member ?graad.

    OPTIONAL {{
        ?id skos:definition ?definition .
    }}

    FILTER (
        ?thema IN ({themas}) &&
        ?graad IN ({graden}) )
}}
ORDER BY ASC(?label)
"""

GET_CONCEPT_BY_IDS_QUERY = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?id ?label ?definition
WHERE {{
    ?id a skos:Concept;
    skos:prefLabel ?label.

    OPTIONAL {{
        ?id skos:definition ?definition .
    }}

    FILTER (?id IN ({concept}))
}}
ORDER BY ASC(?label)
"""

GET_CANDIDATES_QUERY = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?id ?label ?definition
WHERE {{
    BIND(URI('{thema_scheme}') AS ?thema_scheme)
    BIND(URI('{graad_scheme}') AS ?graad_scheme)
    BIND(URI('{vak_scheme}') AS ?vak_scheme)

    ?id a skos:Concept;
    skos:prefLabel ?label;
    skos:inScheme ?vak_scheme;
    skos:related ?thema, ?graad.

    ?thema skos:inScheme ?thema_scheme.
    ?graad_scheme skos:member ?graad.

    OPTIONAL {{
        ?id skos:definition ?definition .
    }}

    FILTER (
        ?thema IN ({themas}) ||
        ?graad IN ({graden}) )

}}
ORDER BY ASC(?label)
"""

GET_RELATED_VAK_QUERY = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?id ?label ?definition
WHERE {{
    BIND(URI('{vak_scheme}') AS ?vak_scheme)

    ?id a skos:Concept;
    skos:prefLabel ?label;
    skos:inScheme ?vak_scheme;
    skos:related ?concept.

    OPTIONAL {{
        ?id skos:definition ?definition .
    }}

    FILTER (?concept IN ({concepts}))

}}
ORDER BY ASC(?label)
"""


# Function to validate URL
# using regular expression
def isValidURI(str):

    # Compile the ReGex
    p = re.compile(URI_REGEX)

    # If the string is empty
    # return false
    if str is None:
        return False

    # Return if the string
    # matched the ReGex
    if re.search(p, str):
        return True

    return False


def join_ids(ids):
    for id in ids:
        if not isValidURI(id):
            raise ValueError("The id {} is not a valid URL.".format(id))

    return ", ".join("<" + str(id) + ">" for id in ids)


def read_query(file_path):
    # check if file is present
    if os.path.isfile(file_path):
        # open text file in read mode
        text_file = open(file_path, "r")

        # read whole file to a string
        data = text_file.read()

        # close file
        text_file.close()
        return data
    return None


class Suggest:
    """A simple api for vocbench data"""

    OND_NS = "https://data.meemoo.be/term/onderwijs/"

    def __init__(self, endpoint: str, user: str, password: str):
        self.sparql = SPARQLWrapper2(endpoint)
        self.sparql.setMethod(POST)
        self.sparql.setCredentials(user, password)
        self.sparql.setReturnFormat(JSON)

    def __exec_query(self, query: str, **kwargs):
        formatted = query.format(**kwargs)
        self.sparql.setQuery(formatted)
        for result in self.sparql.query().bindings:
            yield {
                "id": result["id"].value,
                "label": result["label"].value,
                "definition": result["definition"].value,
            }

    def get_list(self, scheme: str):
        """Get thesaurus concepts by scheme id."""

        if not isValidURI(scheme):
            raise ValueError("The id {} is not a valid URL.".format(scheme))

        for res in self.__exec_query(GET_LIST_QUERY, scheme=scheme):
            yield res

    def get_concept(self, concept: List[str]):
        """Get thesaurus concept by ids."""

        concepts = join_ids(concept)

        for res in self.__exec_query(GET_CONCEPT_BY_IDS_QUERY, concept=concepts):
            yield res

    def get_collection(self, collection: str):
        """Get a collection members by collection id."""

        if not isValidURI(collection):
            raise ValueError("The id {} is not a valid URI.".format(collection))

        for res in self.__exec_query(GET_COLLECTION_QUERY, collection=collection):
            yield res

    def get_children(self, concept: List[str]):
        """Get the children of a list of concept ids."""

        concepts = join_ids(concept)

        for res in self.__exec_query(GET_CHILDREN_QUERY, concept=concepts):
            yield res

    def get_vakken(self):
        """Get list 'vakken'."""

        for res in self.get_list(f"{self.OND_NS}vak"):
            yield res

    def get_themas(self):
        """Get list 'themas'."""

        for res in self.get_list(f"{self.OND_NS}thema"):
            yield res

    def get_graden(self):
        """Get list 'onderwijsgraden'."""

        for res in self.get_collection(f"{self.OND_NS}graad"):
            yield res

    def get_niveaus(self):
        """Get list 'onderwijsniveaus'."""

        for res in self.get_collection(f"{self.OND_NS}niveau"):
            yield res

    def suggest(self, thema: List[str], graad: List[str]):
        """Suggest 'vakken' based on the identifiers of 'onderwijsgraad' and 'thema'."""

        themas = join_ids(thema)
        graden = join_ids(graad)

        for res in self.__exec_query(
            SUGGEST_BY_IDS_QUERY,
            thema_scheme=f"{self.OND_NS}thema",
            vak_scheme=f"{self.OND_NS}vak",
            graad_scheme=f"{self.OND_NS}graad",
            themas=themas,
            graden=graden,
        ):
            yield res

    def suggest_by_label(self, thema: List[str], graad: List[str]):
        """Suggest 'vakken' based on 'onderwijsgraad' and 'thema'."""

        themas = ", ".join('"' + str(t) + '"' for t in thema)
        graden = ", ".join('"' + str(g) + '"' for g in graad)

        print("running qry=", SUGGEST_BY_LABELS_QUERY)
        for res in self.__exec_query(
            SUGGEST_BY_LABELS_QUERY,
            thema_scheme=f"{self.OND_NS}thema",
            vak_scheme=f"{self.OND_NS}vak",
            graad_scheme=f"{self.OND_NS}graad",
            themas=themas,
            graden=graden,
        ):
            yield res

    def get_candidates(self, thema: List[str], graad: List[str]):
        """Get all possible 'vakken' based on the identifiers of 'onderwijsgraad' and 'thema'."""

        themas = join_ids(thema)
        graden = join_ids(graad)

        for res in self.__exec_query(
            GET_CANDIDATES_QUERY,
            thema_scheme=f"{self.OND_NS}thema",
            vak_scheme=f"{self.OND_NS}vak",
            graad_scheme=f"{self.OND_NS}graad",
            themas=themas,
            graden=graden,
        ):
            yield res

    def get_related_vak(self, concept: List[str]):
        """Get related vak by concept ids."""

        concepts = join_ids(concept)

        for res in self.__exec_query(
            GET_RELATED_VAK_QUERY, vak_scheme=f"{self.OND_NS}vak", concepts=concepts
        ):
            yield res

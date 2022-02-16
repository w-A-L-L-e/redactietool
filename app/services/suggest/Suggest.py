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

OND_NS = "https://data.hetarchief.be/id/onderwijs/"
EXT_NS = "https://w3id.org/onderwijs-vlaanderen/id/"

PREFIX = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX str: <{EXT_NS}structuur/>
PREFIX col: <{EXT_NS}collectie/>
PREFIX ocol: <{OND_NS}collectie/>

"""

GET_NIVEAUS = (
    PREFIX
    + """
SELECT ?id ?label ?definition ?collection (count(?child) as ?child_count) (SAMPLE(?parent) as ?parent_id)
WHERE {{
    {{ col:niveau skos:member ?id.
       FILTER (?id != str:basisonderwijs)
    }} UNION {{ col:subniveau skos:member ?id. }}

    ?id a skos:Concept;
        skos:prefLabel ?label;
        skos:definition ?definition .

    ?c skos:member ?id; skos:prefLabel ?collection.

    OPTIONAL {{ ?id skos:narrower ?child. }}
    OPTIONAL {{ ?id skos:broader ?parent }}
}}
GROUP BY ?id ?label ?definition ?collection
"""
)

GET_COLLECTION_QUERY = (
    PREFIX
    + """
SELECT ?id ?label ?definition (count(?child) as ?child_count) (SAMPLE(?parent) as ?parent_id)
WHERE {{
    BIND(URI('{collection}') AS ?collection)
    ?collection a skos:Collection; skos:member ?id.

    ?id a skos:Concept;
        skos:prefLabel ?label;
        skos:definition ?definition .

    OPTIONAL {{ ?id skos:narrower ?child. }}
    OPTIONAL {{ ?id skos:broader ?parent }}
}}
GROUP BY ?id ?label ?definition
"""
)

GET_SORTED_COLLECTION_QUERY = (
    PREFIX
    + """
SELECT DISTINCT ?id ?label ?definition ?child_count ?parent_id {{
WHERE {{
    BIND(URI('{collection}') AS ?collection)
    ?collection skos:memberList ?list .
    ?list stardog:list:member (?id ?index) .

    ?id a skos:Concept;
    skos:prefLabel ?label;
    skos:definition ?definition .
}}
ORDER BY ?index
}}
"""
)

GET_CHILDREN_QUERY = (
    PREFIX
    + """
SELECT DISTINCT ?id ?label ?definition ?parent_id
WHERE {{
    ?parent_id skos:narrower ?id.
    VALUES ?parent {{ {concept} }}

    ?id a skos:Concept;
    skos:prefLabel ?label; skos:definition ?definition.
}}
"""
)

SUGGEST_BY_IDS_QUERY = (
    PREFIX
    + """
SELECT DISTINCT ?id ?label ?definition
WHERE {{
    ocol:thema skos:member ?thema.
    col:graad skos:member ?graad.
    col:vak skos:member ?id.

    ?id a skos:Concept;
        skos:prefLabel ?label;
        skos:definition ?definition;
        skos:related ?thema, ?graad.

    VALUES ?thema {{ {themas} }}
    VALUES ?graad {{ {graden} }}
}}
"""
)

GET_CONCEPT_BY_IDS_QUERY = (
    PREFIX
    + """
SELECT DISTINCT ?id ?label ?definition
WHERE {{
    ?id a skos:Concept;
    skos:prefLabel ?label; skos:definition ?definition .

    VALUES ?id {{ {concept} }}
}}
"""
)

GET_RELATED_VAK_QUERY = (
    PREFIX
    + """
SELECT DISTINCT ?id ?label ?definition
WHERE {{
    col:vak skos:member ?id.

    ?id a skos:Concept;
    skos:prefLabel ?label;
    skos:definition ?definition;
    skos:related ?concept.

    VALUES ?concept {{ {concept} }}
}}
"""
)


# Function to validate URL
# using regular expression
def is_valid_uri(value):

    # Compile the ReGex
    p = re.compile(URI_REGEX)

    # If the string is empty
    # return false
    if value is None:
        return False

    # Return if the string
    # matched the ReGex
    if re.search(p, value):
        return True

    return False


def join_ids(identifiers):
    for idx in identifiers:
        if not is_valid_uri(idx):
            raise ValueError(f"The id {idx} is not a valid URL.")

    return " ".join("<" + str(idx) + ">" for idx in identifiers)


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

    OND_NS = OND_NS
    EXT_NS = EXT_NS

    def __init__(self, endpoint: str, user: str, password: str):
        self.sparql = SPARQLWrapper2(endpoint)
        self.sparql.setMethod(POST)
        self.sparql.setCredentials(user, password)
        self.sparql.setReturnFormat(JSON)

    def __exec_query(self, query: str, **kwargs):
        formatted = query.format(**kwargs)
        print(formatted)
        self.sparql.setQuery(formatted)

        for binding in self.sparql.query().convert().bindings:
            r = {}
            for k, v in binding.items():
                if v.datatype == "http://www.w3.org/2001/XMLSchema#integer":
                    r[k] = int(v.value)
                else:
                    r[k] = v.value
            yield r

            # yield {k: v.value for k, v in result.items()}

    def get_concept(self, concept: List[str]):
        """Get thesaurus concept by ids."""

        for res in self.__exec_query(
            GET_CONCEPT_BY_IDS_QUERY, concept=join_ids(concept)
        ):
            yield res

    def get_collection(self, collection: str, is_sorted: bool = False):
        """Get a collection members by collection id."""

        if not is_valid_uri(collection):
            raise ValueError("The id {} is not a valid URI.".format(collection))

        query = GET_COLLECTION_QUERY
        if is_sorted:
            query = GET_SORTED_COLLECTION_QUERY

        for res in self.__exec_query(query, collection=collection):
            yield res

    def get_children(self, concept: List[str]):
        """Get the children of a list of concept ids."""

        for res in self.__exec_query(GET_CHILDREN_QUERY, concept=join_ids(concept)):
            yield res

    def get_vakken(self):
        """Get list 'vakken'."""

        for res in self.get_collection(f"{self.EXT_NS}collectie/vak", True):
            yield res

    def get_themas(self):
        """Get list 'themas'."""

        for res in self.get_collection(f"{self.OND_NS}collectie/thema", True):
            yield res

    def get_graden(self):
        """Get list 'onderwijsgraden'."""

        for res in self.get_collection(f"{self.EXT_NS}collectie/graad"):
            yield res

    def get_niveaus(self):
        """Get list 'onderwijsniveaus'."""

        for res in self.__exec_query(GET_NIVEAUS):
            yield res

    def suggest(self, thema: List[str], graad: List[str]):
        """Suggest 'vakken' based on the identifiers of 'onderwijsgraad' and 'thema'."""

        for res in self.__exec_query(
            SUGGEST_BY_IDS_QUERY,
            themas=join_ids(thema),
            graden=join_ids(graad),
        ):
            yield res

    def get_related_vak(self, concept: List[str]):
        """Get related vak by concept ids."""

        for res in self.__exec_query(GET_RELATED_VAK_QUERY, concept=join_ids(concept)):
            yield res

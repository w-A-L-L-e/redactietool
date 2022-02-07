#
# disable tests until this package works on our Jenkins/ci.meemoo.be
#

from app.services.suggest.Suggest import Suggest

# sparql-endpoint-fixture>=0.5.0


def test_instantiation():
    suggest = Suggest("http://localhost/", "x", "y")
    assert suggest


def test_get_concept(sparql_endpoint):
    # pylint: disable=unused-variable
    endpoint = sparql_endpoint(
        "https://my.rdfdb.com/repo/sparql", ["tests/fixture_data/skos.ttl"]
    )
    suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")

    results = list(suggest.get_concept([f"{suggest.OND_NS}vak/nederlands"]))
    assert len(results) == 1
    assert results[0] == {
        "definition": "lorem ipsum",
        "id": f"{suggest.OND_NS}vak/nederlands",
        "label": "Nederlands",
    }


def test_suggest_by_label(sparql_endpoint):
    # pylint: disable=unused-variable
    endpoint = sparql_endpoint(
        "https://my.rdfdb.com/repo/sparql", ["tests/fixture_data/skos.ttl"]
    )
    suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")

    results = list(suggest.suggest_by_label(
        ["Nederlandse taal"], ["Lager 1ste graad"]))
    assert len(results) == 1
    assert results[0] == {
        "definition": "lorem ipsum",
        "id": f"{suggest.OND_NS}vak/nederlands",
        "label": "Nederlands",
    }


def test_suggest(sparql_endpoint):
    # pylint: disable=unused-variable
    endpoint = sparql_endpoint(
        "https://my.rdfdb.com/repo/sparql", ["tests/fixture_data/skos.ttl"]
    )
    suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")

    results = list(
        suggest.suggest(
            [f"{suggest.OND_NS}thema/nederlandse-taal"],
            [f"{suggest.OND_NS}graad/lager-1ste-graad"],
        )
    )
    assert len(results) == 1
    assert results[0] == {
        "definition": "lorem ipsum",
        "id": f"{suggest.OND_NS}vak/nederlands",
        "label": "Nederlands",
    }


def test_get_candidates(sparql_endpoint):
    # pylint: disable=unused-variable
    endpoint = sparql_endpoint(
        "https://my.rdfdb.com/repo/sparql", ["tests/fixture_data/skos.ttl"]
    )
    suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")

    results = list(
        suggest.get_candidates(
            [f"{suggest.OND_NS}thema/nederlandse-taal"],
            [f"{suggest.OND_NS}graad/lager-1ste-graad"],
        )
    )
    assert len(results) == 2
    assert results[0] == {
        "definition": "lorem ipsum",
        "id": f"{suggest.OND_NS}vak/nederlands",
        "label": "Nederlands",
    }
    assert results[1] == {
        # pylint: disable=line-too-long
        "definition": "Identiteit, diversiteit, dialoog, mensenrechten, plichten, rechtstaat, democratie, politiek, stemrecht, participatie",
        "id": f"{suggest.OND_NS}vak/burgerschap",
        "label": "burgerschap",
    }


def test_get_graden(sparql_endpoint):
    # pylint: disable=unused-variable
    endpoint = sparql_endpoint(
        "https://my.rdfdb.com/repo/sparql", ["tests/fixture_data/skos.ttl"]
    )
    suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")

    results = list(suggest.get_graden())
    assert len(results) == 1
    assert results[0] == {
        "definition": "Lager 1ste graad",
        "id": f"{suggest.OND_NS}graad/lager-1ste-graad",
        "label": "Lager 1ste graad",
    }


def test_get_niveaus(sparql_endpoint):
    # pylint: disable=unused-variable
    endpoint = sparql_endpoint(
        "https://my.rdfdb.com/repo/sparql", ["tests/fixture_data/skos.ttl"]
    )
    suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")

    results = list(suggest.get_niveaus())
    assert len(results) == 1
    assert results[0] == {
        "definition": "Lager onderwijs",
        "id": f"{suggest.OND_NS}niveau/lager-onderwijs",
        "label": "Lager onderwijs",
    }


def test_get_themas(sparql_endpoint):
    # pylint: disable=unused-variable
    endpoint = sparql_endpoint(
        "https://my.rdfdb.com/repo/sparql", ["tests/fixture_data/skos.ttl"]
    )
    suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")

    results = list(suggest.get_themas())
    assert len(results) == 2
    assert results[0] == {
        "definition": "Taalkunde, exclusief literatuur, voor de Nederlandse taal",
        "id": f"{suggest.OND_NS}thema/nederlandse-taal",
        "label": "Nederlandse taal",
    }
    assert results[1] == {
        "definition": "Alles over rechtbanken, rechtspraak, criminaliteit, wetgeving, ...",
        "id": f"{suggest.OND_NS}thema/recht",
        "label": "Recht",
    }


def test_get_children(sparql_endpoint):
    # pylint: disable=unused-variable
    endpoint = sparql_endpoint(
        "https://my.rdfdb.com/repo/sparql", ["tests/fixture_data/skos.ttl"]
    )
    suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")

    results = list(suggest.get_children(
        [f"{suggest.OND_NS}niveau/lager-onderwijs"]))
    assert len(results) == 1
    assert results[0] == {
        "definition": "Lager 1ste graad",
        "id": f"{suggest.OND_NS}graad/lager-1ste-graad",
        "label": "Lager 1ste graad",
    }


def test_get_related(sparql_endpoint):
    # pylint: disable=unused-variable
    endpoint = sparql_endpoint(
        "https://my.rdfdb.com/repo/sparql", ["tests/fixture_data/skos.ttl"]
    )
    suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")

    results = list(suggest.get_related_vak(
        [f"{suggest.OND_NS}graad/lager-1ste-graad"]))
    assert len(results) == 2
    assert results[0] == {
        "definition": "lorem ipsum",
        "id": f"{suggest.OND_NS}vak/nederlands",
        "label": "Nederlands",
    }
    assert results[1] == {
        # pylint: disable=line-too-long
        "definition": "Identiteit, diversiteit, dialoog, mensenrechten, plichten, rechtstaat, democratie, politiek, stemrecht, participatie",
        "id": f"{suggest.OND_NS}vak/burgerschap",
        "label": "burgerschap",
    }

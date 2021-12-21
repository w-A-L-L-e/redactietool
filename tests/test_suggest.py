from app.services.suggest.Suggest import Suggest

# disable tests until this package works on our Jenkins/ci.meemoo.be
# sparql-endpoint-fixture>=0.5.0
# def test_instantiation():
#     suggest = Suggest("http://localhost/", "x", "y")
#     assert suggest
# 
# 
# def test_get_concept(sparql_endpoint):
#     # pylint: disable=unused-variable
#     endpoint = sparql_endpoint(
#         "https://my.rdfdb.com/repo/sparql", ["tests/data/skos.ttl"]
#     )
#     suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")
# 
#     results = list(
#         suggest.get_concept(["https://data.meemoo.be/terms/ond/vak#nederlands"])
#     )
#     assert len(results) == 1
#     assert results[0] == {
#         "definition": "lorem ipsum",
#         "id": "https://data.meemoo.be/terms/ond/vak#nederlands",
#         "label": "Nederlands",
#     }
# 
# 
# def test_suggest_by_label(sparql_endpoint):
#     # pylint: disable=unused-variable
#     endpoint = sparql_endpoint(
#         "https://my.rdfdb.com/repo/sparql", ["tests/data/skos.ttl"]
#     )
#     suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")
# 
#     results = list(suggest.suggest_by_label(["Nederlandse taal"], ["Lager 1ste graad"]))
#     assert len(results) == 1
#     assert results[0] == {
#         "definition": "lorem ipsum",
#         "id": "https://data.meemoo.be/terms/ond/vak#nederlands",
#         "label": "Nederlands",
#     }
# 
# 
# def test_suggest(sparql_endpoint):
#     # pylint: disable=unused-variable
#     endpoint = sparql_endpoint(
#         "https://my.rdfdb.com/repo/sparql", ["tests/data/skos.ttl"]
#     )
#     suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")
# 
#     results = list(
#         suggest.suggest(
#             ["https://data.meemoo.be/terms/ond/thema#nederlandse-taal"],
#             ["https://data.meemoo.be/terms/ond/graad#lager-1ste-graad"],
#         )
#     )
#     assert len(results) == 1
#     assert results[0] == {
#         "definition": "lorem ipsum",
#         "id": "https://data.meemoo.be/terms/ond/vak#nederlands",
#         "label": "Nederlands",
#     }
# 
# 
# def test_get_candidates(sparql_endpoint):
#     # pylint: disable=unused-variable
#     endpoint = sparql_endpoint(
#         "https://my.rdfdb.com/repo/sparql", ["tests/data/skos.ttl"]
#     )
#     suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")
# 
#     results = list(
#         suggest.get_candidates(
#             ["https://data.meemoo.be/terms/ond/thema#nederlandse-taal"],
#             ["https://data.meemoo.be/terms/ond/graad#lager-1ste-graad"],
#         )
#     )
#     assert len(results) == 1
#     assert results[0] == {
#         "definition": "lorem ipsum",
#         "id": "https://data.meemoo.be/terms/ond/vak#nederlands",
#         "label": "Nederlands",
#     }
# 
# 
# def test_get_graden(sparql_endpoint):
#     # pylint: disable=unused-variable
#     endpoint = sparql_endpoint(
#         "https://my.rdfdb.com/repo/sparql", ["tests/data/skos.ttl"]
#     )
#     suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")
# 
#     results = list(suggest.get_graden())
#     assert len(results) == 1
#     assert results[0] == {
#         "definition": "Lager 1ste graad",
#         "id": "https://data.meemoo.be/terms/ond/graad#lager-1ste-graad",
#         "label": "Lager 1ste graad",
#     }
# 
# 
# def test_get_niveaus(sparql_endpoint):
#     # pylint: disable=unused-variable
#     endpoint = sparql_endpoint(
#         "https://my.rdfdb.com/repo/sparql", ["tests/data/skos.ttl"]
#     )
#     suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")
# 
#     results = list(suggest.get_niveaus())
#     assert len(results) == 1
#     assert results[0] == {
#         "definition": "Lager onderwijs",
#         "id": "https://data.meemoo.be/terms/ond/niveau#lager-onderwijs",
#         "label": "Lager onderwijs",
#     }
# 
# 
# def test_get_themas(sparql_endpoint):
#     # pylint: disable=unused-variable
#     endpoint = sparql_endpoint(
#         "https://my.rdfdb.com/repo/sparql", ["tests/data/skos.ttl"]
#     )
#     suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")
# 
#     results = list(suggest.get_themas())
#     assert len(results) == 1
#     assert results[0] == {
#         "definition": "Taalkunde, exclusief literatuur, voor de Nederlandse taal",
#         "id": "https://data.meemoo.be/terms/ond/thema#nederlandse-taal",
#         "label": "Nederlandse taal",
#     }
# 
# 
# def test_get_children(sparql_endpoint):
#     # pylint: disable=unused-variable
#     endpoint = sparql_endpoint(
#         "https://my.rdfdb.com/repo/sparql", ["tests/data/skos.ttl"]
#     )
#     suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")
# 
#     results = list(
#         suggest.get_children("https://data.meemoo.be/terms/ond/niveau#lager-onderwijs")
#     )
#     assert len(results) == 1
#     assert results[0] == {
#         "definition": "Lager 1ste graad",
#         "id": "https://data.meemoo.be/terms/ond/graad#lager-1ste-graad",
#         "label": "Lager 1ste graad",
#     }
# 
# 
# def test_get_related(sparql_endpoint):
#     # pylint: disable=unused-variable
#     endpoint = sparql_endpoint(
#         "https://my.rdfdb.com/repo/sparql", ["tests/data/skos.ttl"]
#     )
#     suggest = Suggest("https://my.rdfdb.com/repo/sparql", "x", "y")
# 
#     results = list(
#         suggest.get_related_vak(
#             ["https://data.meemoo.be/terms/ond/graad#lager-1ste-graad"]
#         )
#     )
#     assert len(results) == 1
#     assert results[0] == {
#         "definition": "lorem ipsum",
#         "id": "https://data.meemoo.be/terms/ond/vak#nederlands",
#         "label": "Nederlands",
#     }

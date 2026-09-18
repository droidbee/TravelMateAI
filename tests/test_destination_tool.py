from tools.destination_tool import search_destinations


def test_search_by_country_and_interest():
    results = search_destinations.invoke({"country": "Italy", "interest": "relaxing"})
       
    assert len(results) == 2

    names = [destination["name"] for destination in results]

    assert "Amalfi Coast" in names
    assert "Lake Como" in names


def test_search_by_country():
    results = search_destinations.invoke({"country": "Spain"})
        
    

    assert len(results) == 1
    assert results[0]["name"] == "Barcelona"


def test_search_by_interest():
    results = search_destinations.invoke({"interest": "historical"})
        
    

    names = [destination["name"] for destination in results]

    assert "Florence" in names
    assert "Rome" in names


def test_search_with_no_matches():
    results = search_destinations.invoke({"country": "Italy", "interest": "adventure"})

    assert results == []


def test_search_without_filters():
    results = search_destinations.invoke({})

    assert len(results) == 6
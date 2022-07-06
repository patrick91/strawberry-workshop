def test_returns_none_when_there_is_no_podcast(client):
    response = client.post(
        "/graphql",
        data={"query": """{ podcast(id: "1") { title } }"""},
        content_type="application/json",
    )

    data = response.json()

    assert data == {"data": {"podcast": None}}

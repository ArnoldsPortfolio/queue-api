def auth(client):
    res = client.post("/auth/sign-up", json={"email": "ops@x.com", "password": "password1"})
    return {"Authorization": f"Bearer {res.json()['access_token']}"}
def test_submit_tick_done_and_dead(client):
    headers = auth(client)
    echo = client.post("/jobs", json={"kind": "echo", "payload": {"text": "hi"}, "idempotency_key": "a"}, headers=headers)
    again = client.post("/jobs", json={"kind": "echo", "payload": {"text": "other"}, "idempotency_key": "a"}, headers=headers)
    assert again.json()["id"] == echo.json()["id"]
    client.post("/worker/tick", headers=headers)
    assert client.get(f"/jobs/{echo.json()['id']}", headers=headers).json()["status"] == "done"
    fail = client.post("/jobs", json={"kind": "fail", "payload": {"message": "boom"}}, headers=headers).json()
    for _ in range(3):
        client.post("/worker/tick", headers=headers)
    dead = client.get(f"/jobs/{fail['id']}", headers=headers).json()
    assert dead["status"] == "dead"
    assert dead["attempts"] == 3
def test_public_key(client):
    headers = auth(client)
    issued = client.post("/keys", json={"name": "ci"}, headers=headers).json()
    res = client.post("/v1/jobs", json={"kind": "upper", "payload": {"text": "ok"}}, headers={"X-API-Key": issued["token"]})
    assert res.status_code == 200

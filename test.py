import pytest
import main
import uvicorn
import requests


def setup():
    main.parser_thread.start()
    uvicorn.run(
        app=main.app,
        host="localhost",
        port=8888
    )


def teardown():
    main.loop.stop()


def test_add_channel():
    resp = requests.post("http://localhost:8888/add-channel/forbesrussia/")
    assert resp.status_code // 10 == 20
    assert "forbesrussia" in main.channels.list


def test_del_channel():
    resp = requests.post("http://localhost:8888/del-channel/forbesrussia/")
    assert resp.status_code // 10 == 20
    assert not ("forbesrussia" in main.channels.list)
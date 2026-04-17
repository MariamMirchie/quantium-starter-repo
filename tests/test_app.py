import app


def test_header_is_present(dash_duo):
    dash_duo.start_server(app.app)
    header = dash_duo.find_element("h1")
    assert header is not None
    assert "Pink Morsels" in header.text


def test_visualisation_is_present(dash_duo):
    dash_duo.start_server(app.app)
    graph = dash_duo.find_element("#sales-line")
    assert graph is not None


def test_region_picker_is_present(dash_duo):
    dash_duo.start_server(app.app)
    region_picker = dash_duo.find_element("#region-radio")
    assert region_picker is not None
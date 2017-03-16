from vpr_alexa import programs


def test_vt_edition():
    vt_edition = programs.latest_vt_edition()
    assert 'https://cpa.ds.npr.org/vpr/audio/' in vt_edition.url
    assert len(vt_edition.title) > 0

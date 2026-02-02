from miniDXF import DXFDocument


def test_dxf_contains_entities_section():
    doc = DXFDocument()
    doc.line(0, 0, 10, 0)

    dxf = doc.to_dxf()

    assert "SECTION" in dxf
    assert "ENTITIES" in dxf
    assert "LINE" in dxf
    assert "EOF" in dxf

from miniDXF import DXFDocument


def test_bbox_simple():
    doc = DXFDocument()
    doc.line(10, 20, 110, 70)

    assert doc.bbox() == (10, 20, 110, 70)


def test_bbox_multiple_entities():
    doc = DXFDocument()
    doc.line(0, 0, 10, 10)
    doc.line(-5, 5, 5, 15)

    assert doc.bbox() == (-5, 0, 10, 15)

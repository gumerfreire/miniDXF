from miniDXF import DXFDocument

def test_move_to_origin():
    doc = DXFDocument()
    doc.line(-10, -20, 30, 40)

    doc.move_to_origin()

    assert doc.bbox() == (0, 0, 40, 60)

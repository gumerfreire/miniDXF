from miniDXF import DXFDocument


def test_rotate_90_deg():
    doc = DXFDocument()
    doc.line(0, 0, 10, 0)

    doc.rotate(90)

    min_x, min_y, max_x, max_y = doc.bbox()

    # Allow small floating point tolerance
    assert round(min_x, 6) == 0
    assert round(min_y, 6) == 0
    assert round(max_x, 6) == 0
    assert round(max_y, 6) == 10

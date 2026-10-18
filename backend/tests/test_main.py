from app.main import clean_json, extraction_prompt

def test_clean_json_fence():
    assert clean_json('```json\\n{"vendor":"Cafe"}\\n```')['vendor'] == 'Cafe'

def test_prompt_has_required_fields():
    p = extraction_prompt('Example receipt')
    assert 'line_items' in p and 'total' in p

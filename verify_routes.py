import json
from web import create_app
app = create_app('dev')
with app.test_request_context():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': str(rule)
        })
    print(json.dumps(routes, ensure_ascii=False, indent=2))

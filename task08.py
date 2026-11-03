# 8.1: Python classes store methods in a single namespace dictionary (__dict__), so defining search() a second time overwrites the first definition completely.
# 8.2: A mutable default like filters={} is created only once when the function is defined, so any later mutation of that dictionary persists across calls and causes shared-state bugs.
# 8.3: An optional filters: dict | None = None parameter is preferable over **kwargs because product attribute names might collide with future method parameters (like query, limit, or sort).
# 8.4: Running pyflakes on the original code reports: "redefinition of unused 'search' from line 5".

from __future__ import annotations


class ProductSearch:
    def __init__(self, products: list[dict]):
        self.products = products

    def search(self, query: str, filters: dict | None = None) -> list[dict]:
        q = query.lower()
        result = [p for p in self.products if q in p["title"].lower()]
        if filters is not None:
            for key, value in filters.items():
                result = [p for p in result if p.get(key) == value]
        return result


# --- Tests ---
def test_search_with_and_without_filters():
    products = [
        {"title": "iPhone 15", "brand": "Apple", "color": "black"},
        {"title": "iPhone 15 Case", "brand": "Spigen", "color": "black"},
    ]
    ps = ProductSearch(products)

    assert len(ps.search("iphone")) == 2
    assert ps.search("iphone", filters={"brand": "Apple"}) == [products[0]]

import requests
import sys

PROJECT_CODE = "products-s13"
GRAPHQL_URL = "http://localhost:8223/graphql"  

def build_payload(query: str, variables: dict) -> dict:
    """
    Формирует словарь для отправки GraphQL запроса.
    
    :param query: Текст запроса (query или mutation).
    :param variables: Словарь с переменными.
    :return: Словарь с ключами "query" и "variables".
    """
    return {"query": query, "variables": variables}

def execute_graphql(query: str, variables: dict = None):
    """Отправляет GraphQL запрос и обрабатывает ответ."""
    payload = build_payload(query, variables or {})
    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()  
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        return
    except ValueError:
        print("Ответ не является валидным JSON")
        return

    if "errors" in data:
        print("GraphQL вернул ошибки:")
        for error in data["errors"]:
            print(f"  - {error.get('message')}")
    if "data" in data:
        print("Полученные данные:")
        print(data["data"])

if __name__ == "__main__":
    query_products = """
    query {
        products {
            id
            name
            price
        }
    }
    """
    print("=== Выполняем запрос products ===")
    execute_graphql(query_products)

    mutation_create = """
    mutation($name: String!, $price: Float!) {
        createProduct(name: $name, price: $price) {
            id
            name
            price
        }
    }
    """
    variables = {"name": "Новый товар", "price": 123.45}
    print("\n=== Выполняем мутацию createProduct ===")
    execute_graphql(mutation_create, variables)
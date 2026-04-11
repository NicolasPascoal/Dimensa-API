import requests
from app.database.mongoDB import ip_collection

def fetch_ip_data(ip: str):
    url = f"https://ipwho.is/{ip}"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Erro ao acessar API externa")

    data = response.json()

    if not data.get("success", False):
        raise Exception("IP inválido ou não encontrado")

    return {
        "ip": data.get("ip"),
        "raw_data": data,
        "data": {
            "type": data.get("type"),
            "continent": data.get("continent"),
            "continent_code": data.get("continent_code"),
            "country": data.get("country"),
            "country_code": data.get("country_code"),
            "region": data.get("region"),
            "region_code": data.get("region_code"),
            "city": data.get("city"),
            "capital": data.get("capital"),
        }
    }


def create_ip(ip: str):
    existing = ip_collection.find_one({"ip": ip})

    if existing:
        print("Retornando do banco")

        existing["_id"] = str(existing["_id"])

        return existing

    print("Chamando API externa")
    data = fetch_ip_data(ip)

    ip_collection.insert_one(data)
    
    if "_id" in data:
        data["_id"] = str(data["_id"])

    return data


def get_ips(page: int = 1, limit: int = 15, filter_ip: str = ""):
    query = {}
    if filter_ip:
        query["ip"] = {"$regex": f"^{filter_ip}"}
    
    skip = (page - 1) * limit
    
    cursor = ip_collection.find(query).skip(skip).limit(limit)
    
    results = []
    for item in cursor:
        results.append({
            "ip": item.get("ip"),
            "data": item.get("data", {})
        })
        
    return results
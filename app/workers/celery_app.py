import time
from celery import Celery
from app.database.mongoDB import ip_collection
from app.controller.ip_service import fetch_ip_data
from config import Config

def create_celery():
    celery_app = Celery(
        "ip_workers",
        broker=Config.REDIS_URL,
        backend=Config.REDIS_URL
    )

    celery_app.conf.timezone = 'UTC'

    celery_app.conf.beat_schedule = {
        'atualiza-ips': {
            'task': 'app.workers.celery_app.update_all_ips_job',
            'schedule': 43200.0,
        },
    }

    return celery_app

celery = create_celery()

@celery.task
def update_all_ips_job():
    print("Iniciando job de atualização de IPs...")
    
    all_ips = list(ip_collection.find({}))
    total = len(all_ips)
    print(f"Total de IPs para atualizar: {total}")
    
    for item in all_ips:
        ip = item.get("ip")
        if ip:
            try:
                print(f"Atualizando IP: {ip}")
                new_data = fetch_ip_data(ip)
                
                if "_id" in new_data:
                    del new_data["_id"]
                    
                ip_collection.update_one(
                    {"ip": ip},
                    {"$set": new_data}
                )
            except Exception as e:
                print(f"Erro ao atualizar o IP {ip}: {str(e)}")
            
            time.sleep(1.1)
            
    print("Job finalizado e IPs atualizados.")

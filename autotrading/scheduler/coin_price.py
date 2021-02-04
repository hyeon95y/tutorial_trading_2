import os
import sys

from celery import Celery

from autotrading.db.mongodb import mongodb_handler
from autotrading.machine.korbit_machine import KorbitMachine
from autotrading.scheduler.coiner import Coiner

project_dir = os.path.abspath(os.getcwd())
sys.path.append(project_dir)


app = Celery(
    "get_coin_info",
    backend="redis://localhost:6379/0",
    broker="redis://localhost:6379/0",
)

app.conf.beat_schedule = {
    "add-every-1-min": {
        "task": "scheduler.coin_price.get_coin_info",
        "schedule": 59.0,
        "args": (),
    },
}


@app.task
def get_coin_info():
    korbit_machine = KorbitMachine()
    coiner = Coiner(korbit_machine)
    result_etc = coiner.get_filled_orders(coin_type="etc_krw")
    result_eth = coiner.get_filled_orders(coin_type="eth_krw")
    result_btc = coiner.get_filled_orders(coin_type="btc_krw")
    result_xrp = coiner.get_filled_orders(coin_type="xrp_krw")
    result_bch = coiner.get_filled_orders(coin_type="bch_krw")
    mongodb = mongodb_handler.MongoDbHandler("local", "coiner", "price_info")
    result_list = result_etc + result_eth + result_btc + result_xrp + result_bch
    mongodb.insert_items(result_list)

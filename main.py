import eel
import os
import base64
import threading
import time
from libs.logic import *

# Inicjalizacja Eel
eel.init('web')
backtester = Backtester()

@eel.expose
def execute_backtest(positions_file_name, positions_file_content, prices_file_name, prices_file_content, take_profit, stop_loss, spreadpips, invert):
    positions_file_path = save_file(positions_file_name, positions_file_content)
    prices_file_path = save_file(prices_file_name, prices_file_content)
    spreadpips = float(spreadpips)
    spreadpips = 10 ** -spreadpips

    log_message = (
        f"Positions file path: {positions_file_path}\n"
        f"Prices file path: {prices_file_path}\n"
        f"Take profit: {take_profit}\n"
        f"Stop loss: {stop_loss}\n"
        f"Spread pips: {spreadpips}\n"
        f"Invert: {invert}\n"
    )
    eel.block_output_name()
    eel.updateLog("Starting")
    eel.updateLog("---------")
    eel.updateLog(log_message)
    eel.updateLog("---------")
    backtester.setValues(invert, stop_loss, take_profit, spreadpips, positions_file_path, prices_file_path, eel.updateLog)
    backtester.runbacktester()
    eel.unlock_output_name()

def save_file(file_name, file_content):
    file_data = base64.b64decode(file_content.split(',')[1])
    file_path = os.path.join(os.getcwd(), file_name)

    with open(file_path, 'wb') as f:
        f.write(file_data)

    return file_path


eel.start('index.html')
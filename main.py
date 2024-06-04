import eel
import os
import base64
import threading
import time

# Inicjalizacja Eel
eel.init('web')

def log_test_message():
    while True:
        log_message = "Test message"
        print(log_message)
        eel.updateLog(log_message)
        time.sleep(1)

@eel.expose
def execute_backtest(positions_file_name, positions_file_content, prices_file_name, prices_file_content, take_profit, stop_loss, output_name):
    positions_file_path = save_file(positions_file_name, positions_file_content)
    prices_file_path = save_file(prices_file_name, prices_file_content)

    log_message = (
        f"Positions file path: {positions_file_path}\n"
        f"Prices file path: {prices_file_path}\n"
        f"Take profit: {take_profit}\n"
        f"Stop loss: {stop_loss}\n"
        f"Output name: {output_name}\n"
    )
    print(log_message)
    eel.updateLog(log_message)
    return log_message

def save_file(file_name, file_content):
    file_data = base64.b64decode(file_content.split(',')[1])
    file_path = os.path.join(os.getcwd(), file_name)

    with open(file_path, 'wb') as f:
        f.write(file_data)

    return file_path

@eel.expose
def start_logging():
    thread = threading.Thread(target=log_test_message)
    thread.daemon = True
    thread.start()

eel.start('index.html')

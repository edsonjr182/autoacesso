import os
import sys
import time
import tkinter as tk
from tkinter import scrolledtext
import csv
import random
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import threading
from queue import Queue

def resource_path(relative_path):
    """ Obtenha o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_proxies_from_csv(file_path):
    file_path = resource_path(file_path)
    
    proxies = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Https'] == 'yes':
                proxy = {
                    "http": f"http://{row['IP Address']}:{row['Port']}",
                    "https": f"https://{row['IP Address']}:{row['Port']}"
                }
                proxies.append(proxy)
    return proxies

def access_with_proxy(url, element_id, proxy_dict, queue):
    proxy_ip_port = proxy_dict['http'].replace('http://', '')
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': proxy_ip_port,
        'ftpProxy': proxy_ip_port,
        'sslProxy': proxy_ip_port,
        'noProxy': ''
    })

    options = webdriver.ChromeOptions()
    options.proxy = proxy
    driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver.exe')
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    try:
        driver.get(url)
        button = driver.find_element_by_id(element_id)
        button.click()

        time.sleep(random.randint(20, 120))

        queue.put(f"Acesso bem-sucedido usando proxy: {proxy_dict['http']}\n")

    except Exception as e:
        queue.put(f"Erro ao acessar {url} usando proxy: {proxy_dict['http']}. Erro: {str(e)}\n")

    finally:
        driver.quit()

def access_and_click(url, element_id, proxies, queue, run_event):
    if not proxies:
        queue.put("Não foi possível obter uma lista de proxies.\n")
        return

    while run_event.is_set():
        threads = []
        for _ in range(random.randint(3, 8)):
            proxy_dict = random.choice(proxies)
            t = threading.Thread(target=access_with_proxy, args=(url, element_id, proxy_dict, queue))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        time.sleep(60)

def write_csv(messages):
    with open('report.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Message"])
        for message in messages:
            writer.writerow([message])

def main_gui():
    root = tk.Tk()
    root.title("Teste de Acesso usando Proxies")
    
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    lbl_url = tk.Label(frame, text="URL do site:")
    lbl_url.pack(pady=5)
    
    entry_url = tk.Entry(frame, width=50)
    entry_url.pack(pady=5)
    entry_url.insert(0, "")

    lbl_id = tk.Label(frame, text="ID do Elemento para Clique:")
    lbl_id.pack(pady=5)
    
    entry_id = tk.Entry(frame, width=50)
    entry_id.pack(pady=5)
    entry_id.insert(0, "")

    lbl = tk.Label(frame, text="Log de Atividades:")
    lbl.pack(pady=5)

    text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=70, height=20)
    text_area.pack(pady=5)

    message_queue = Queue()
    messages = []

    def check_queue():
        while not message_queue.empty():
            message = message_queue.get_nowait()
            text_area.insert(tk.END, message)
            messages.append(message)
        root.after(100, check_queue)

    root.after(100, check_queue)

    run_event = threading.Event()

    def on_start_click():
        text_area.delete(1.0, tk.END)
        url = entry_url.get()
        element_id = entry_id.get()
        proxies = get_proxies_from_csv("proxies.csv")
        run_event.set()
        access_and_click_thread = threading.Thread(target=access_and_click, args=(url, element_id, proxies, message_queue, run_event))
        access_and_click_thread.start()
        btn_start.pack_forget()
        btn_pause.pack(pady=20)

    def on_pause_click():
        run_event.clear()
        write_csv(messages)
        btn_pause.pack_forget()
        btn_start.pack(pady=20)

    btn_start = tk.Button(frame, text="Iniciar Teste", command=on_start_click)
    btn_start.pack(pady=20)

    btn_pause = tk.Button(frame, text="Pausar", command=on_pause_click)

    root.mainloop()

if __name__ == "__main__":
    main_gui()

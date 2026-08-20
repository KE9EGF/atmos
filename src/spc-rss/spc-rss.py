running = True
while running:
    try:
        try:
            # Packages my beloved
            import sys
            import rich
            import httpx as hx
            import feedparser as fp
            from time import sleep
            from tqdm import tqdm
        except ImportError as e:
            print("Imports failed. Please ensure all libraries are installed.")
            print(e)
            sleep(2)
            sys.exit()
            
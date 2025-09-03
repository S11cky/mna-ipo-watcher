# -*- coding: utf-8 -*-
import logging
import os
from main import send_alerts

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    send_alerts()

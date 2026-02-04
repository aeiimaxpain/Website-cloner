#!/usr/bin/env python3
"""
Ethical Website Cloner
Author: Authorized Security Testing / Offline Analysis Tool

USE ONLY ON WEBSITES YOU OWN OR HAVE EXPLICIT PERMISSION TO TEST.
"""

import os
import time
import sys
import requests
import urllib.parse
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from tqdm import tqdm

HEADERS = {
    "User-Agent": "Mozilla/5.0 (EthicalCloner/1.0)"
}

CRAWL_DELAY = 1.0  # seconds


class EthicalCloner:
    def __init__(self, base_url):
        self.base_url = self.normalize_url(base_url)
        self.domain = urllib.parse.urlparse(self.base_url).netloc
        self.root_dir = self.domain
        self.visited = set()
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

        self.robot_parser = RobotFileParser()
        self.robot_parser.set_url(
            urllib.parse.urljoin(self.base_url, "/robots.txt")
        )
        self.robot_parser.read()

    def normalize_url(self, url):
        if not url.startswith("http"):
            url = "https://" + url
        return url.rstrip("/")

    def allowed(self, url):
        return self.robot_parser.can_fetch(HEADERS["User-Agent"], url)

    def save_file(self, path, content, binary=False):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        mode = "wb" if binary else "w"
        with open(path, mode, encoding=None if binary else "utf-8") as f:
            f.write(content)

    def local_path(self, url):
        parsed = urllib.parse.urlparse(url)
        path = parsed.path
        if path.endswith("/") or path == "":
            path += "index.html"
        return os.path.join(self.root_dir, path.lstrip("/"))

    def download_asset(self, url):
        try:
            r = self.session.get(url, timeout=10)
            r.raise_for_status()
            path = self.local_path(url)
            self.save_file(path, r.content, binary=True)
        except Exception:
            pass

    def process_html(self, url):
        if url in self.visited or not self.allowed(url):
            return

        self.visited.add(url)

        try:
            r = self.session.get(url, timeout=10)
            r.raise_for_status()
        except Exception:
            return

        soup = BeautifulSoup(r.text, "lxml")

        # Assets
        for tag, attr in [
            ("img", "src"),
            ("script", "src"),
            ("link", "href"),
        ]:
            for element in soup.find_all(tag):
                link = element.get(attr)
                if not link:
                    continue

                full_url = urllib.parse.urljoin(url, link)
                parsed = urllib.parse.urlparse(full_url)

                if parsed.netloc == self.domain:
                    self.download_asset(full_url)
                    element[attr] = os.path.relpath(
                        self.local_path(full_url),
                        os.path.dirname(self.local_path(url))
                    )

        # Save HTML
        self.save_file(self.local_path(url), soup.prettify())

        # Crawl internal links
        for a in soup.find_all("a", href=True):
            next_url = urllib.parse.urljoin(url, a["href"])
            if urllib.parse.urlparse(next_url).netloc == self.domain:
                time.sleep(CRAWL_DELAY)
                self.process_html(next_url)

    def start(self):
        print(f"[+] Target: {self.base_url}")
        print(f"[+] Output Folder: {self.root_dir}")
        os.makedirs(self.root_dir, exist_ok=True)
        self.process_html(self.base_url)
        print("[✓] Done. Offline copy created ethically.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ethical_cloner.py <domain>")
        sys.exit(1)

    target = sys.argv[1]
    cloner = EthicalCloner(target)
    cloner.start()
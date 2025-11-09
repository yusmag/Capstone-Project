#!/usr/bin/env python3
"""
Download all images referenced by <image:image><image:loc>...</image:loc></image:image>
from one or more XML sitemap URLs.

Usage:
  python download_sitemap_images.py "https://exilewakesurfing.com/sitemap_products_1.xml?from=8548733747444&to=8898413461748" -o images -w 12
"""

import argparse
import concurrent.futures as cf
import gzip
import os
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib
import mimetypes
import time
from typing import List, Optional, Tuple, Set

import requests
from requests.adapters import HTTPAdapter
try:
    # urllib3 >=1.26
    from urllib3.util.retry import Retry
    RETRY_KW = {"allowed_methods": frozenset(["GET", "HEAD"])}
except Exception:
    # older urllib3
    from urllib3.util.retry import Retry
    RETRY_KW = {"method_whitelist": frozenset(["GET", "HEAD"])}

import xml.etree.ElementTree as ET
from tqdm import tqdm

IMAGE_NS = "http://www.google.com/schemas/sitemap-image/1.1"
XML_TIMEOUT = 30
DL_TIMEOUT = 60

def make_session() -> requests.Session:
    sess = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        **RETRY_KW
    )
    # IMPORTANT: do NOT advertise 'br' (Brotli). Let requests handle gzip/deflate only.
    sess.headers.update({
        "User-Agent": "img-sitemap-downloader/1.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
    })
    sess.mount("http://", HTTPAdapter(max_retries=retries))
    sess.mount("https://", HTTPAdapter(max_retries=retries))
    return sess

def fetch_xml_bytes(sess: requests.Session, url: str) -> bytes:
    r = sess.get(url, timeout=XML_TIMEOUT)
    r.raise_for_status()

    # requests will auto-decompress gzip/deflate when Accept-Encoding excludes 'br'
    content = r.content

    # if server still lies and sends raw gzip
    enc = (r.headers.get("Content-Encoding", "") or "").lower()
    ctype = (r.headers.get("Content-Type", "") or "").lower()

    if enc == "gzip" and content[:2] == b"\x1f\x8b":
        try:
            content = gzip.decompress(content)
        except OSError:
            pass

    # Quick sanity check: XML should start with '<' (ignoring BOM/whitespace)
    head = content.lstrip()[:1]
    if head != b"<":
        # Dump a small debug preview so you can see what arrived
        preview = content[:300]
        with open("response_debug.bin", "wb") as f:
            f.write(content)
        raise RuntimeError(
            "Response is not XML (saved to response_debug.bin). "
            f"Content-Type: {ctype!r}, Content-Encoding: {enc!r}, "
            f"First bytes: {preview!r}"
        )

    return content

def parse_image_locs(xml_bytes: bytes) -> List[str]:
    root = ET.fromstring(xml_bytes)
    ns = {"image": IMAGE_NS}
    urls: Set[str] = set()

    # Proper namespace
    for img in root.findall(".//image:image", ns):
        loc = img.find("image:loc", ns)
        if loc is not None and loc.text:
            urls.add(loc.text.strip())

    # Fallback: any <loc> that looks like an image URL
    if not urls:
        for el in root.iter():
            tag_local = el.tag.split("}")[-1]
            if tag_local.lower() == "loc" and el.text:
                txt = el.text.strip()
                if txt.startswith("http") and any(ext in txt.lower()
                                                  for ext in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif")):
                    urls.add(txt)

    return sorted(urls)

def safe_filename_from_url(url: str, content_type: Optional[str] = None) -> str:
    parsed = urlsplit(url)
    name = Path(unquote(parsed.path)).name or "image"
    ext = Path(name).suffix.lower()
    if not ext:
        if content_type:
            guessed_ext = mimetypes.guess_extension(content_type.split(";")[0].strip()) or ""
            if guessed_ext:
                ext = guessed_ext
        if not ext:
            ext = ".jpg"
        name = name + ext

    h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    stem = Path(name).stem
    final = f"{stem}-{h}{ext}"
    final = "".join(c for c in final if c not in '<>:"/\\|?*')
    return final

def download_one(sess: requests.Session, url: str, out_dir: Path, rate_delay: float = 0.0) -> Tuple[str, Optional[str]]:
    try:
        with sess.get(url, stream=True, timeout=DL_TIMEOUT) as r:
            r.raise_for_status()
            ctype = r.headers.get("Content-Type", "")
            fname = safe_filename_from_url(url, ctype)
            fpath = out_dir / fname
            if fpath.exists() and fpath.stat().st_size > 0:
                return (url, str(fpath))
            with open(fpath, "wb") as f:
                for chunk in r.iter_content(chunk_size=1 << 15):
                    if chunk:
                        f.write(chunk)
        if rate_delay > 0:
            time.sleep(rate_delay)
        return (url, str(fpath))
    except Exception:
        return (url, None)

def main():
    ap = argparse.ArgumentParser(description="Download images referenced by <image:loc> in XML sitemaps.")
    ap.add_argument("sitemaps", nargs="+", help="One or more sitemap XML URLs (.xml or .xml.gz).")
    ap.add_argument("-o", "--out", default="images", help="Output directory (default: images)")
    ap.add_argument("-w", "--workers", type=int, default=8, help="Concurrent downloads (default: 8)")
    ap.add_argument("--delay", type=float, default=0.0, help="Optional per-download delay (seconds)")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    sess = make_session()

    all_urls: List[str] = []
    for sm_url in args.sitemaps:
        xml_bytes = fetch_xml_bytes(sess, sm_url)
        urls = parse_image_locs(xml_bytes)
        if not urls:
            print("[WARN] No <image:loc> entries found in:", sm_url)
        all_urls.extend(urls)

    # De-dup preserving order
    seen = set()
    uniq_urls = [u for u in all_urls if not (u in seen or seen.add(u))]
    if not uniq_urls:
        print("No image URLs found. Nothing to download.")
        return

    print(f"Found {len(uniq_urls)} image URLs. Starting downloads to '{out_dir}'...")

    results: List[Tuple[str, Optional[str]]] = []
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = [ex.submit(download_one, sess, url, out_dir, args.delay) for url in uniq_urls]
        for fut in tqdm(cf.as_completed(futures), total=len(futures), unit="img"):
            results.append(fut.result())

    ok = [p for (_, p) in results if p is not None]
    fail = [u for (u, p) in results if p is None]
    print(f"Downloaded {len(ok)} images to: {out_dir}")
    if fail:
        print(f"Failed ({len(fail)}):")
        for u in fail[:20]:
            print("  -", u)
        if len(fail) > 20:
            print("  ... (truncated)")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Deploy a dist directory to the Cloudflare Pages project 'mischief-portal'
using the Pages direct-upload API. Account-level calls go through Muse's
surrogate credential helper (same as bin/cf.py); asset calls use the
short-lived upload JWT. Usage: python3 deploy.py <dist-dir> [branch]"""
import base64, json, mimetypes, os, sys, urllib.request, uuid
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response
import blake3

ACCT = "95f9d4d4b30ddd165f0ce16e9cf15f82"
import os
PROJECT = os.environ.get("PAGES_PROJECT", "software")
API = "https://api.cloudflare.com/client/v4"

def surrogate_req(method, url, data=None, ctype="application/json"):
    body = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(url, data=body, method=method)
    if body: r.add_header("Content-Type", ctype)
    add_surrogate_to_request(r, "custom.cloudflare", allowed_hosts=["api.cloudflare.com"])
    with urllib.request.urlopen(r, timeout=120) as resp:
        return read_json_response(resp)

def jwt_req(method, url, jwt, data=None):
    body = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(url, data=body, method=method)
    r.add_header("Authorization", f"Bearer {jwt}")
    if body: r.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(r, timeout=300) as resp:
        return json.loads(resp.read().decode())

def hash_file(path):
    with open(path, "rb") as f: raw = f.read()
    ext = os.path.splitext(path)[1].lstrip(".")
    return blake3.blake3(base64.b64encode(raw) + ext.encode()).hexdigest()[:32], raw

def main():
    dist = sys.argv[1]
    branch = sys.argv[2] if len(sys.argv) > 2 else "main"
    files = {}
    for root, _, names in os.walk(dist):
        for n in names:
            full = os.path.join(root, n)
            rel = "/" + os.path.relpath(full, dist).replace(os.sep, "/")
            h, raw = hash_file(full)
            files[rel] = (h, full, raw)
    print(f"{len(files)} files hashed")
    tok = surrogate_req("GET", f"{API}/accounts/{ACCT}/pages/projects/{PROJECT}/upload-token")
    jwt = tok["result"]["jwt"]
    hashes = [v[0] for v in files.values()]
    missing = jwt_req("POST", f"{API}/pages/assets/check-missing", jwt, {"hashes": hashes})
    missing_set = set(hashes)  # forced: prior upload stored base64 text
    print(f"missing assets to upload: {len(missing_set)}")
    if missing_set:
        payload = []
        for rel, (h, full, raw) in files.items():
            if h in missing_set:
                payload.append({"key": h, "value": base64.b64encode(raw).decode(),
                                "metadata": {"contentType": mimetypes.guess_type(full)[0] or "application/octet-stream"}, "base64": True})
        jwt_req("POST", f"{API}/pages/assets/upload", jwt, payload)
        print(f"uploaded {len(payload)} assets")
    jwt_req("POST", f"{API}/pages/assets/upsert-hashes", jwt, {"hashes": hashes})
    headers_txt = None
    redirects_txt = None
    if "/_headers" in files:
        headers_txt = files["/_headers"][2].decode()
    if "/_redirects" in files:
        redirects_txt = files["/_redirects"][2].decode()
    manifest = {rel: v[0] for rel, v in files.items()}
    # deployment create = multipart with manifest field (surrogate auth)
    boundary = "----zqmlabs" + uuid.uuid4().hex
    parts = []
    parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"manifest\"\r\n\r\n{json.dumps(manifest)}\r\n".encode())
    parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"branch\"\r\n\r\n{branch}\r\n".encode())
    if headers_txt is not None:
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"_headers\"\r\n\r\n{headers_txt}\r\n".encode())
    if redirects_txt is not None:
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"_redirects\"\r\n\r\n{redirects_txt}\r\n".encode())
    parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"commit_hash\"\r\n\r\n76b790fe48884e9c027da955174a9fc4f4ffdfd3\r\n".encode())
    parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"commit_message\"\r\n\r\nZ's Zoo bestiary v1 — approved text, first deployment\r\n".encode())
    parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"commit_dirty\"\r\n\r\nfalse\r\n".encode())
    parts.append(f"--{boundary}--\r\n".encode())
    body = b"".join(parts)
    r = urllib.request.Request(f"{API}/accounts/{ACCT}/pages/projects/{PROJECT}/deployments",
                               data=body, method="POST")
    r.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    add_surrogate_to_request(r, "custom.cloudflare", allowed_hosts=["api.cloudflare.com"])
    with urllib.request.urlopen(r, timeout=300) as resp:
        dep = read_json_response(resp)
    res = dep.get("result") or {}
    print("deployment:", res.get("id"), "| url:", res.get("url"), "| stage:", (res.get("latest_stage") or {}).get("name"), (res.get("latest_stage") or {}).get("status"))

if __name__ == "__main__":
    main()

# 🔐 Central Bank Encrypted API Integration

> AES-256 Encryption + Digital Signature + FastAPI  
> Built by [Tajudeen Jalaudin](https://github.com/Tajudeenj)

## Overview

Demonstrates the **AES-256-CBC encryption + HMAC-SHA256 digital signature** pattern used in UAE Central Bank (CBUAE) API integrations. Achieves sub-second payment flow performance. Based on a live production delivery at ADIB in 2024.

## Features

- AES-256-CBC payload encryption
- HMAC-SHA256 digital signature
- Tamper detection on decrypt
- Sub-second latency design
- REST API (FastAPI)

## Quick Start

```bash
git clone https://github.com/Tajudeenj/central-bank-encrypted-api.git
cd central-bank-encrypted-api
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## Flow

```
Payment Request → AES-256 Encrypt → HMAC Sign → POST to CBUAE
CBUAE Response → Verify Signature → AES Decrypt → Process Payment
```

## Related Skills

`AES Encryption` `Digital Signature` `HMAC` `Central Bank Integration` `UAE CBUAE` `Oracle OIC` `FastAPI`

---
*Part of the [Tajudeen Jalaudin](https://github.com/Tajudeenj) Banking Tech Portfolio*

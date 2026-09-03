# MirzaBot Pro vs Free — Differences and Installation

## Two Repos

| Repo | Version | Notes |
|------|---------|-------|
| `mahdiMGF2/mirza_pro` | Free/Basic | Simpler, fewer panels |
| `mahdiMGF2/mirzabot` | Pro | More panels, payment gateways, pro features |

Both repos are by the same author (mahdiMGF2).

## What's Different in Pro

### Supported Panels (Pro adds)
- Marzneshin, S-UI, Hiddify, MikroTik, IBSng, Pasarguard

### Payment Gateways (Pro)
- Card-to-Card (manual approval)
- NowPayments, Plisio, cubpay (crypto)
- Zarinpal, Aqayepardakht, IranPay (Iranian gateways)

## Config
Same config.php structure as MirzaPro2:
- `$APIKEY`, `$adminnumber`, `$domainhosts`, `$usernamebot`
- Same DB schema, same table.php approach

## .htaccess Differences (CRITICAL)

### Free version
```apache
RewriteCond %{DOCUMENT_ROOT}/install/index.php -f
```
Blocks if `install/index.php` exists.

### Pro version
```apache
RewriteCond %{DOCUMENT_ROOT}/install/.installed !-f
```
Blocks if `.installed` does NOT exist.

**Problem:** After `mirzaEnsureInstallerRemoved()` runs, install/ is deleted, so `.installed` check fails and blocks everything with 403. Fix: remove install gate entirely after installation.

### Recommended safe .htaccess (both versions)
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME}.php -f
RewriteRule ^([^/]+)$ $1.php [L]
RewriteCond %{THE_REQUEST} \s/+(.+?)\.php[\s?] [NC]
RewriteRule ^ /%1 [R=301,L]
SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1
# ... file blocking rules (*.txt, *.sh, *.json, etc.)
```

## Webhook URL — .php Stripping (CRITICAL)

The .htaccess RewriteRule strips `.php` from URLs (301 redirect). Telegram webhook must use URL **without** `.php`:
```bash
# WRONG — 301 redirect, Telegram ignores
curl -s ".../setWebhook?url=https://domain/index.php"
# CORRECT
curl -s ".../setWebhook?url=https://domain/index"
```

## install.sh requires Ubuntu
Official install script requires Ubuntu 22.04/24.04. Manual install works fine on Debian 13.

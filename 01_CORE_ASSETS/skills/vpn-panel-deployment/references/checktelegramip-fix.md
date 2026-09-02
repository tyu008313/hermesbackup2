# Critical Fix: checktelegramip() for Cloudflare Tunnel

## Problem
When using Cloudflare Quick Tunnel, Telegram webhook requests arrive from localhost (REMOTE_ADDR = ::1 or 127.0.0.1). The original `checktelegramip()` function only accepts Telegram's IP ranges, so all webhook requests are silently rejected.

## Symptoms
- `getWebhookInfo` shows `ok: true`, `pending_update_count: 0`
- User sends /start but bot does not respond
- No error in logs (silent failure)
- `last_message_time` updates in database but no message sent

## Fix
Replace the `checktelegramip()` function in `/var/www/mirza_pro/function.php` (around line 1593) with:

```php
function checktelegramip()
{
    // Allow localhost requests (Cloudflare Tunnel proxy)
    $clientIp = $_SERVER['REMOTE_ADDR'] ?? '';
    if ($clientIp === '127.0.0.1' || $clientIp === '::1' || $clientIp === '::ffff:127.0.0.1') {
        return true;
    }

    // Check CF-Connecting-IP header (Cloudflare)
    $cfIp = $_SERVER['HTTP_CF_CONNECTING_IP'] ?? '';
    if (!empty($cfIp) && filter_var($cfIp, FILTER_VALIDATE_IP)) {
        $clientIp = $cfIp;
    }

    if (!is_string($clientIp) || $clientIp === '') {
        return false;
    }

    $clientIp = trim($clientIp);
    if (!filter_var($clientIp, FILTER_VALIDATE_IP)) {
        return false;
    }

    $telegramIpRanges = [
        ['lower' => '149.154.160.0', 'upper' => '149.154.175.255'],
        ['lower' => '91.108.4.0', 'upper' => '91.108.7.255'],
        ['lower' => '2001:67c:4e8::', 'upper' => '2001:67c:4e8:ffff:ffff:ffff:ffff:ffff']
    ];

    foreach ($telegramIpRanges as $range) {
        if (isClientIpInRange($clientIp, $range['lower'], $range['upper'])) {
            return true;
        }
    }

    return false;
}
```

## Why This Works
- Cloudflare Tunnel connects to localhost:80, so REMOTE_ADDR is always localhost
- The fix whitelists localhost IPs before checking Telegram ranges
- CF-Connecting-IP header provides the real client IP when available
- Original Telegram IP check is preserved as fallback

## When to Apply
- Always apply when using Cloudflare Quick Tunnel
- Safe to apply even with direct connections (localhost check is additive)

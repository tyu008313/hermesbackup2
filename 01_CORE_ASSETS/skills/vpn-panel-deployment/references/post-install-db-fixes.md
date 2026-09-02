# Post-Install Database Fixes for MirzaPro2

## Problem 1: Admin ID Placeholder

After installation, the `admin` table may contain placeholder values instead of the actual admin Telegram ID.

### Symptoms
- Bot receives webhook but admin cannot access admin panel
- Admin commands don't work

### Fix
```sql
-- Check current admin ID
mysql -e "USE mirza_pro; SELECT * FROM admin;"

-- Update to actual admin ID
mysql -e "USE mirza_pro; UPDATE admin SET id_admin='ACTUAL_ADMIN_ID' WHERE id_admin='YOUR_TELEGRAM_ID_HERE';"
```

## Problem 2: New User Blocked by roll_Status

### Symptoms
- New user sends /start
- Bot sends rules message but user cannot proceed
- User's roll_Status is 0

### Fix
```sql
-- For admin user
mysql -e "USE mirza_pro; UPDATE user SET roll_Status=1, joinchannel='active' WHERE id=ADMIN_ID;"

-- For all users (if needed)
mysql -e "USE mirza_pro; UPDATE user SET roll_Status=1 WHERE roll_Status=0;"
```

## Problem 3: joinchannel Not Active

### Symptoms
- Bot asks user to join channel
- No channels are configured in database

### Fix
```sql
-- Check channels
mysql -e "USE mirza_pro; SELECT * FROM channels;"

-- If no channels needed, set user as active
mysql -e "USE mirza_pro; UPDATE user SET joinchannel='active' WHERE id=USER_ID;"
```

## Verification
```sql
-- Check user status
mysql -e "USE mirza_pro; SELECT id, username, step, verify, roll_Status, joinchannel FROM user;"

-- Check admin
mysql -e "USE mirza_pro; SELECT * FROM admin;"
```

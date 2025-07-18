-- SQL commands to manually verify users through pgAdmin

-- 1. View all users and their verification status
SELECT 
    id,
    username,
    email,
    email_verified,
    status,
    created_at
FROM users
ORDER BY created_at DESC;

-- 2. View all verification tokens
SELECT 
    id,
    user_id,
    token,
    token_type,
    used,
    expires_at,
    created_at
FROM verification_tokens
ORDER BY created_at DESC;

-- 3. Manually verify a user by email (replace with actual email)
-- UPDATE users 
-- SET email_verified = true, status = 'active' 
-- WHERE email = 'your-email@example.com';

-- 4. Mark verification token as used (replace with actual token)
-- UPDATE verification_tokens 
-- SET used = true 
-- WHERE token = 'your-verification-token';

-- 5. View a specific user with their verification token
-- SELECT 
--     u.id,
--     u.username,
--     u.email,
--     u.email_verified,
--     u.status,
--     vt.token,
--     vt.used as token_used,
--     vt.expires_at
-- FROM users u
-- LEFT JOIN verification_tokens vt ON u.id = vt.user_id
-- WHERE u.email = 'your-email@example.com';
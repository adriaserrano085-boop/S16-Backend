const { Client } = require('pg');
require('dotenv').config();

async function debugUser() {
    const client = new Client({
        connectionString: process.env.DATABASE_URL,
        ssl: { rejectUnauthorized: false }
    });

    try {
        await client.connect();
        console.log('--- DATABASE DEBUG: USER PROFILE ---');

        const res = await client.query(
            "SELECT id, email, role, length(hashed_password) as hash_len, LEFT(hashed_password, 10) as hash_start FROM users WHERE email ILIKE 'adriserrajime@gmail.com'"
        );

        if (res.rows.length > 0) {
            console.log('User found:');
            console.table(res.rows);

            // Log exactly the email string to check for spaces
            console.log(`Email check: '${res.rows[0].email}' (length: ${res.rows[0].email.length})`);
        } else {
            console.log('User adriserrajime@gmail.com NOT FOUND in database.');

            console.log('Listing first 5 users:');
            const allUsers = await client.query("SELECT email FROM users LIMIT 5");
            console.table(allUsers.rows);
        }
    } catch (err) {
        console.error('Debug error:', err);
    } finally {
        await client.end();
    }
}

debugUser();

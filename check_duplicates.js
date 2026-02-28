const { Client } = require('pg');
require('dotenv').config();

async function checkDuplicates() {
    const client = new Client({
        connectionString: process.env.DATABASE_URL,
        ssl: { rejectUnauthorized: false }
    });

    try {
        await client.connect();
        const res = await client.query(
            "SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1"
        );

        if (res.rows.length > 0) {
            console.log('Duplicate emails found:');
            console.table(res.rows);
        } else {
            console.log('No duplicate emails found.');
        }

        const allUserDetails = await client.query(
            "SELECT id, email, role FROM users WHERE email ILIKE 'adriserrajime@gmail.com'"
        );
        console.log('All users with adriserrajime@gmail.com (case-insensitive):');
        console.table(allUserDetails.rows);

    } catch (err) {
        console.error('Debug error:', err);
    } finally {
        await client.end();
    }
}

checkDuplicates();

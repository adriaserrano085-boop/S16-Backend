const { Client } = require('pg');
require('dotenv').config();

const oldUrl = process.env.OLD_DATABASE_URL;
const newUrl = process.env.DATABASE_URL;

async function checkSchema(url, name) {
    const client = new Client({ connectionString: url });
    try {
        await client.connect();
        console.log(`\n--- Schema for ${name} ---`);
        const tables = ['estadisticas_partido', 'estadisticas_jugador'];
        for (const t of tables) {
            console.log(`\nTable: ${t}`);
            // Columns
            const colRes = await client.query(`
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = $1 
                ORDER BY ordinal_position
            `, [t]);
            console.log('Columns:');
            colRes.rows.forEach(r => console.log(`  ${r.column_name} (${r.data_type})`));

            // Constraints (PK, Unique)
            const conRes = await client.query(`
                SELECT conname, pg_get_constraintdef(c.oid) as def
                FROM pg_constraint c 
                JOIN pg_namespace n ON n.oid = c.connamespace 
                WHERE nspname = 'public' 
                AND conrelid = $1::regclass
            `, [t]);
            console.log('Constraints:');
            conRes.rows.forEach(r => console.log(`  ${r.conname}: ${r.def}`));
        }
    } catch (e) {
        console.error(`Error checking ${name}: ${e.message}`);
    } finally {
        await client.end();
    }
}

async function run() {
    await checkSchema(oldUrl, 'Supabase (Old)');
    await checkSchema(newUrl, 'Neon (New)');
}

run();

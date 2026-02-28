const { Client } = require('pg');
require('dotenv').config();

const oldUrl = process.env.OLD_DATABASE_URL;
const newUrl = process.env.DATABASE_URL;

async function getCount(url, table) {
    const client = new Client({ connectionString: url });
    try {
        await client.connect();
        const res = await client.query(`SELECT COUNT(*) FROM ${table}`);
        await client.end();
        return res.rows[0].count;
    } catch (e) {
        if (client) await client.end();
        return `Error: ${e.message}`;
    }
}

async function run() {
    const tables = ['estadisticas_partido', 'estadisticas_jugador'];
    console.log('--- Counts Comparison ---');
    for (const t of tables) {
        const oldC = await getCount(oldUrl, t);
        const newC = await getCount(newUrl, t);
        console.log(`${t}: Old=${oldC}, New=${newC}`);
    }
}

run();

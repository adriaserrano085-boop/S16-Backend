const { Client } = require('pg');

const connectionString = "postgresql://neondb_owner:npg_U0vCalO7zufg@ep-bold-recipe-alp1x8ep-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require";

async function checkCounts() {
    const client = new Client({ connectionString });
    try {
        await client.connect();
        console.log("Connected to Neon DB.");

        const tables = [
            'asistencia',
            'estadisticas_partido',
            'partidos',
            'entrenamientos',
            'rivales',
            'jugadores_propios',
            'Staff',
            'familias'
        ];

        for (const table of tables) {
            try {
                // Determine if table needs quotes (like Staff)
                const tableName = (table === 'Staff') ? '"Staff"' : table;
                const res = await client.query(`SELECT COUNT(*) FROM ${tableName}`);
                console.log(`${table}: ${res.rows[0].count}`);
            } catch (err) {
                console.log(`${table}: Error or not found (${err.message})`);
            }
        }

    } catch (err) {
        console.error("Connection error:", err.message);
    } finally {
        await client.end();
    }
}

checkCounts();

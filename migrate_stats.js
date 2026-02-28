const { Client } = require('pg');
require('dotenv').config();

const oldUrl = process.env.OLD_DATABASE_URL;
const newUrl = process.env.DATABASE_URL;

async function migrateTable(tableName, sourceClient, destClient) {
    console.log(`📦 Migrando tabla: ${tableName}...`);
    try {
        // Fetch all rows from source
        const res = await sourceClient.query(`SELECT * FROM public.${tableName}`);
        const rows = res.rows;
        const columns = res.fields.map(f => f.name);

        if (rows.length === 0) {
            console.log(`  ⚠️ No se encontraron registros en ${tableName}.`);
            return;
        }

        console.log(`  Found ${rows.length} rows in source.`);

        // Column mapping for estadisticas_partido
        const columnMap = {
            'partido': 'partido_id',
            'partido_externo': 'partido_externo_id'
        };

        // Upsert each row into destination
        let count = 0;
        for (const row of rows) {
            const keys = Object.keys(row).map(k => (tableName === 'estadisticas_partido' && columnMap[k]) ? columnMap[k] : k);
            const values = Object.values(row);
            const placeholders = keys.map((_, i) => `$${i + 1}`).join(', ');
            const updateClause = keys.map((key, i) => `${key} = EXCLUDED.${key}`).join(', ');

            const query = {
                text: `
                    INSERT INTO ${tableName} (${keys.join(', ')})
                    VALUES (${placeholders})
                    ON CONFLICT (id) DO UPDATE SET ${updateClause}
                `,
                values: values
            };

            await destClient.query(query);
            count++;
        }
        console.log(`✅ Migrados/Actualizados ${count} registros en ${tableName}.`);
    } catch (e) {
        console.error(`❌ Error migrando ${tableName}: ${e.message}`);
    }
}

async function run() {
    if (!oldUrl || !newUrl) {
        console.error("❌ Error: Faltan URLs de base de datos en .env");
        process.exit(1);
    }

    const sourceClient = new Client({ connectionString: oldUrl, connectionTimeoutMillis: 10000 });
    const destClient = new Client({ connectionString: newUrl, connectionTimeoutMillis: 10000 });

    try {
        console.log("Connecting to source...");
        await sourceClient.connect();
        console.log("Connecting to destination...");
        await destClient.connect();
        console.log("🚀 Iniciando migración de estadísticas...");

        const tables = ['estadisticas_partido', 'estadisticas_jugador'];
        for (const table of tables) {
            await migrateTable(table, sourceClient, destClient);
        }

        console.log("\n✨ Proceso de migración completado.");
    } catch (e) {
        console.error("Critical error during migration:", e.message);
    } finally {
        await sourceClient.end();
        await destClient.end();
    }
}

run();

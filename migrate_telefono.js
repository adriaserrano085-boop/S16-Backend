
const { Client } = require('pg');

async function migrateType() {
    const client = new Client({
        connectionString: "postgresql://neondb_owner:npg_U0vCalO7zufg@ep-bold-recipe-alp1x8ep-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require"
    });

    try {
        await client.connect();
        console.log("Connected to DB");

        // 1. Alter column type to VARCHAR
        // We use USING to convert existing numeric to string and trim the .0
        await client.query(`
            ALTER TABLE jugadores_propios 
            ALTER COLUMN "Telefono" TYPE VARCHAR(50) 
            USING (CASE WHEN "Telefono" IS NULL THEN NULL ELSE REPLACE("Telefono"::TEXT, '.0', '') END);
        `);

        console.log("Column 'Telefono' migrated to VARCHAR(50) successfully.");

    } catch (err) {
        console.error("Migration error:", err);
    } finally {
        await client.end();
    }
}

migrateType();

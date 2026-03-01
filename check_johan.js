
const { Client } = require('pg');

async function checkPlayer() {
    const client = new Client({
        connectionString: "postgresql://neondb_owner:npg_U0vCalO7zufg@ep-bold-recipe-alp1x8ep-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require"
    });

    try {
        await client.connect();
        console.log("Connected to DB");

        const res = await client.query("SELECT id, nombre, apellidos, \"Telefono\", email FROM jugadores_propios WHERE nombre ILIKE '%Johan%' LIMIT 5;");
        console.log("Players found:");
        console.table(res.rows);

    } catch (err) {
        console.error(err);
    } finally {
        await client.end();
    }
}

checkPlayer();

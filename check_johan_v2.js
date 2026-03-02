
const { Client } = require('pg');

async function checkJohan() {
    const client = new Client({
        connectionString: "postgresql://neondb_owner:npg_U0vCalO7zufg@ep-bold-recipe-alp1x8ep-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require"
    });
    try {
        await client.connect();
        const res = await client.query("SELECT * FROM jugadores_propios WHERE nombre = 'Johan' OR apellidos = 'Johan'");
        console.log(JSON.stringify(res.rows, null, 2));
    } finally {
        await client.end();
    }
}

checkJohan();

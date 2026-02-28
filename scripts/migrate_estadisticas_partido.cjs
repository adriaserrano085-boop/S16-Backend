const { Client } = require('pg');
const client = new Client({
    connectionString: 'postgresql://neondb_owner:npg_U0vCalO7zufg@ep-bold-recipe-alp1x8ep-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require'
});

async function run() {
    await client.connect();
    try {
        console.log('Altering estadisticas_partido.partido_id and partido_externo_id to UUID...');
        await client.query(`ALTER TABLE estadisticas_partido ALTER COLUMN partido_id TYPE uuid USING partido_id::uuid`);
        await client.query(`ALTER TABLE estadisticas_partido ALTER COLUMN partido_externo_id TYPE uuid USING partido_externo_id::uuid`);
        console.log('Success!');
    } catch (e) {
        console.error(e);
    }
    await client.end();
}
run();

const { Client } = require('pg');

const client = new Client({
    connectionString: 'postgresql://neondb_owner:npg_U0vCalO7zufg@ep-bold-recipe-alp1x8ep-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require'
});

async function run() {
    await client.connect();
    try {
        console.log('Altering columnas a UUID...');
        await client.query(`ALTER TABLE entrenamientos ALTER COLUMN evento TYPE uuid USING evento::uuid`);
        console.log('Conversion of entrenamientos.evento successful!');
    } catch (err) {
        console.error('Error:', err);
    } finally {
        await client.end();
    }
}

run();

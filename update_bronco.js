const { Client } = require('pg');

const client = new Client({
    connectionString: 'postgresql://neondb_owner:npg_U0vCalO7zufg@ep-bold-recipe-alp1x8ep-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
});

async function run() {
    try {
        await client.connect();

        // Find players matching criteria
        const playersQuery = `
      SELECT id, nombre, apellidos FROM jugadores_propios
      WHERE nombre ILIKE '%Adrian%'
         OR nombre ILIKE '%Alex%'
         OR nombre ILIKE '%Alexis%'
         OR nombre ILIKE '%Xavi%'
         OR nombre ILIKE '%Victor%'
    `;
        const playersRes = await client.query(playersQuery);
        const validIds = playersRes.rows.map(r => r.id);
        console.log(`Found ${validIds.length} players modifying Bronco test.`);

        if (validIds.length > 0) {
            // Update tests
            const updateQuery = `
        UPDATE "pruebas_fisicas"
        SET broncotest_20m = broncotest, broncotest = NULL
        WHERE fecha = '2025-11-01'
          AND broncotest IS NOT NULL
          AND jugador_id = ANY($1::uuid[])
      `;
            const updateRes = await client.query(updateQuery, [validIds]);
            console.log(`Updated ${updateRes.rowCount} physical tests.`);
        }

    } catch (err) {
        console.error('Error:', err);
    } finally {
        await client.end();
    }
}

run();

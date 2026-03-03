const { Client } = require('pg');
const crypto = require('crypto');

const connectionString = "postgresql://neondb_owner:npg_U0vCalO7zufg@ep-bold-recipe-alp1x8ep-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require";

const data = [
    { name: "Adrian Gutierrez Gordillo", flex: [20, 22], pecho: [3.00, 3.60], cab: [3.10, 3.40], plan: ["1.33", "2.00"], abd: [24, 28], bronco: ["9,25", null, "4,30"] },
    { name: "Alba Rodriguez Torres", flex: [10, null], pecho: [3.90, 4.10], cab: [4.00, 4.00], plan: ["1.20", null], abd: [15, null], bronco: ["5,45", "6,48", null] },
    { name: "Alexis Calderon Encinas", flex: [10, 27], pecho: [5.00, 4.70], cab: [4.40, 4.50], plan: ["1.20", "1.44"], abd: [19, 27], bronco: ["5,05", "5,07", "3,48"] },
    { name: "Alex Navarro Minguez", flex: [32, 38], pecho: [4.50, 4.80], cab: [4.50, 5.40], plan: ["2.40", "4.02"], abd: [30, 45], bronco: ["4,41", "4,41", "3,26"] },
    { name: "Bruno Guill Perez", flex: [20, 30], pecho: [5.10, 5.10], cab: [4.80, 5.00], plan: ["1.00", "1.36"], abd: [20, 31], bronco: ["6,05", "5,52", "6,13"] },
    { name: "Bruno Villanova Escobar", flex: [13, 12], pecho: [4.50, 4.70], cab: [4.60, 4.45], plan: ["1.53", "2.29"], abd: [22, 24], bronco: ["5,22", null, "5,43"] },
    { name: "Daniel Bodokia Tsartsidze", flex: [41, null], pecho: [5.30, 5.50], cab: [5.20, 5.20], plan: ["2.26", null], abd: [35, null], bronco: ["5,12", "4,49", "4,52"] },
    { name: "Edu Torres Puebla", flex: [26, 31], pecho: [null, null], cab: [null, null], plan: ["0.58", "3.07"], abd: [30, 38], bronco: ["6,48", "6,07", "5,55"] },
    { name: "Erik Buges Sanchez", flex: [18, 28], pecho: [5.00, 4.80], cab: [5.20, 5.00], plan: ["1.00", "2.09"], abd: [28, 31], bronco: ["5,18", "5,49", "4,48"] },
    { name: "Fabio Daniel de Toledo Castro", flex: [29, 34], pecho: [null, null], cab: [null, null], plan: ["0.54", "2.15"], abd: [31, 35], bronco: ["5,02", null, null] },
    { name: "Hugo Navarro Minguez", flex: [28, 38], pecho: [4.70, 4.90], cab: [3.60, 4.40], plan: ["4.17", "2.42"], abd: [27, 35], bronco: ["5,18", "5,32", "5,14"] },
    { name: "Iu Villen Hernandez", flex: [18, 23], pecho: [null, null], cab: [null, null], plan: ["2.10", "3.03"], abd: [20, 27], bronco: ["5,40", null, "5,00"] },
    { name: "Jon Garreta Abad", flex: [23, 28], pecho: [3.90, 4.60], cab: [3.80, 3.10], plan: ["3.22", "2.35"], abd: [29, 38], bronco: ["5,12", "5,49", "4,25"] },
    { name: "Julen Lozano Nieto", flex: [20, 34], pecho: [4.00, 5.00], cab: [3.90, 4.10], plan: ["2.51", "5.24"], abd: [22, 37], bronco: ["5,40", null, "5,26"] },
    { name: "Julen Moral Saez", flex: [21, null], pecho: [3.30, 3.40], cab: [3.10, 3.00], plan: ["1.10", null], abd: [19, null], bronco: [null, "7,13", "6,18"] },
    { name: "Lucas Jimenez Gonzalez", flex: [20, null], pecho: [4.70, 4.00], cab: [4.35, 4.00], plan: ["2.30", null], abd: [27, null], bronco: ["4,52", null, "4,38"] },
    { name: "Manuel Garcia Jimenez", flex: [null, null], pecho: [null, null], cab: [null, null], plan: [null, null], abd: [null, null], bronco: [null, "6,10", "6,05"] },
    { name: "Maximo Gil Bebebino", flex: [26, null], pecho: [null, null], cab: [null, null], plan: ["0.25", null], abd: [30, null], bronco: ["4,55", "6,05", null] },
    { name: "Nicolas Covelo Gonzalez", flex: [22, 30], pecho: [3.00, 3.85], cab: [2.90, 3.10], plan: ["2.26", "6.07"], abd: [24, 25], bronco: ["5,00", "5,13", "4,57"] },
    { name: "Ohian Lozano Nieto", flex: [35, 32], pecho: [4.90, 5.00], cab: [4.45, 4.50], plan: ["5.60", "9.18"], abd: [29, 35], bronco: ["5,18", null, "4,57"] },
    { name: "Oriol Vallespin Viera", flex: [35, 39], pecho: [5.00, 5.50], cab: [4.45, 4.60], plan: ["3.33", "4.49"], abd: [27, 35], bronco: ["5,50", "5,58", "4,44"] },
    { name: "Pablo Santos Vallejo", flex: [38, 43], pecho: [5.40, 4.90], cab: [5.10, 4.90], plan: ["2.47", "7.59"], abd: [28, 38], bronco: [null, null, "5,20"] },
    { name: "Pau Diaz Pauta", flex: [35, 45], pecho: [null, null], cab: [null, null], plan: ["3.30", "4.09"], abd: [32, 40], bronco: ["4,41", "5,02", "4,38"] },
    { name: "Prescott Epoumbi", flex: [24, 30], pecho: [5.95, 6.00], cab: [7.10, 6.40], plan: ["0.50", "1.20"], abd: [22, 34], bronco: ["5,40", "5,19", "5,00"] },
    { name: "Victor Caro Caballero", flex: [20, 24], pecho: [null, null], cab: [null, null], plan: ["2.10", "3.23"], abd: [29, 37], bronco: ["5,56", "6,07", "3,57"] },
    { name: "Xavi Ferré Gracia", flex: [32, 30], pecho: [5.50, 5.40], cab: [6.00, 6.00], plan: ["2.00", "3.24"], abd: [27, 54], bronco: ["5,42", "5,10", "3,43"] }
];

function removeAccents(str) {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
}

async function run() {
    const client = new Client({ connectionString });
    try {
        await client.connect();

        const res = await client.query('SELECT id, nombre, apellidos FROM jugadores_propios');
        const players = res.rows;

        const playerMap = new Map();
        for (const p of players) {
            const fullName = `${p.nombre} ${p.apellidos}`.toLowerCase().trim();
            playerMap.set(fullName, p.id);
            playerMap.set(removeAccents(fullName), p.id);
        }

        const dates = {
            sep: '2025-09-01',
            oct: '2025-10-01',
            nov: '2025-11-01',
            dic: '2025-12-01'
        };

        const aliases = {
            "alexis calderon encinas": "alexis paul calderon encinas",
            "bruno guill perez": "bruno guil perez",
            "edu torres puebla": "eduard torres puebla",
            "maximo gil bebebino": "maximo luciano gil bebebino",
            "pablo santos vallejo": "pablo ignacio santos vallejo",
            "prescott epoumbi": "prescott lacroix epoumbi",
            "xavi ferré gracia": "xavier ferré garcia",
            "xavi ferre gracia": "xavier ferre garcia",
            "victor caro caballero": "victor caro caballero"
        };

        const executeUpdates = async (pId, dt, updates, values) => {
            if (updates.length > 0) {
                const check = await client.query('SELECT id FROM pruebas_fisicas WHERE jugador_id = $1 AND fecha = $2', [pId, dt]);
                if (check.rows.length === 0) {
                    const id = crypto.randomUUID();
                    const cols = ["id", "jugador_id", "fecha", ...updates.map(u => u.split(' = ')[0])];
                    const vals = [id, pId, dt, ...values];
                    const placeholders = cols.map((_, i) => `$${i + 1}`);
                    await client.query(`INSERT INTO pruebas_fisicas (${cols.join(', ')}) VALUES (${placeholders.join(', ')})`, vals);
                } else {
                    const id = check.rows[0].id;
                    values.push(id);
                    await client.query(`UPDATE pruebas_fisicas SET ${updates.join(', ')} WHERE id = $${updates.length + 1}`, values);
                }
            }
        };

        const missing = [];

        for (const row of data) {
            let nameClean = row.name.toLowerCase().trim();
            if (aliases[nameClean]) nameClean = aliases[nameClean];

            let pId = playerMap.get(nameClean);
            if (!pId) {
                nameClean = removeAccents(nameClean);
                if (aliases[nameClean]) nameClean = removeAccents(aliases[nameClean]);
                pId = playerMap.get(nameClean);
            }

            if (!pId) {
                missing.push(row.name);
                continue;
            }

            // --- SEPTEMBER ---
            let sepUpdates = []; let sepValues = []; let cSep = 1;
            if (row.flex?.[0] !== null && row.flex?.[0] !== undefined) { sepUpdates.push(`flexiones = $${cSep++}`); sepValues.push(row.flex[0]); }
            if (row.pecho?.[0] !== null && row.pecho?.[0] !== undefined) { sepUpdates.push(`lanzamiento_pecho = $${cSep++}`); sepValues.push(row.pecho[0]); }
            if (row.pecho?.[1] !== null && row.pecho?.[1] !== undefined) { sepUpdates.push(`lanzamiento_pecho_2 = $${cSep++}`); sepValues.push(row.pecho[1]); }
            if (row.cab?.[0] !== null && row.cab?.[0] !== undefined) { sepUpdates.push(`lanzamiento_encima_cabeza = $${cSep++}`); sepValues.push(row.cab[0]); }
            if (row.cab?.[1] !== null && row.cab?.[1] !== undefined) { sepUpdates.push(`lanzamiento_encima_cabeza_2 = $${cSep++}`); sepValues.push(row.cab[1]); }
            if (row.plan?.[0] !== null && row.plan?.[0] !== undefined) { sepUpdates.push(`plancha = $${cSep++}`); sepValues.push(row.plan[0]); }
            if (row.abd?.[0] !== null && row.abd?.[0] !== undefined) { sepUpdates.push(`abdominales = $${cSep++}`); sepValues.push(row.abd[0]); }
            if (row.bronco?.[0] !== null && row.bronco?.[0] !== undefined) { sepUpdates.push(`broncotest = $${cSep++}`); sepValues.push(row.bronco[0]); }
            await executeUpdates(pId, dates.sep, sepUpdates, sepValues);

            // --- OCTOBER ---
            let octUpdates = []; let octValues = []; let cOct = 1;
            if (row.bronco?.[1] !== null && row.bronco?.[1] !== undefined) { octUpdates.push(`broncotest = $${cOct++}`); octValues.push(row.bronco[1]); }
            await executeUpdates(pId, dates.oct, octUpdates, octValues);

            // --- NOVEMBER ---
            let novUpdates = []; let novValues = []; let cNov = 1;
            if (row.bronco?.[2] !== null && row.bronco?.[2] !== undefined) { novUpdates.push(`broncotest = $${cNov++}`); novValues.push(row.bronco[2]); }
            await executeUpdates(pId, dates.nov, novUpdates, novValues);

            // --- DECEMBER ---
            let dicUpdates = []; let dicValues = []; let cDic = 1;
            if (row.flex?.[1] !== null && row.flex?.[1] !== undefined) { dicUpdates.push(`flexiones = $${cDic++}`); dicValues.push(row.flex[1]); }
            if (row.plan?.[1] !== null && row.plan?.[1] !== undefined) { dicUpdates.push(`plancha = $${cDic++}`); dicValues.push(row.plan[1]); }
            if (row.abd?.[1] !== null && row.abd?.[1] !== undefined) { dicUpdates.push(`abdominales = $${cDic++}`); dicValues.push(row.abd[1]); }
            await executeUpdates(pId, dates.dic, dicUpdates, dicValues);
        }

        if (missing.length > 0) {
            console.log("Could not find the following players:");
            for (const m of missing) console.log("-", m);
        } else {
            console.log("Success! Data has been imported for all provided players.");
        }

    } catch (err) {
        console.error("Error:", err);
    } finally {
        await client.end();
    }
}

run();

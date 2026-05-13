const express = require('express');
const path = require('path');
const Database = require('better-sqlite3');

const app = express();
const PORT = process.env.PORT || 3000;
const db = new Database('taskmaster.db');

// Cədvəl yoxdursa yarat
db.exec(`
    CREATE TABLE IF NOT EXISTS posts (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        name    TEXT NOT NULL,
        message TEXT NOT NULL,
        time    TEXT NOT NULL
    )
`);

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// GET - Bütün postları qaytar
app.get('/api/posts', (req, res) => {
    const posts = db.prepare('SELECT * FROM posts ORDER BY id DESC').all();
    res.status(200).json(posts);
});

// POST - Yeni post əlavə et
app.post('/api/posts', (req, res) => {
    const { name, message } = req.body;

    if (!name || !message) {
        return res.status(400).json({ error: 'Ad ve mesaj mutleqdir!' });
    }

    const time = new Date().toLocaleString();
    const result = db.prepare('INSERT INTO posts (name, message, time) VALUES (?, ?, ?)').run(name, message, time);

    const newPost = { id: result.lastInsertRowid, name, message, time };
    console.log('\n>>> YENİ POST:');
    console.log('    Ad    : ' + name);
    console.log('    Mesaj : ' + message);
    res.status(201).json(newPost);
});

// PUT - Post düzəliş et
app.put('/api/posts/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const { name, message } = req.body;

    const post = db.prepare('SELECT * FROM posts WHERE id = ?').get(id);
    if (!post) return res.status(404).json({ error: 'Post tapilmadi!' });

    const newName = name || post.name;
    const newMessage = message || post.message;
    const newTime = post.time + ' (duzeldildi)';

    db.prepare('UPDATE posts SET name = ?, message = ?, time = ? WHERE id = ?').run(newName, newMessage, newTime, id);

    console.log('\n>>> POST DÜZƏLDİLDİ:');
    console.log('    Ad    : ' + post.name + ' -> ' + newName);
    console.log('    Mesaj : ' + post.message + ' -> ' + newMessage);
    res.status(200).json({ id, name: newName, message: newMessage, time: newTime });
});

// DELETE - Post sil
app.delete('/api/posts/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const post = db.prepare('SELECT * FROM posts WHERE id = ?').get(id);

    if (!post) return res.status(404).json({ error: 'Post tapilmadi!' });

    db.prepare('DELETE FROM posts WHERE id = ?').run(id);
    console.log('\n>>> POST SİLİNDİ: ' + post.name);
    res.status(200).json({ message: 'Post deleted.' });
});

// GET /api/v1/data
app.get('/api/v1/data', (req, res) => {
    res.status(200).json({
        status: "success",
        data: [
            { id: 1, name: "Node.js Fundamentals", type: "Backend" },
            { id: 2, name: "Express.js Routing",   type: "Framework" },
            { id: 3, name: "API Testing",           type: "Testing" }
        ]
    });
});

// POST /api/v1/data
app.post('/api/v1/data', (req, res) => {
    const payload = req.body;
    console.log('Received Payload:', payload);
    res.status(201).json({ status: "created", receivedData: payload });
});

app.listen(PORT, () => {
    console.log('\nServer is running at http://localhost:' + PORT + '\n');
});
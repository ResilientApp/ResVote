import express from "express";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import cors from "cors";
import bodyParser from "body-parser";

const app = express();
const port = 5000;

app.use(cors());
app.use(bodyParser.json()); // Only deals with json bodies

app.get("/", async(req, res) => {
    res.json({message: "Hi there", status: "Running"})
});

app.post("/login", async (req, res) => {
    const { username, password } = req.body; // Pull username and password from request body

    // look up user in DB through graphQL IG
    const user = null

    if (!user) return res.status(401).json({ message: "Invalid username or password"});

    const match = await bcrypt.compare(password, user.password);

    if (!match) return res.status(401).json({ message: "Invalid username or password"});

    const token = jwt.sign({ username: user.username }, "s0meCr4ZyL33t4K3y (put key here)", { expiresIn: "1h"} );

    res.json({token}); // respond with a jwt
});

app.listen(port, () => {
    console.log(`Express server running on http://localhost:${port}`);
})
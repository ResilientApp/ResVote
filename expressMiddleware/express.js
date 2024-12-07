const express = require('express');
const { MongoClient } = require('mongodb');
const cors = require('cors');

const ELECTION_LIST_KEYS = {
  pub_key: "CNYD8bh324Wfpv2YPuXnXCgA5FsuNG2x1NW1ZxZCgzGf",
  priv_key: "Deq2mn9cRhVHDcMiYSNhhc2KufzzNdor4udq31c5JfYn"
}

const VOTE_USER_KEYS = {
  pub_key: "EhUevpJhHBPuR2JuruiVp2URMCdgKAFCirCBNvhc75iA",
  priv_key: "FNNeS67CJov9VEW13k4QQH1LfZGmjGQ1qKuxj7uaDPfD"
}

const app = express();
app.use(cors()); // Allow requests from your React frontend
app.use(express.json()); // Parse JSON bodies

const uri = "mongodb+srv://taculp:SRAo8EG1Ub6YFP6C@cluster0.htruocb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";
const dbName = "resDB";
const collectionName = "the_cache";

const client = new MongoClient(uri);

app.get('/elections', async (req, res) => {
  console.log("elections request received");
  try {
    await client.connect();
    const db = client.db(dbName);
    const collection = db.collection(collectionName);

    const pipeline = [
      { $unwind: "$transactions" },
      { $unwind: "$transactions.value.inputs" },
      { $unwind: "$transactions.value.outputs" },
      {
        $match: {
          "transactions.value.outputs.public_keys": ELECTION_LIST_KEYS.pub_key
        }
      },
      { $sort: { "transactions.value.asset.data.timestamp": -1 } },
      { $project: { transactions: "$transactions", _id: 0 } }
    ];

    const cursor = collection.aggregate(pipeline);
    const transactions = await cursor.toArray();

    if (transactions.length > 0) {
      console.log('Transactions with the specified publicKey in owners_before:', 
                  JSON.stringify(transactions, null, 2));
    } 
    else {
      console.log(`No transactions found for publicKey: ${ELECTION_LIST_KEYS.pub_key}`);
    }

    res.json(transactions);
  } 
  catch (err) {
    console.error(err);
    res.status(500).send("Error connecting to MongoDB");
  }   
  finally {
    await client.close();
  }
});

app.get('/votes', async (req, res) => {
  console.log("vote request received");
  try {
    await client.connect();
    const db = client.db(dbName);
    const collection = db.collection(collectionName);

    const pipeline = [
      { $unwind: "$transactions" },
      { $unwind: "$transactions.value.inputs" },
      { $unwind: "$transactions.value.outputs" },
      {
        $match: {
          "transactions.value.outputs.public_keys": VOTE_USER_KEYS.pub_key
        }
      },
      { $sort: { "transactions.value.asset.data.timestamp": -1 } },
      { $project: { transactions: "$transactions", _id: 0 } }
    ];

    const cursor = collection.aggregate(pipeline);
    const transactions = await cursor.toArray();

    if (transactions.length > 0) {
      console.log('Transactions with the specified publicKey in owners_before:', 
                  JSON.stringify(transactions, null, 2));
    } 
    else {
      console.log(`No transactions found for publicKey: ${VOTE_USER_KEYS.pub_key}`);
    }
    res.json(transactions);
  } 
  catch (err) {
    console.error(err);
    res.status(500).send("Error connecting to MongoDB");
  }    
  finally {
    await client.close();
  }
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

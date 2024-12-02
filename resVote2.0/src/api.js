
import { ResilientDB, FetchClient } from 'resilientdb-javascript-sdk';
import { v4 as uuidv4 } from 'uuid';
// import fs from "file-system";

const ELECTION_LIST_KEYS = {
    "pub_key": "65CKYjMoaez6FZnPkD53wxtTAiTX7YEcLvjnQtNjWEas",
    "priv_key": "2b814nXg4ZKPh6LC9pZsC7BVEKFR6eyENG6JybKYxKqt"
}

const resilientDBClient = new ResilientDB("http://localhost:8000/graphql", new FetchClient());

export async function getElections() {
    const filter = {
        "recipientPublickKey": ELECTION_LIST_KEYS.pub_key
    }
    try {
        const elections = await resilientDBClient.getFilteredTransactions(filter);
        console.log("elections", elections);
    }
    catch(e) {
        console.error("error getting elections", e);
    }
    return [];
}

export function castVote(electionId, candidateName, user) {
    return true;
}

export async function addElectionToResDB(election) {
    const { name, description, candidates } = election;
    const transactionData = {
        operation: "CREATE",
        signerPublicKey: "test",
        signerPrivateKey: "test",
        recipientPublickKey: ELECTION_LIST_KEYS.pub_key,
        asset: {
            name,
            description,
            candidates,
            ID: uuidv4()
        }
    }
    try {
        const transaction = await resilientDBClient.postTransaction(transactionData);
        console.log("New election created transaction", transaction);
        return transaction.id;
    }
    catch(e) {
        console.error("Error making transaction:", e);
    }
}

function updateMasterElectionID(newElectionID) {
    const prevElections = getElections();
    prevElections.append(newElectionID);

    // send new transaction to resDB
    // update asset.json with new main transactionID
} 
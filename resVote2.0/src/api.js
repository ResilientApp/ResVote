
import { ResilientDB, FetchClient } from 'resilientdb-javascript-sdk';
import ResVaultSDK from 'resvault-sdk';

const ELECTION_LIST_KEYS = {
    pub_key: "65CKYjMoaez6FZnPkD53wxtTAiTX7YEcLvjnQtNjWEas",
    priv_key: "DeV5ytoprBy7k5M31ABkNNPi8mwaUL8dhGgJnXk1bGN9"
}

const TEST_USER_KEYS = {
    pub_key: "EhUevpJhHBPuR2JuruiVp2URMCdgKAFCirCBNvhc75iA",
    priv_key: "FNNeS67CJov9VEW13k4QQH1LfZGmjGQ1qKuxj7uaDPfD"
}

const resilientDBClient = new ResilientDB("https://cloud.resilientdb.com", new FetchClient());
const sdkRef = new ResVaultSDK();

/**
 * 
 * @param {Object} election 
 * @returns transaction id of newly created election
 * 
 * Let's us create elections fine, but the signer keys are always the same.
 * Behavior may be fine if we assume this is like an admin key or something for example.
 * 
 * It works but I don't know how to retrieve create elections :'(
 */
export async function addElectionToResDB(election) {
    const { name, description, candidates } = election;
    const message = {
        type: "commit",
        direction: "commit",
        amount: 1,
        data: {
            name,
            description,
            candidates
        },
        recipient: ELECTION_LIST_KEYS["pub_key"]
    };

    try {
        const res = await sdkRef.sendMessage(message);
        console.log("New election:", res);
    }
    catch (err) {
        console.error("Error making election", err);
    }
    // const transactionData = {
    //     operation: "CREATE",
    //     amount: 1,
    //     signerPublicKey: TEST_USER_KEYS["pub_key"],
    //     signerPrivateKey: TEST_USER_KEYS["priv_key"],
    //     recipientPublicKey: ELECTION_LIST_KEYS["pub_key"], 
    //     asset: {
    //         name,
    //         description,
    //         candidates,
    //     }
    // }
    // try {
    //     const transaction = await resilientDBClient.postTransaction(transactionData);
    //     console.log("New election created transaction", transaction);
    //     return transaction.id;
    // }
    // catch(e) {
    //     console.error("Error making transaction:", e);
    // }
}

/**
 * 
 * @returns List of availble election Ids
 * 
 * Currently doesn't work
 */
export async function getElections() {
    // The below code breaks. It seems like the transaction ID isn't being entered right (complains about
    // seeing the char 'd' and not a number). IDK why it's doing this
    // const test = await resilientDBClient.getTransaction("7d34971e49bddce01eec1460463cdb1d9f37ff10382c08c0ec3a4a942e6d3264")

    const filter = {
        "senderPublicKey": TEST_USER_KEYS["pub_key"],
        "recipientPublickKey": ELECTION_LIST_KEYS["priv_key"]
    }
    try {
        // This straight up doesn't work, idk if this function got deprecated or something
        const elections = await resilientDBClient.getFilteredTransactions(filter); 
        console.log("elections", elections);
    }
    catch(e) {
        console.error("error getting elections", e);
    }
    return [];
}

/**
 * 
 * @param {Int} electionId 
 * @param {string} candidateName 
 * @param {pubKey} user 
 * @returns void
 * TODO: Need to implement cast vote once creating elections is possible, should just send a transaction
 * to resilientDB that includes the electionID and candidate selected in the asset data
 * 
 * Once that is done we will just collect all votes later and filter specific elction votes down
 * when visualizing the elections
 */
export function castVote(electionId, candidateName, user) {
    return true;
}
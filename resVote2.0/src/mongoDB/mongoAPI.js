import axios from "axios";

export const ELECTION_LIST_KEYS = {
    pub_key: "CNYD8bh324Wfpv2YPuXnXCgA5FsuNG2x1NW1ZxZCgzGf",
    priv_key: "Deq2mn9cRhVHDcMiYSNhhc2KufzzNdor4udq31c5JfYn"
}

export const VOTE_USER_KEYS = {
    pub_key: "EhUevpJhHBPuR2JuruiVp2URMCdgKAFCirCBNvhc75iA",
    priv_key: "FNNeS67CJov9VEW13k4QQH1LfZGmjGQ1qKuxj7uaDPfD"
}

/**
 * 
 * @returns List of availble election objects
 * electionObj = {
 *      electionName: str,
 *      electionDesc: str,
 *      candidates: List
 * }
 * Works by making a request to an express application running on port 5000.
 * Filters mongoDB cache based off election users public key
 * 
 */
export async function getElections() {
    const elections = (await fetch("http://127.0.0.1:5000/elections"));
    const electionJson = await elections.json();
    console.log("electionJson from express:", electionJson);
    const electionObjects = electionJson.map((json) => {
        try {
            const obj = json.transactions.value.asset.data;
            return obj;
        }
        catch (err) {
            console.error(`failed to decode ${json} with error ${err}`);
            return {"name": "error", "reason": err};
        }
    })
    console.log("election objects:", electionObjects);
    return electionObjects;
}

/**
 * Similar to above, will return a list of vote objects
 * Done by making request to express server and filtering mongo cache
 */
export async function getVotes() {
    const votes = (await fetch("http://127.0.0.1:5000/votes"));
    const voteJson = await votes.json();
    console.log("electionJson from express:", voteJson);
    const voteObjects = voteJson.map((json) => {
        try {
            const obj = json.transactions.value.asset.data;
            return obj;
        }
        catch (err) {
            console.error(`failed to decode ${json} with error ${err}`);
            return {"name": "error", "reason": err};
        }
    })
    console.log("election objects:", voteObjects);
    return voteObjects;
}

async function getElectionFromGraphQL(electionID) {
    console.log(`electionID retrieving = ${electionID}`)
    const data = JSON.stringify({
        query: `query {getTransaction(id: "${electionID}") {
        id
        version
        amount
        metadata
        operation
        asset
        publicKey
        uri
        type
        signerPublicKey
      }}`
    });

    const config = {
        method: 'post',
        // url: 'http://127.0.0.1:8000/graphql',
        url: 'https://cloud.resilientdb.com/graphql',
        headers: {
            'Content-Type': 'application/json',
        },
        data: data,
    };
    try {
        const pulledData = await axios(config);
        console.log("PulledData =", pulledData);
        const fixedJsonString = pulledData.data.data.getTransaction.asset.replace(/'/g, '"');
        const parsedData = JSON.parse(fixedJsonString).data;

        console.log("PulledData type = ", typeof(pulledData));
        console.log("parsedData =", parsedData);


        if (pulledData && pulledData.status === 200) {
            return parsedData;
        }
    }
    catch (err) {
        console.error(err);
        return {"name": "error", "reason": err};
    }
}
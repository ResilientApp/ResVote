import axios from "axios"

/**
 * 
 * @returns List of availble election Ids
 * 
 * Currently have to add in newly created elections by hand (can find transaction ids
 * for them in console logs after creating them)
 * TODO: Filter mongoDB cache on election user public key to get list of votes
 * 
 * returns a list of objects, each having: a name, descripting, and list of candidates
 * 
 * Note: I think I got throttled or something because I can't make any requests to the cloud instance
 */

// Can remove fields as desired (must have at least 1)
let data = JSON.stringify({
    query: `query {getTransaction(id: "c3c1f71f13137d8843c4fbf2411d17982f2f2e46004c929c2c7eff35621b1d96") {
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
  }}`,
    variables: {}
});

  let config = {
    method: 'post',
    maxBodyLength: Infinity,
    url: 'https://cloud.resilientdb.com/graphql',
    headers: { 
      'Content-Type': 'application/json'
    },
    data : data
  };
export const elections = ["c3c1f71f13137d8843c4fbf2411d17982f2f2e46004c929c2c7eff35621b1d96", "df235b422bae9aeeb89545fb5d75941481b2bfa485c6d7af9049f0efc1b580fb", "44116e50bb139b02b0de8189c3b96040e3a0b8f85363b21c3d75f06d63bb6572"];
// export const elections = ["c3c1f71f13137d8843c4fbf2411d17982f2f2e46004c929c2c7eff35621b1d96"]
// export const elections = [];

export async function getElections() {
    console.log(`elections = ${elections}`);
    const electionPromises = elections.map(electionID => getElection(electionID));

    const electionObjects = await Promise.all(electionPromises);

    console.log("electionObjects", electionObjects);  // Debug: check the final array of election data
    return electionObjects;
}

async function getElection(electionID) {
    console.log(`electionID retrieving = ${electionID}`)
    const data = JSON.stringify({
        query: `query {getTransaction(id: "${electionID}") {
        asset
      }}`
    });

    const config = {
        method: 'post',
        url: 'http://127.0.0.1:8000/graphql',
        // url: 'https://cloud.resilientdb.com/graphql',
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
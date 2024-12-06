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
export async function getElections() {
    // const elections = ["df235b422bae9aeeb89545fb5d75941481b2bfa485c6d7af9049f0efc1b580fb"];
    const elections = ["c3c1f71f13137d8843c4fbf2411d17982f2f2e46004c929c2c7eff35621b1d96", "df235b422bae9aeeb89545fb5d75941481b2bfa485c6d7af9049f0efc1b580fb"];
    const electionObjects = elections.map(async (electionID) => {
        const election = await getElection(electionID);
        return election; // This is a promise resolution, returning the election data
    });

    // Wait for all the promises to resolve using Promise.all
    const resolvedElections = await Promise.all(electionObjects);
    console.log(resolvedElections)
    // const electionObjects = [];
    // elections.forEach(async (electionID) => {
    //     const url = `https://crow.resilientdb.com/v1/transactions/${electionID}`;
    //     try {
    //         const pulledData = await fetch(url);
    //         if (pulledData.ok) {
    //             const jsonBody = await pulledData.json();
    //             const assetData = jsonBody.asset.data;
    //             console.log("assetData,", assetData);
    //             electionObjects.push(assetData);
    //         }
    //     }
    //     catch (err) {
    //         console.error("Error when retrieving transaction", err);
    //     }
    // });
    // console.log("electionObjects:", electionObjects);
    return resolvedElections;
}

async function getElection(electionID) {
    const url = `https://crow.resilientdb.com/v1/transactions/${electionID}`;
    try {
        const pulledData = await fetch(url);

        if (pulledData.ok) {
            const jsonBody = await pulledData.json();
            console.log(jsonBody)
            // const assetData = jsonBody.asset.data;
            //return assetData;
        }
    }
    catch (err) {
        return {"description": "error"};
    }
}
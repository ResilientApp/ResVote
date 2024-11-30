import ResVaultSDK from 'resvault-sdk';
// import fs from "file-system";

export function getElections() {
    const sdk = new ResVaultSDK(); // Trying to figure out how this sdk words
    console.log("Attempt to generate keys");
    const key = sdk.sendMessage({
        type: "Keys",
        direction: "Keys",
    })
    console.log("keys =", key)
    return [];
}

export function castVote(electionId, candidateName, user) {
    return true;
}

export function addElectionToResDB(election) {

}

function updateMasterElectionID(newElectionID) {
    const prevElections = getElections();
    prevElections.append(newElectionID);

    // send new transaction to resDB
    // update asset.json with new main transactionID
} 
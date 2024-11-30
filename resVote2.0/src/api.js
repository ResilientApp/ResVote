export function getElections() {
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
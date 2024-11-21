// Not sure if I want to actually use this, was thinking of a controller where elections get created
// With specific parameters, and then those elections get pushed out to users if they meet specific criteria

import { getElections } from "../src/apis";

// Might get too complicated though
class ElectionController {
    constructor() {
        this.openElections = [];
        this.subscripedUsers = [];
    }
    createNewElection(candidateName, location, timeWindow) {
        const election = Election(candidateName, location, timeWindow);
        this.openElections.append(election);
        updateUsers(election)
    }

    updateUsers(election) {
        this.subscripedUsers.forEach(user => {
            // get userObject from kv
            // const userInfo = getUser(user);
            const userInfo = { };
            if (election.valid(userInfo)) {
                // api.addElection(user, election)
            }
        });
    }
}

class Election {
    constructor(candidateName, location, timeWindow) {
        this.uuid = "1234"; // make this unique later
        this.candidateName = candidateName;
        this.location = location;
        this.timeWindow = timeWindow;
    }
    valid(userInfo) {
        return true;
    }
}
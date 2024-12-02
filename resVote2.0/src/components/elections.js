import React, { useState } from "react";
import { Button } from "antd"
import Logout from "./Logout";
import CreateElectionView from "./Election_Components/CreateElectionView";
import VoteInElectionView from "./Election_Components/VoteInElectionView";
import ElectionTableView from "./Election_Components/ElectionTableView";
import "./election.css";

/**
 * 
 * @param {onLogout, token} params 
 * onLogout is a callback to just log the user out
 * token is users unique identifier
 * 
 * Defines our main election view (where most of our project will live)
 * 
 * By default we will display a table of ongoing elections which a user can participate in.
 * Users can select an election to participate in and will then be taken to the VoteInElection view
 * where they can actually select their chosen candidate and cast a vote
 * @returns 
 */
export default function ElectionsView(params) {
    const { onLogout, token } = params;
    const [electionToVoteIn, setElectionToVoteIn] = useState(null);
    const [createElection, setCreateElection] = useState(false);

    return (
        <div className="electionContainer">
            {/* Only render CreateElection or the button when createElection is true */}
            {createElection ? (
                <CreateElectionView setCreateElection={setCreateElection}/> // Render CreateElection when state is true
            ) : (
                <>
                    {/* When a user isn't creating an election they can view or vote */}
                    <Button onClick={() => setCreateElection(true)}>Create Election</Button>
                    {electionToVoteIn === null ? (
                        <ElectionTableView
                            setElectionToVoteIn={setElectionToVoteIn}
                        />
                    ) : (
                        <>
                            <VoteInElectionView election={electionToVoteIn} token={token} setElectionToVoteIn={setElectionToVoteIn}/>
                        </>
                    )}
                </>
            )}

            {/* The logout button is always available */}
           <Logout onLogout={onLogout} />
        </div>
    );
}
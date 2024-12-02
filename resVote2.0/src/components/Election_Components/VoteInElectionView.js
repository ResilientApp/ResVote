import React, { useState } from "react";
import { castVote } from "../../api";
import "./VoteInElectionView.css"

/**
 * 
 * @param {election, token} params 
 * election is the same as in the SelectElection function
 * token is the logged in users unique token (I think their pub key but i need to test)
 * 
 * Creates a form with a list of candidates that can be voted for.
 * Displays a radio button next to candidates name for selection.
 * Once a candidate has been selected user can vote for them
 * @returns 
 */
export default function VoteInElectionView(params) {
    const { election, token, setElectionToVoteIn } = params
    const { description, electionID, candidates } = election;
    const [selectedCandidate, setSelectedCandidate] = useState("");

    // Function to submit which candidate was chosen from the form
    async function handleSubmit(e) {
        e.preventDefault();

        if (!selectedCandidate) {
            alert("Must vote for someone!");
        }
        else {
            try { // If they have chosen a candidate and click 'Vote' we attempt to cast their vote
                const voteSuccessful = await castVote(electionID, selectedCandidate, token);
                setElectionToVoteIn(null);
            }
            catch (error) {
                console.error("Votting error", error);
                alert("error casting vote");
            }
        }
    }
    return (
        <>
            <h1>Vote in Election: {electionID}</h1>
            <h2>{description}</h2>
            <form onSubmit={handleSubmit}>
                {candidates.map(candidate => {
                    <label for={candidate}>{
                        candidate}: <input 
                                        type="radio" 
                                        id={candidate} 
                                        name={candidate}
                                        value={candidate}
                                        onChange={() => setSelectedCandidate(candidate)}/>
                    </label>
                })}
                <input type="submit" value="Vote!" />
            </form>
        </>
    )
}
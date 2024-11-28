import React, { useState } from "react";
import { Table, Button } from "antd"
import { castVote, getElections } from "../api";
import Logout from "./Logout";
/**
 * 
 * @param {election, setElectionToVoteIn} params 
 * election holds info on a specific election, including description, electionID, and candidates in election.
 * setElectionToVoteIn is a useState function that sets a variable when the user decides which election to actually partipate in. 
 * Once selected this will switch them to the VoteInELection view where they can actually vote for a candidate.
 * 
 * TODO: Possibly could make this all one thing, by just letting them vote for candidates in the table
 * could be more or less work (idk)
 * @returns null
 */
function SelectElection(params) { 
    const { description, electionID, candidates } = params.election;
    const { setElectionToVoteIn } = params.setElectionToVoteIn;
    return (
        // Just make a table row with election info and a button that can be used to select 
        // a particular election to vote in
        <>
            <tr>
                <td>{description}</td>
                <td>{electionID}</td>
                <td>{candidates}</td>
                <td><Button onClick={() => setElectionToVoteIn(params.election)}>Vote</Button></td>
            </tr>
        </>
    )
}
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
function VoteInElection(params) {
    const { description, electionID, candidates } = params.election;
    const { token } = params;
    const [selectedCandidate, setSelectedCandidate] = useState("");

    // Function to submit which candidate was chosen from the form
    async function handleSubmit(e) {
        e.preventDfault();

        if (!selectedCandidate) {
            alert("Must vote for someone!");
        }
        else {
            try { // If they have chosen a candidate and click 'Vote' we attempt to cast their vote
                const voteSuccessful = await castVote(electionID, selectedCandidate, token);
            }
            catch (error) {
                console.error("Votting error", error);
                alert("error casting vote");
            }
        }
    }
    return (
        <>
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
    const availableElections = getElections();
    return(
        <>
            ({electionToVoteIn !== null} ?
            <>
                <h1>Vote in Election: {electionToVoteIn.electionID}</h1>
                <VoteInElection election={electionToVoteIn} token={token}/>
            </>
            :
            <h1>Elections View</h1>
            <table>
                <tr>
                    <th>Election Description</th>
                    <th>Election ID</th>
                    <th>Election Candidates</th>
                    <th>Vote in Election</th>
                </tr>
                {availableElections.map(election => {
                    <SelectElection election={election} setElectionToVoteIn={setElectionToVoteIn}/>
                })}
            </table>)
            <Logout onLogout={onLogout} />
        </>
    )
}
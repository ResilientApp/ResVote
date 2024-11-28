import React, { useState } from "react";
import { Table, Button } from "antd"
import { castVote, getElections } from "../api";
import Logout from "./Logout";

function SelectElection(params) {
    const { description, electionID, candidates } = params.election;
    const { setElectionToVoteIn } = params.setElectionToVoteIn;
    return (
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

function VoteInElection(params) {
    const { description, electionID, candidates } = params.election;
    const { token } = params;
    const [selectedCandidate, setSelectedCandidate] = useState("");

    async function handleSubmit(e) {
        e.preventDfault();

        if (!selectedCandidate) {
            alert("Must vote for someone!");
        }
        else {
            const voteSuccessful = await castVote(electionID, selectedCandidate, token);
        }
    }
    return (
        <>
            <h2>{description}</h2>
            <form>
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
import React, { useEffect, useState } from "react";
import { Button } from "antd"
import { getElections } from "../../mongoDB/mongoAPI";
import "./ElectionTableView.css";

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
    const { election, setElectionToVoteIn } = params;
    const { description, electionID, candidates } = election;
    return (
        // Just make a table row with election info and a button that can be used to select 
        // a particular election to vote in
        <>
            <tr>
                <td>{description}</td>
                <td>{electionID}</td>
                <td>{candidates}</td>
                <td><Button onClick={() => setElectionToVoteIn(election)}>Vote</Button></td>
            </tr>
        </>
    )
}

export default function ElectionTableView(params) {
    const [availableElections, setAvailableElections] = useState([]);
    const {setElectionToVoteIn } = params;

    // Hacky way to get the getElections() function to call without error
    useEffect(() => {
        const fetchElections = async () => {
            const elections = await getElections();  // Fetch elections asynchronously
            setAvailableElections(elections);  // Update state with the fetched elections
        };

        fetchElections();
    }, []);
    return (
        <>
            <h1>Available Elections View</h1>
            <table>
                <thead>
                    <tr>
                        <th>Election Description</th>
                        <th>Election ID</th>
                        <th>Election Candidates</th>
                        <th>Vote in Election</th>
                    </tr>
                </thead>
                <tbody>
                    {availableElections.map(election => (
                        <SelectElection 
                            key={election.electionID} 
                            election={election} 
                            setElectionToVoteIn={setElectionToVoteIn} 
                        />
                    ))}
                </tbody>
            </table>
        </>
    )
}
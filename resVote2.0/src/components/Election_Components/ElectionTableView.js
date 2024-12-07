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
    const { description, name, candidates } = election;
    return (
        // Just make a table row with election info and a button that can be used to select 
        // a particular election to vote in
        <>
            <tr>
                <td>{name}</td>
                <td>{description}</td>
                <td>{candidates.map((candidate) => {
                    return (
                        <ul>
                            <li>{candidate}</li>
                        </ul>
                    )
                })}</td>
                <td><Button onClick={() => setElectionToVoteIn(election)}>Vote</Button></td>
            </tr>
        </>
    )
}

export default function ElectionTableView(params) {
    const [availableElections, setAvailableElections] = useState([]);
    const [isFetching, setIsFetching] = useState(false);
    const {setElectionToVoteIn } = params;

    // Fetch elections and cache in localStorage
    const fetchElections = async () => {
        try {
            setIsFetching(true);
            const elections = await getElections();
            setAvailableElections(elections);

            // Save to localStorage
            localStorage.setItem("cachedElections", JSON.stringify(elections));
            localStorage.setItem("cacheTimestamp", Date.now().toString());
        } catch (error) {
            console.error("Error fetching elections:", error);
        } finally {
            setIsFetching(false);
        }
    };

    // Check for cached elections and load them if they are fresh
    const loadCachedElections = () => {
        const cachedElections = localStorage.getItem("cachedElections");
        const cacheTimestamp = localStorage.getItem("cacheTimestamp");

        if (cachedElections && cacheTimestamp) {
            const now = Date.now();
            const cacheAge = now - parseInt(cacheTimestamp, 10);

            // Use cached elections if they are less than 5 minutes old
            if (cacheAge < 5 * 60 * 1000) {
                setAvailableElections(JSON.parse(cachedElections));
            } else {
                fetchElections();
            }
        } else {
            fetchElections();
        }
    };

    // Fetch elections every 5 minutes
    useEffect(() => {
        loadCachedElections();

        const interval = setInterval(() => {
            fetchElections();
        }, 5 * 60 * 1000);

        return () => clearInterval(interval);
    }, []);

    return (
        <>
            <div className="header">
                <h1>Available Elections View</h1>
                <Button
                    onClick={fetchElections}
                    disabled={isFetching}
                >
                    {isFetching ? "Loading..." : "Fetch Elections"}
                </Button>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Election Name</th>
                        <th>Election Description</th>
                        <th>Election Candidates</th>
                        <th>Vote in Election</th>
                    </tr>
                </thead>
                <tbody>
                    {availableElections.map(election => {
                        return ((!election || !election.name || election.name === "error")  ? 
                        <></>
                        :
                        <SelectElection 
                            key={election.name} 
                            election={election} 
                            setElectionToVoteIn={setElectionToVoteIn} 
                        />
                        )
                    })}
                </tbody>
            </table>
        </>
    )
}
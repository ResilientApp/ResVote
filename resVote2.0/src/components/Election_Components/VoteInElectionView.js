import React, { useState, useRef, useEffect } from "react";
import ResVaultSDK from 'resvault-sdk';
import "./VoteInElectionView.css"

const VOTE_USER_KEYS = {
    pub_key: "EhUevpJhHBPuR2JuruiVp2URMCdgKAFCirCBNvhc75iA",
    priv_key: "FNNeS67CJov9VEW13k4QQH1LfZGmjGQ1qKuxj7uaDPfD"
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
export default function VoteInElectionView(params) {
    const { election, token, setElectionToVoteIn } = params
    const { description, electionID, candidates } = election;
    const [selectedCandidate, setSelectedCandidate] = useState("");

    const sdkRef = useRef(null);

    if (!sdkRef.current) {
        sdkRef.current = new ResVaultSDK();
    }

    useEffect(() => {
        const sdk = sdkRef.current;
        if (!sdk) return;
    
        const messageHandler = (event) => {
          const message = event.data;
    
          if (
            message &&
            message.type === 'FROM_CONTENT_SCRIPT' &&
            message.data &&
            message.data.success !== undefined
          ) {
            if (message.data.success) {
                console.log("Election created successfully");
                console.log("Response:", JSON.stringify(message));
            } else {
                console.error("Election creation failed:", message.data.error, JSON.stringify(message.data.errors));
            }
          }
        };
    
        sdk.addMessageListener(messageHandler);
    
        return () => {
          sdk.removeMessageListener(messageHandler);
        };
      }, []);

    // Function to submit which candidate was chosen from the form
    async function handleSubmit(e) {
        e.preventDefault();

        if (!selectedCandidate) {
            alert("Must vote for someone!");
        }
        else {
            try {
                sdkRef.current.sendMessage({
                    type: 'commit',
                    direction: 'commit',
                    amount: "1",
                    data: {
                        "type": "vote",
                        "candidate": selectedCandidate,
                        "election": electionID
                    },
                    recipient: VOTE_USER_KEYS["pub_key"],
                });
                setSelectedCandidate(null);
                setElectionToVoteIn(null);
            }
            catch (err) {
                console.error("Vote wasn't cast", err);
                alert(err);
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
import React, { useState, useRef, useEffect } from "react";
import ResVaultSDK from 'resvault-sdk';
import { Button, Modal } from "antd";
import { VOTE_USER_KEYS } from "../../mongoDB/mongoAPI";
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
    const { description, name, candidates } = election;
    const [selectedCandidate, setSelectedCandidate] = useState("");
    const [modalMessage, setModalMessage] = useState(null);

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
                console.log("Vote created successfully");
                console.log("Response:", JSON.stringify(message));
                setModalMessage(`Vote successfully submitted. Click ok to return to elections.`);
            } else {
                console.error("Vote creation failed:", message.data.error, JSON.stringify(message.data.errors));
                setModalMessage("Vote failed to complete, hit cancel to try again.")
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
                        "election": name
                    },
                    recipient: VOTE_USER_KEYS["pub_key"],
                });
            }
            catch (err) {
                console.error("Vote wasn't cast", err);
                alert(err);
            }
        }
    }

    function cleanUp() {
        setModalMessage(null);
        setElectionToVoteIn(null);
        setSelectedCandidate(null);
    }
    console.log("Selected Candidate = ", selectedCandidate);
    return (
        <>
            <Button onClick={() => setElectionToVoteIn(null)}>Exit</Button>
            <h1>Vote in Election: {name}</h1>
            <h2>{description}</h2>
            <form onSubmit={handleSubmit}>
                {candidates.map(candidate => {
                    return (
                        <label for={candidate}>{
                            candidate}: <input 
                                            type="radio" 
                                            id={candidate} 
                                            name="candidate"
                                            value={candidate}
                                            onClick={() => setSelectedCandidate(candidate)}
                                        />
                        </label>
                    )
                })}
                <input type="submit" value="Vote!" />
            </form>
            <Modal
            open={modalMessage !== null}
            onOk={cleanUp}
            onCancel={() => setModalMessage(null)}
            closable={false}
            >
                {modalMessage}
            </Modal>
        </>
    )
}
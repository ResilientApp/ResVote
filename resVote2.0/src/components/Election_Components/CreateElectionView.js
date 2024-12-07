import React, { useState, useRef, useEffect } from "react";
import { Button, Input, Form, List, Modal } from "antd";
import ResVaultSDK from 'resvault-sdk';
import { ELECTION_LIST_KEYS } from "../../mongoDB/mongoAPI";
import "./CreateElectionView.css";

export default function CreateElectionView(params) {
    const { setCreateElection } = params;
    
    // State for the election form
    const [electionName, setElectionName] = useState('');
    const [description, setDescription] = useState('');
    
    // State for candidates
    const [candidateInput, setCandidateInput] = useState('');
    const [candidates, setCandidates] = useState([]);

    const [modalVisible, setModalVisible] = useState(false);
    const [modalMessage, setModalMessage] = useState('');
    const [isSuccess, setIsSuccess] = useState(false);

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
                const id = message.data.data.postTransaction.id;
                setModalMessage(`Election created successfully! ID: ${id}`);
                setIsSuccess(true);

            } else {
                console.error("Election creation failed:", message.data.error, JSON.stringify(message.data.errors));
                setModalMessage(`Election creation failed: ${message.data.error}`);
                setIsSuccess(false);
            }
            setModalVisible(true);
          }
        };
    
        sdk.addMessageListener(messageHandler);
    
        return () => {
          sdk.removeMessageListener(messageHandler);
        };
      }, []);

    
    
    // Handle form submission (currently just logs the election data)
    function handleSubmit(e) {
        e.preventDefault();
        if (sdkRef.current) {
            try {
                sdkRef.current.sendMessage({
                    type: 'commit',
                    direction: 'commit',
                    amount: "1",
                    data: {
                        "type": "election",
                        "name": electionName,
                        "description": description,
                        "candidates": candidates
                    },
                    recipient: ELECTION_LIST_KEYS["pub_key"],
                })
            }
            catch (err) {
                console.error("Election wasn't created", err)
            }
        }
        
        // Reset the form
        setElectionName('');
        setDescription('');
        setCandidates([]);
    }
    
    // Handle adding a candidate to the list
    function addCandidate() {
        if (candidateInput && !candidates.includes(candidateInput)) {
            setCandidates([...candidates, candidateInput]);
            setCandidateInput(''); // Clear the input after adding
        }
    }

    function removeCandidate(toRemove) {
        setCandidates(candidates.filter(candidate => candidate !== toRemove))
    }

    return (
        <>
            <Button onClick={() => setCreateElection(false)}>View Elections</Button>
            <h1>Create Election</h1>
            <Form onSubmit={handleSubmit}>
                <div className="padding">
                    <label>
                        Election Name:
                        <Input
                            value={electionName}
                            onChange={(e) => setElectionName(e.target.value)}
                            placeholder="Enter the election name"
                        />
                    </label>
                </div>
                <div className="padding">
                    <label>
                        Description:
                        <Input.TextArea
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            placeholder="Enter election description"
                        />
                    </label>
                </div>
                <div className="padding">
                    <label>
                        Add Candidate:
                        <Input
                            value={candidateInput}
                            onChange={(e) => setCandidateInput(e.target.value)}
                            onPressEnter={addCandidate} // Add candidate when Enter is pressed
                            placeholder="Enter candidate name"
                        />
                    </label>
                    <Button onClick={addCandidate} type="primary">Add Candidate</Button>
                </div>
                
                <div className="candidateList">
                    <h3>Candidate List:</h3>
                    {candidates.length === 0 ?
                    <></>
                    :
                    <List
                        size="small"
                        bordered
                        dataSource={candidates}
                        renderItem={candidate => (
                            <List.Item>
                                {candidate}
                                <Button 
                                    type="danger" 
                                    onClick={() => removeCandidate(candidate)} 
                                    size="small" 
                                    style={{ marginLeft: '10px', color: "red"}}
                                >
                                    Remove
                                </Button>
                            </List.Item>
                        )}
                    />
                    }
                </div>
                
                <Button type="primary" onClick={handleSubmit}>Create Election</Button>
            </Form>

            <Modal
                open={modalVisible}
                onOk={() => setModalVisible(false)}
                onCancel={() => setModalVisible(false)}
                title={isSuccess ? "Success" : "Error"}
                okText="Close"
                cancelButtonProps={{ style: { display: 'none' } }}
                centered
                closable={false}
            >
                <p>{modalMessage}</p>
            </Modal>
        </>
    );
}

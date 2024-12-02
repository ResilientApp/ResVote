import React, { useState } from "react";
import { Button, Input, Form, List } from "antd";
import { addElectionToResDB } from "../../api";
import "./CreateElectionView.css"

export default function CreateElectionView(params) {
    const { setCreateElection } = params;
    
    // State for the election form
    const [electionName, setElectionName] = useState('');
    const [description, setDescription] = useState('');
    
    // State for candidates
    const [candidateInput, setCandidateInput] = useState('');
    const [candidates, setCandidates] = useState([]);
    
    // Handle form submission (currently just logs the election data)
    function handleSubmit(e) {
        e.preventDefault();
        const electionData = {
            electionName,
            description,
            candidates,
        };

        const electionID = addElectionToResDB(electionData);
        
        // Handle the election creation (send electionData to your API or state)
        console.log("Election created:", electionData);
        
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
        setCandidates(candidates.filter(candidate => candidate != toRemove))
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
        </>
    );
}

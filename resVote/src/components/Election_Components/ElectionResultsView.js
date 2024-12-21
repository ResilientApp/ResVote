import React, { useEffect, useState } from "react";
import { Button } from "antd"
import { getVotes } from "../../mongoDB/mongoAPI";

export default function ElectionResultsView(params) {
    const { electionToViewResultsIn, setElectionToViewResultsIn } = params;
    const { name, description, candidates } = electionToViewResultsIn;
    console.log("election =",electionToViewResultsIn);

    return (
        <>
            <Button onClick={() => setElectionToViewResultsIn(null)}>Return to Elections</Button>
            <h1>Viewing results for {name}</h1>
        </>
    )
}
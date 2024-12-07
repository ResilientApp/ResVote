import React, { useEffect, useState } from "react";
import { Button } from "antd"
import { getVotes } from "../../mongoDB/mongoAPI";

export default function ElectionResultsView(params) {
    const { election, setElectionToViewResultsIn } = params;
    console.log("election =",election);

    return (
        <>
            <Button onClick={() => setElectionToViewResultsIn(null)}>Return to Elections</Button>
            <h1>Viewing results for {election}</h1>
        </>
    )
}
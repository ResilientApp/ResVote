import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function HomeView() {
    return (
        <>
        <nav>
            <ul>
                <li>
                    <p>Login</p>
                </li>
            </ul>
        </nav>
        <h1>Welcom to ResVote</h1>
        <p> A first of its kind votting pplication using a distributed database,
            helping to secure elections from 3rd party tamperers.
        </p>
        </>
    )
}
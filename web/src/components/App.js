import "bootstrap/dist/css/bootstrap.min.css"
import {Nav, Navbar} from "react-bootstrap-v5";
import React, {useState} from "react";
import "./styles.css"
import {DATA_URL} from "./const";
import {VideoView} from "./VideoView";
import {Info} from "./Info"

function App(props) {
    const [page, setPage] = useState(0)

    return (
        <div>
            <Navbar bg="secondary" variant="dark" className="mb-1">
                <div onClick={() => setPage(1)} className="navbar-brand">Стрим</div>
                <Nav className="mr-auto">
                    <div onClick={() => setPage(0)} className="nav-link cursor-pointer">Detected</div>
                    <div onClick={() => setPage(1)} className="nav-link cursor-pointer">Raw</div>
                </Nav>
            </Navbar>
            <div className="d-flex">
                <VideoView stream={DATA_URL + (page === 0 ? "detected-stream" : "raw-stream")}/>
                <Info/>
            </div>

        </div>
    )
}

export default App;

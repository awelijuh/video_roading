import "bootstrap/dist/css/bootstrap.min.css"
import {Nav, Navbar} from "react-bootstrap-v5";
import React, {useState} from "react";
import "./styles.css"
import {DATA_URL} from "./const";
import {VideoView} from "./VideoView";
import {Info} from "./Info"

function App(props) {
    const [page, setPage] = useState(0)
    const [options, setOptions] = useState({size: '1080', type: 'detected'})

    return (
        <div>
            {/*<Navbar bg="secondary" variant="dark" className="mb-1">*/}
            {/*    <div onClick={() => setPage(1)} className="navbar-brand">Стрим</div>*/}
            {/*    <Nav className="mr-auto">*/}
            {/*        <div onClick={() => setPage(0)} className="nav-link cursor-pointer">Detected</div>*/}
            {/*        <div onClick={() => setPage(1)} className="nav-link cursor-pointer">Raw</div>*/}
            {/*    </Nav>*/}
            {/*</Navbar>*/}
            <div className="d-flex mt-2">
                <VideoView stream={DATA_URL + "stream?type=" + options?.type + "&size=" + options?.size}/>
                <Info options={options} onChangeOptions={d => setOptions(d)}/>
            </div>

        </div>
    )
}

export default App;

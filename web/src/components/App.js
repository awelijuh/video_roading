import "bootstrap/dist/css/bootstrap.min.css"
// import 'bootstrap/scss/bootstrap.scss'
import {Nav, Navbar} from "react-bootstrap-v5";
import React, {useState} from "react";
import "./styles.css"
import {DATA_URL} from "./const";
import {VideoView} from "./VideoView";
import {Info} from "./Info"
import {VideoTable} from "./video_table";

function App(props) {
    const [page, setPage] = useState(1)
    const [options, setOptions] = useState({size: '480', type: 'detected'})

    return (
        <div>
            <Navbar bg="secondary" variant="dark" className="mb-1">
                <div onClick={() => setPage(0)} className="navbar-brand"></div>
                <Nav className="mr-auto">
                    <div onClick={() => setPage(1)} className="nav-link cursor-pointer">Записи</div>
                    <div onClick={() => setPage(0)} className="nav-link cursor-pointer">Видео</div>
                </Nav>
            </Navbar>
            <div className="d-flex mt-2">
                {
                    page === 0
                        ? <VideoView stream={DATA_URL + "stream?type=" + options?.type + "&size=" + options?.size}/>
                        : <VideoTable/>
                }
                <Info showType={page === 0} options={options} onChangeOptions={d => setOptions(d)}/>
            </div>

        </div>
    )
}

export default App;

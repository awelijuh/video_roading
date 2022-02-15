import {Container} from "react-bootstrap-v5";
import React, {useEffect, useState} from "react";
import {DATA_URL} from "./const";


export function VideoView({stream}) {

    return (
        <Container className="d-flex">
            <img className="ms-auto me-auto" style={{height: 'calc(100vh - 70px)'}} src={stream}/>
        </Container>
    )
}

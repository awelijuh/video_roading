import React, {useEffect, useState} from "react";
import {DATA_URL} from "./const";

function Item({name, value}) {
    return (
        <tr>
            <td className="fw-bold" style={{width: '200px'}}>{name}:</td>
            <td className="text-end">{value}</td>
        </tr>
    )
}

export function Info(props) {
    const [params, setParams] = useState();

    async function fetchFps() {
        let resp = await fetch(DATA_URL + "params")
        if (resp.ok) {
            let f = await resp.json()
            setParams(f)
        }
    }

    useEffect(() => {
        const interval = setInterval(() => {
            fetchFps()
        }, 5000);
        return () => clearInterval(interval);
    }, [props]);


    return (
        <div className="w-auto me-2 mt-1">
            <div className="d-inline-block border p-2">
                <table>
                    <tbody>
                    <Item name="read fps" value={params?.read_fps?.toFixed?.(3)}/>
                    <Item name="detect fps" value={params?.detect_fps?.toFixed?.(3)}/>
                    <Item name="yolo time" value={params?.yolo_time?.toFixed?.(3)}/>
                    <Item name="DeepSort time" value={params?.deep_sort_time?.toFixed?.(3)}/>
                    </tbody>
                </table>
            </div>

        </div>
    )
}

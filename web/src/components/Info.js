import React, {useEffect, useState} from "react";
import {DATA_URL} from "./const";
import {FormControl, InputLabel, MenuItem, Select} from "@material-ui/core";

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
    let options = props.options
    let onChangeOptions = props.onChangeOptions

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

    console.log('opt', options)

    return (
        <div className="w-auto me-2">
            <div className="border p-2">
                <FormControl className="m-2 w-100" variant="standard" sx={{m: 1, minWidth: 120}}>
                    <InputLabel id="type-label">Тип</InputLabel>
                    <Select
                        labelId="type-label"
                        id="type-select"
                        value={options?.type}
                        label="Тип"
                        variant="standard"
                        sx={{width: 400}}
                        onChange={(e) => onChangeOptions?.({...options, type: e.target.value})}
                    >
                        <MenuItem value={"raw"}>raw</MenuItem>
                        <MenuItem value={"detected"}>detected</MenuItem>
                    </Select>
                </FormControl>
                <FormControl className="m-2 w-100" variant="standard" sx={{m: 1, minWidth: 120}}>

                    <InputLabel id="size-label">Размер</InputLabel>
                    <Select
                        labelId="size-label"
                        id="size-select"
                        value={options?.size}
                        label="Размер"
                        variant="standard"
                        sx={{width: 400}}
                        onChange={(e) => onChangeOptions?.({...options, size: e.target.value})}
                    >
                        <MenuItem value={"1080"}>1080p</MenuItem>
                        <MenuItem value={"720"}>720p</MenuItem>
                        <MenuItem value={"540"}>540p</MenuItem>
                        <MenuItem value={"480"}>480p</MenuItem>
                        <MenuItem value={"360"}>360p</MenuItem>
                    </Select>
                </FormControl>
            </div>
            <div className="border p-2">
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

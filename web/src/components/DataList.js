import React, {forwardRef, useEffect, useState} from "react";
import {DATA_URL} from "./const";
import MaterialTable from "material-table";
import AddBox from '@material-ui/icons/AddBox';
import ArrowDownward from '@material-ui/icons/ArrowDownward';
import Check from '@material-ui/icons/Check';
import ChevronLeft from '@material-ui/icons/ChevronLeft';
import ChevronRight from '@material-ui/icons/ChevronRight';
import Clear from '@material-ui/icons/Clear';
import DeleteOutline from '@material-ui/icons/DeleteOutline';
import Edit from '@material-ui/icons/Edit';
import FilterList from '@material-ui/icons/FilterList';
import FirstPage from '@material-ui/icons/FirstPage';
import LastPage from '@material-ui/icons/LastPage';
import Remove from '@material-ui/icons/Remove';
import SaveAlt from '@material-ui/icons/SaveAlt';
import Search from '@material-ui/icons/Search';
import ViewColumn from '@material-ui/icons/ViewColumn';
import RefreshIcon from '@material-ui/icons/Refresh';
import moment from "moment";
import {
    Container,
    FormControl,
    IconButton,
    InputLabel,
    LinearProgress,
    MenuItem,
    Paper,
    Select,
    TextField
} from "@material-ui/core";
import {Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";

const tableIcons = {
    Add: forwardRef((props, ref) => <AddBox {...props} ref={ref}/>),
    Check: forwardRef((props, ref) => <Check {...props} ref={ref}/>),
    Clear: forwardRef((props, ref) => <Clear {...props} ref={ref}/>),
    Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref}/>),
    DetailPanel: forwardRef((props, ref) => <ChevronRight {...props} ref={ref}/>),
    Edit: forwardRef((props, ref) => <Edit {...props} ref={ref}/>),
    Export: forwardRef((props, ref) => <SaveAlt {...props} ref={ref}/>),
    Filter: forwardRef((props, ref) => <FilterList {...props} ref={ref}/>),
    FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref}/>),
    LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref}/>),
    NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref}/>),
    PreviousPage: forwardRef((props, ref) => <ChevronLeft {...props} ref={ref}/>),
    ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref}/>),
    Search: forwardRef((props, ref) => <Search {...props} ref={ref}/>),
    SortArrow: forwardRef((props, ref) => <ArrowDownward {...props} ref={ref}/>),
    ThirdStateCheck: forwardRef((props, ref) => <Remove {...props} ref={ref}/>),
    ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref}/>)
};


function DataTable({data}) {


    return (

        <MaterialTable options={{padding: "dense"}} title={"Данные"} icons={tableIcons} columns={[
            {
                title: 'Время',
                render: row => (
                    <span
                        title={moment(Date.parse(row.time)).format("DD.MM.YYYY HH:mm:ss")}>
                            {moment(Date.parse(row.time)).format("HH:mm:ss.SSS")}
                        </span>)
            },
            {title: 'Машины', field: 'car'},
            {title: 'Грузовики', field: 'truck'},
            {title: 'Автобусы', field: 'bus'},
            // {title: 'Люди', field: 'person'},
            {title: 'Все', field: 'all'},
            // {title: 'Фото', field: 'image'},
        ]} data={data}/>

    )
}

function Filter({onChange, value, onUpdate}) {

    return (
        <div className="d-flex">
            <TextField
                className="m-2"
                label="С"
                type="datetime-local"
                defaultValue={value?.start_time}
                sx={{width: 250}}
                InputLabelProps={{
                    shrink: true,
                }}
                onBlur={(e) => onChange?.({...value, start_time: e.target.value})}
            />
            <TextField
                className="m-2"
                label="До"
                type="datetime-local"
                defaultValue={value?.end_time}
                sx={{width: 250}}
                InputLabelProps={{
                    shrink: true,
                }}
                onBlur={(e) => onChange?.({...value, end_time: e.target.value})}
            />

            <FormControl className="m-2" variant="standard" sx={{m: 1, minWidth: 120}}>
                <InputLabel id="demo-simple-select-label">Масштаб</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={value?.scale}
                    label="Масштаб"
                    variant="standard"
                    sx={{width: 250}}
                    onChange={(e) => onChange?.({...value, scale: e.target.value})}
                >
                    <MenuItem value={"null"}>Все</MenuItem>
                    <MenuItem value={"second"}>Секунда</MenuItem>
                    <MenuItem value={"minute"}>Минута</MenuItem>
                    <MenuItem value={"hour"}>Час</MenuItem>
                    <MenuItem value={"day"}>День</MenuItem>
                    <MenuItem value={"week"}>Неделя</MenuItem>
                </Select>

            </FormControl>

            <FormControl disabled={value?.scale === 'null'} className="m-2" variant="standard"
                         sx={{m: 1, minWidth: 120}}>
                <InputLabel id="aggregate-select-label">Функция</InputLabel>
                <Select
                    labelId="aggregate-select-label"
                    id="demo-simple-select"
                    value={value?.aggregate}
                    label="Функция"
                    variant="standard"
                    sx={{width: 250}}
                    onChange={(e) => onChange?.({...value, aggregate: e.target.value})}
                >
                    <MenuItem value={"average"}>Среднее</MenuItem>
                    <MenuItem value={"median"}>Медиана</MenuItem>
                    <MenuItem value={"max"}>Максимум</MenuItem>
                    <MenuItem value={"min"}>Минимум</MenuItem>
                </Select>

            </FormControl>
            <div className="ms-auto mt-auto mb-auto">
                <IconButton onClick={() => onUpdate?.()}>
                    <RefreshIcon/>
                </IconButton>
            </div>
        </div>

    )
}

function DataChart({data}) {
    return (
        <ResponsiveContainer width='100%' height={400}>
            <BarChart height={400} data={data}>
                <XAxis dataKey="timeL"/>
                <YAxis yAxisId="a"/>
                <YAxis yAxisId="b" orientation="right"/>
                <Legend/>
                <Tooltip/>
                <CartesianGrid vertical={false}/>
                <Bar fill="#00CCFF" yAxisId="a" dataKey="all">
                </Bar>

            </BarChart>
        </ResponsiveContainer>
    )
}

function getDefaultStartTime() {
    let time = new Date();
    time.setHours(0)
    time.setMinutes(0)
    time.setSeconds(0)
    time.setMilliseconds(0)

    return moment(time).format("YYYY-MM-DDTHH:mm")
}

function getDefaultEndTime() {
    let time = new Date();
    time.setHours(0)
    time.setMinutes(0)
    time.setSeconds(0)
    time.setMilliseconds(0)
    time = moment(time).add(1, 'day')

    return time.format("YYYY-MM-DDTHH:mm")
}

function DataList(props) {
    console.log(getDefaultStartTime())
    console.log(getDefaultEndTime())
    const [data, setData] = useState()
    const [loading, setLoading] = useState(true)

    const [filter, setFilter] = useState({
        scale: 'hour',
        start_time: getDefaultStartTime(),
        end_time: getDefaultEndTime(),
        aggregate: 'average',
    })


    function getUrl() {
        let url = new URL(DATA_URL + "frames")
        let f = {...filter}
        if (f.scale === 'null') {
            f.scale = ""
        }
        f.start_time = new Date(f.start_time).toISOString().replace('Z', '')
        f.end_time = new Date(f.end_time).toISOString().replace('Z', '')
        url.search = new URLSearchParams(f).toString();
        return url;
    }

    async function fetchTableData() {
        setLoading(true)
        let url = getUrl().toString()
        let resp = await fetch(url)
        if (!resp.ok) {
            setLoading(false)
            return
        }
        let d = await resp.json()

        for (let i in d) {
            d[i].time = new Date(d[i].time)
            d[i].timeL = moment(new Date(d[i].time)).format("DD.MM.YYYY HH:mm:ss")
        }
        console.log(url.toString(), getUrl().toString())
        console.log('eq', url.toString() === getUrl().toString())
        if (url.toString() !== getUrl().toString()) {
            console.log('not equal')
            return
        }

        setData(d)
        setLoading(false)
    }

    useEffect(() => {
        fetchTableData()
    }, [filter])

    return (
        <Container>
            <Paper className="p-3 m-2">
                <Filter value={filter} onChange={v => setFilter(v)} onUpdate={() => fetchTableData()}/>
            </Paper>

            {
                loading
                    ? <LinearProgress className="m-2"/>
                    : <></>
            }
            <Paper className="p-3 m-2">
                <DataChart data={data}/>
            </Paper>

            <Paper className="p-3 m-2">
                <DataTable data={data}/>
            </Paper>
        </Container>

    )
}

export default DataList

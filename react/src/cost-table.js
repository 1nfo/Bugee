import React from 'react'
import ReactDOM from 'react-dom'
import autoBind from 'react-autobind'
import ReactDataGrid from "react-data-grid"
import { Toolbar, Data, Filters, Editors} from "react-data-grid-addons"


const {
    NumericFilter,
    AutoCompleteFilter,
    MultiSelectFilter,
    SingleSelectFilter
} = Filters;

const {
    AutoComplete,
    DropDownEditor,
    ContainerEditorWrapper,
    SimpleTextEditor,
    CheckboxEditor
} = Editors

const saveBtnStyle = { 
    position: 'relative', 
    top: '1px',
    padding: '4px', 
    paddingBottom: '10px', 
    fontSize: '14px', 
    height: '30px',
    backgroundColor: 'red'
}

const DateFormatter = function(props){
    const click = () => props.row.del(props.row.id)
    return (
        <div className="container">
            <span>{props.value}</span> 
            <a role='button' onClick={click} className='text-danger font-weight-bold float-right'>X</a>
        </div>
    )
}

class OverrideNumericFilter extends NumericFilter{

    render() {
        let inputKey = 'header-filter-' + this.props.column.key;
        let columnStyle = {
            float: 'left',
            marginRight: 5,
            maxWidth: '80%',
        };

        return (
            <div>
                <div className='Select-control'>
                    <input key={inputKey} type="text" style={{ fontSize: '12px', border:'0px' }}
                        placeholder="e.g. 3,10-15,>20" className="Select-input" 
                        onChange={this.handleChange} onKeyPress={this.handleKeyPress} />
                </div>
            </div>
        );
    }
}

class DateEditor extends React.Component {
    constructor(props) {
        super(props)
        this.state = { date: props.value }
        autoBind(this)
    }

    getValue() {
        return { date:this.state.date }
    }

    getInputNode() {
        return ReactDOM.findDOMNode(this)
    }

    handleChange(event) {
        this.setState({ date: event.target.value })
    }

    render() {
        return (
            <input type='text' onChange={this.handleChange} value={this.state.date} />
        )
    }
}

const reformatInput = function(input){
    if('date' in input){
        var date = new Date(input.date)
        if(isNaN(date.getTime())){
            delete input.date
        } else {
            input.date = date.toISOString().split('T')[0]
        }
    }
    if('amount' in input){
        var amount = parseFloat(input.amount).toFixed(2)
        if (isNaN(amount)) {
            delete input.amount
        } else {
            input.amount = amount
        }
    }
    return input
}

const isUpdated = function(origin, updated){
    for(const key of Object.keys(updated)){
        if (origin[key] != updated[key]){
            return true
        }
    }
    return false
}


export default class CostTable extends React.Component {

    constructor(props) {
        super(props)
        this.id = props.id
        this.refresh = props.refresh
        this.state = {
            rows: props.rows,
            sortColumn: null,
            sortDirection: null,
            filter: {},
            rowsToSave: []
        }

        this.cols = [
            {
                key: "date",
                name: "Cost Date",
                width: 250,
                resizable: true,
                sortable: true,
                filterable: true,
                editable: true,
                // TODO datepicker
                editor: <DateEditor/>,
                formatter: DateFormatter,
                filterRenderer: AutoCompleteFilter
            },
            {
                key: "amount",
                name: "Cost Amount",
                width: 200,
                resizable: true,
                sortable: true,
                filterable: true,
                editable: true,
                filterRenderer: OverrideNumericFilter
            },
            {
                key: "note",
                name: "Cost Note",
                width: 450,
                resizable: true,
                sortable: false,
                filterable: true,
                editable: true,
                filterRenderer: AutoCompleteFilter
            }
        ]
        autoBind(this)
    }

    componentWillReceiveProps (props) {
        this.setState({ rows: props.rows });
    }

    getRows() {
        return Data.Selectors.getRows(this.state);
    } 

    rowGetter(i){
        var row = this.getRows()[i]
        row = Object.assign({ del: this.deleteRow }, row)
        return row
    }

    handleSort(sortColumn, sortDirection) {
        this.setState({ sortColumn, sortDirection})
    }

    onAddFilter(filter) {
        let newFilters = Object.assign({}, this.state.filters);
        if (filter.filterTerm) {
            newFilters[filter.column.key] = filter;
        } else {
            delete newFilters[filter.column.key];
        }
        this.setState({ filters: newFilters });
    }

    onClearFilters() {
        this.setState({ filters: {} });
    }

    getValidFilterValues(columnId) {
        return this.state.rows.map(r => r[columnId]).filter((item, i, a) => {
                return i === a.indexOf(item);
        });
    }

    onGridRowsUpdated({ fromRow, toRow, updated }) {
        var rows = this.state.rows.slice()
        updated = reformatInput(updated)
        if (isUpdated(rows[fromRow], updated)) {
            var rowsToSave = this.state.rowsToSave.slice()
            rows[fromRow] = Object.assign({}, rows[fromRow], updated)
            rowsToSave.push(fromRow)
            this.setState({ rows, rowsToSave })
        }
    }

    addRow(row){
        var rows = this.state.rows.slice()
        var rowsToSave = this.state.rowsToSave.slice()
        rows.push({ id: "new-"+Date.now(), date: new Date().toISOString().split('T')[0], amount: 0, note: '' })
        rowsToSave.push(row.newRowIndex)
        this.setState({ rows, rowsToSave})
    }

    deleteRow(id){
        if(confirm("Confirm to delete")){
            var that = this
            if(isNaN(id)){
                that.setState({ rows: that.state.rows.filter((r) => r.id != id) })
                return;
            }
            fetch("/cost/"+id , {})
                .then((r) => r.json())
                .then(function(res) {
                    if (res.result) {
                        that.setState({ rows: that.state.rows.filter((r) => r.id != id) })
                    } else {
                        alert(res.enum)
                        console.log(res.details)
                    }
                })
        }
    }

    sendRowsToSave(event) {
        var that = this
        var rowsToSend = [... new Set(this.state.rowsToSave)].map(function(index) {
            return that.state.rows[index]
        })
        fetch('/budget/' + this.id + '/costs', { method: 'POST', body: JSON.stringify(rowsToSend)})
            .then((d) => d.json())
            .then(function(res){
                if(res.result){
                    that.setState({ rowsToSave: [] })
                    that.refresh()
                    //event.target.hidden = true
                } else {
                    alert(res.enum)
                    console.log(res.details)
                }
            })
    }

    render() {
        var that = this
        return (
            <div>
                <ReactDataGrid
                    columns={this.cols}
                    rowGetter={this.rowGetter}
                    rowsCount={this.getRows().length}
                    minHeight={330}
                    onGridSort={this.handleSort}
                    onAddFilter={this.onAddFilter}
                    onClearFilters={this.onClearFilters}
                    onGridRowsUpdated={this.onGridRowsUpdated}
                    enableCellSelect={true}
                    getValidFilterValues={this.getValidFilterValues}
                    toolbar={
                        <Toolbar onAddRow={that.addRow}
                            enableFilter={true}
                            children={
                                
                                <button className='react-grid-Toolbar text-white' 
                                        hidden={this.state.rowsToSave.length==0}
                                        style={saveBtnStyle} 
                                        onClick={that.sendRowsToSave}>
                                        Save
                                </button>
                            }
                        />
                    }
                />
            </div>
        )
    }
}

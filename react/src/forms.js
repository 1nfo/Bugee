import React from 'react'
import ReactDOM from 'react-dom'
import autoBind from 'react-autobind'
import moment from 'moment'
import DatePicker from 'react-datepicker'

import 'react-datepicker/dist/react-datepicker.css';

const time_unit_options = [
    'years',
    'months',
    'weeks',
    'days'
]
 
export default class NewBudgetForm extends React.Component{

    constructor(props) {
        super(props)
        this.state = {
            recursive: false,
            budgetName: '',
            amount: 0,
            startdate: new Date(),
            enddate: new Date(),
            howlong: 0,
            timeunit:'months'
        }
        this.hideAndRefresh = props.hideAndRefresh
        autoBind(this)
    }

    submit(){
        var that = this
        var resource = '/budget/'
        if(that.state.recursive){
            resource += 'recursive'
        } else {
            resource += 'occasional'
        }
        var req = Object.assign({}, this.state)
        req.startdate = req.startdate.getTime()
        req.enddate = req.enddate.getTime()
        fetch(resource, { 
            method: 'POST',
            body: JSON.stringify(req) 
        }).then(function(response) {
            return response.json()
        }).then(function(data) {
            if(data.result){
                that.hideAndRefresh()
            } else {
                alert(data.enum)
                console.log(data.details)
            }
        })
    }

    onChangeFactory(state_key, target_key='value'){
        var that = this
        var handler = function(event) {
            that.setState({ [state_key]: event.target[target_key] })
        }
        return handler
    }

    onChangeDate(state_key){
        var that = this
        var handler = function(date){
            that.setState({[state_key]:date})
        }
        return handler
    }

    listOptions(arr){
        var selected = this.state.timeunit
        return arr.map(function(d) {
            return <option key={d} value={d}>{d}</option>
        })
    }

    render() {
        return (
            <div className="container-fluid">
                <div className="form-check mb-3">
                    <input type="checkbox" className="form-check-input" id="recursive_checkbox"
                        checked={this.state.recursive} onChange={this.onChangeFactory('recursive', 'checked')} />
                    <label className="form-check-label" htmlFor="recursive_checkbox">Recursive</label>
                </div>
                <div className="form-group input-group mb-3">
                    <div className="form-label-group">
                        <input type="text" className="form-control" id="budget_name_input" 
                            onChange={this.onChangeFactory('budgetName')} />
                        <label className="form-text-label" htmlFor="budget_name_input">Budget Name</label>
                    </div>
                    <div className="form-label-group">
                        <input type="text" id="new_budget_amount" className="form-control" 
                            onChange={this.onChangeFactory('amount')} />
                        <label className="form-text-label"  htmlFor="new_budget_amount">Amount</label>
                    </div>
                </div>
                <div className="form-group input-group mb-3">
                    <div className="mr-4">
                        <DatePicker dateFormat="yyyy/MM/dd"
                                    selected={this.state.startdate} 
                                    onChange={this.onChangeDate('startdate')} />
                    </div>
                    <div className="mr-4" hidden={this.state.recursive}>
                        <DatePicker dateFormat="yyyy/MM/dd"
                                    selected={this.state.enddate} 
                                    onChange={this.onChangeDate('enddate')} />
                    </div>
                    <div className="form-label-group" hidden={!this.state.recursive}>
                        <input type="text" id="new_budget_time_delta" className="form-control" 
                            onChange={this.onChangeFactory('howlong')} />
                        <label className="form-text-label" htmlFor="new_budget_time_delta">How long</label>
                    </div>
                    <select onChange={this.handleTimeUnitSelect} defaultValue={this.state.timeunit} hidden={!this.state.recursive}>
                        {this.listOptions(time_unit_options)}
                    </select>
                </div>
                <div className="fixed-bottom px-3 mb-3"> 
                    <button className="btn btn-primary btn-block" onClick={this.submit}>Create</button>
                </div>
            </div>
        )
    }
}
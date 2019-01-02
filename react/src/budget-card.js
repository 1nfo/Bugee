import React from 'react'
import ReactDOM from 'react-dom'
import autoBind from 'react-autobind'
import SkyLight from 'react-skylight'
import ProgressBar from 'react-bootstrap/lib/ProgressBar'
import CostTable from './cost-table'

export default class BudgetCard extends React.Component {

    constructor(props) {
        super(props)
        Object.assign(this, props.budget)
        this.state = { rows:[] }
        autoBind(this)
    }

    clickOnCard() {
        this.getAllCosts()
        this.refs.budget_details.show()
    }

    getAllCosts() {
        fetch('/budget/' + this.id + '/costs', { method: 'GET' })
            .then((r) => r.json())
            .then((rows) => rows.map(function(row) {
                var cost = row.Cost
                return cost
            }))
            .then((rows) => this.setState({ rows }))
    }

    popup_title() {
        return 'Budget ' + this.name
    }

    render() {
        return (
            <div>
                <div className='col-sm-6 col-xl-3 h-100 mb-1 ml-1'>
                    <div className='card text-white bg-success' onClick={this.clickOnCard}>
                        <div className='card-body'>
                            Budget {this.name} <span className='pull-right'>{this.balance}/{this.amount}</span>
                            <ProgressBar now={this.balance *100 /this.amount}/>
                            <br/>
                            {new Date(this.start_date).toLocaleDateString()}  --  {new Date(this.end_date).toLocaleDateString()}
                        </div>
                    </div>
                </div>
                <SkyLight hideOnOverlayClicked ref="budget_details" title={this.popup_title()}>
                    <p className='text-right'>from {this.start_date} to {this.end_date}</p>
                    <CostTable id={this.id} rows={this.state.rows} refresh={this.getAllCosts}/>
                </SkyLight>
            </div>
        )
    }
}
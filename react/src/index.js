import React from 'react'
import ReactDOM from 'react-dom'
import autoBind from 'react-autobind'
import SkyLight from 'react-skylight'
import NewBudgetForm from './forms'
import BudgetCard from './budget-card'


class Content extends React.Component{
    constructor(props) {
        super(props)
        this.state = {
            username: 'Loading ...',
            budgets: []
        }
        this.getUsername()
        this.getAllBudgets()
        autoBind(this)
    }
 
    getUsername(){
        var that = this
        fetch("/user", { method: 'GET' }).then(function(response) {
            return response.json()
        }).then(function(data) {
            that.setState(data)
        })
    }

    getAllBudgets() {
        var that = this
        fetch("/budgets", { method: 'GET' }).then(function(response) {
            return response.json()
        }).then(function(data) {
            that.setState(data)
        })
    }

    popup () {
        this.refs.new_budget_form.show()
    }

    hideAndRefresh() {
        this.refs.new_budget_form.hide()
        this.getAllBudgets()
    }

    render() {
        return (
            <div>
                <h2> Hello, {this.state.username} </h2>
                <br/>
                <div>
                    <button className="btn btn-primary btn-block" onClick={this.popup}>New budget</button>
                </div>
                <div>
                    <SkyLight hideOnOverlayClicked ref="new_budget_form" title="New budget">
                        <NewBudgetForm hideAndRefresh={this.hideAndRefresh} />
                    </SkyLight>
                </div>
                <br/>
                <div>
                    {
                        this.state.budgets.map(function(d){
                            var budget = d.Budget
                            return <BudgetCard budget={budget} key={budget.id} />
                        })
                    }
                </div>
            </div>
        )
    }
}

const element = (
    <div className=" panel-primary panel">
        <Content />
    </div>
);

ReactDOM.render(
    element,
    document.getElementById('reactMainApp')
);
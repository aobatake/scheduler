import React from 'react';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import {getDepartmentList, changeDepartment} from '../actions';

require('../../scss/department_list.scss');

class DepartmentList extends React.Component {

  componentDidMount(){
    this.props.dispatch(getDepartmentList);
  }

  departmentClick(element,e){
    const acronym = element.slice(element.indexOf('(') + 1, element.indexOf(')'));
    this.props.dispatch(changeDepartment.bind(this,acronym));
  }

  departmentList() {
    const {department_list, department, dispatch} = this.props;
    return(
      <div className='list-group list-container'>
        {
          department_list.data.map((element, index)=>{
            const acronym = element.slice(element.indexOf('(') + 1, element.indexOf(')'));
            if (acronym === department.data) {
              return (
                <button key={index} 
                  className='active list-group-item' 
                  onClick={this.departmentClick.bind(this, element)}>
                    {element}
                </button>
              );
            }
            else {
              return (
                <button key={index} 
                  className='list-group-item'
                  onClick={this.departmentClick.bind(this, element)}>
                    {element}
                </button>
              );
            }
          })
        }
      </div>
    );
  }


  render(){
    const {department_list} = this.props;
    if (department_list.fetching === true) {
      return(<h1>Getting Department List</h1>);
    }
    else if (department_list.fetching === false && department_list.fetched === false){
      return (<h1>Error</h1>);
    } 
    else {
      return (<div>{this.departmentList()}</div>);
    }

  }
};


function mapStateToProps(state){
  return {
    department_list: state.department_list,
    department: state.department
  };
}

export default connect(mapStateToProps)(DepartmentList);

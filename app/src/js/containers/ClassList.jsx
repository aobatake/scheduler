import React from 'react';
import {connect} from 'react-redux';
import Class from './Class';
require('../../scss/department_list.scss');

class ClassList extends React.Component {
  classList(){
    const {department, class_list} = this.props;
    return (
      <div className="list-group list-container">
        {class_list.data.map((element, index)=>{
          return (<Class department={department.data} class_data={element} key={element._id} />);
        }) }
      </div>
    );
  }

  render(){
    const {department, class_list} = this.props;
    if(department.data === ''){
      return (<h1>Pick a Department</h1>);
    }
    else {
      if(class_list.fetching === true){
        return (<h1>Getting Class List</h1>);
      }
      else if(class_list.fetching === false && class_list.fetched === false){
        return (<p>{class_list.error}</p>);
      }
      else {
       return (<div>{this.classList()}</div>);
      }
    }
  }
};


function mapStateToProps(state){
  return {
    department: state.department,
    class_list: state.class_list
  };
}

export default connect(mapStateToProps)(ClassList);

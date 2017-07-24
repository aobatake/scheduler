import React from 'react';
import ClassList from '../containers/ClassList';
import DepartmentList from '../containers/DepartmentList';
require('../../scss/classes.scss');

const Classes = () => {
  return (
    <div className='container-fluid'>
      <div className='col-xs-2 department-container'>
        <DepartmentList />
      </div>
      <div className='col-xs-4'>
        <ClassList />
      </div>
      <div className='col-xs-6'>
      
      </div>
    </div>
  );
}

export default Classes;

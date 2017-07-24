import {combineReducers} from 'redux';
import departmentReducer from './department-reducer';
import departmentListReducer from './department-list-reducer';
import classListReducer from './class-list-reducer';

const allReducers = combineReducers({
  department: departmentReducer,
  department_list: departmentListReducer,
  class_list: classListReducer
})

export default allReducers;

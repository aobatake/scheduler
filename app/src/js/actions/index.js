

export const getDepartmentList = (dispatch) => {
  dispatch({type: "REQUEST_DEPARTMENT"});

  fetch('department' , 
    { 
      method: 'GET' , 
      headers: {
        "Content-Type": "application/json"
      }
    })
  .then( res => res.json())
  .then( json => {
    dispatch({type: "RECEIVED_DEPARTMENT", payload: json})
  })
  .catch( err => {
    dispatch({type: "ERROR_DEPARTMENT", payload: err})
  })
}

export const changeDepartment = (acronym, dispatch) =>{
  dispatch({type: "CHANGE_DEPARTMENT", payload: acronym});
  getClassList(acronym, dispatch);
}

const getClassList = (acronym, dispatch) => {
  dispatch({type: "REQUEST_CLASS_LIST"});
  const url = "classes/" + acronym;
  fetch(url , 
    { 
      method: 'GET' , 
      headers: {
        "Content-Type": "application/json"
      }
    })
  .then( res => res.json())
  .then( json => {
    dispatch({type: "RECEIVED_CLASS_LIST", payload: json})
  })
  .catch( err => {
    dispatch({type: "ERROR_CLASS_LIST", payload: err})
  })
}


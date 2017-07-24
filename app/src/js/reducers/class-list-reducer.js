
let initialState = {
  fecthing: false,
  fetched: false,
  data: [],
  error: null  
}

export default function(state = initialState, action) {
  switch(action.type){
    case "REQUEST_CLASS_LIST":
      return {...state, fetching: true};
      break
    case "RECEIVED_CLASS_LIST":
      return {...state, fetching: false, fetched: true, data: action.payload}
      break;
    case "ERROR_CLASS_LIST":
      return {...state, fetching: false, error: action.payload}
      break;
  }
  return state;
}

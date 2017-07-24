let initialState = {
  data: [],
  fetching: false,
  fetched: false,
  error: null
}

export default function(state = initialState, action) {
  switch(action.type){
    case "REQUEST_DEPARTMENT":
      return {...state, fetching: true };
      break;
    case "ERROR_DEPARMENT":
      return {...state, fetching: false, error: action.payload }
      break;
    case "RECEIVED_DEPARTMENT":
      return {...state, fetching: false, fetched: true, data: action.payload}
      break
  }
  return state
}

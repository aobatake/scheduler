
let initialState = {
  data: ''
}

export default function(state = initialState, action) {
  switch(action.type){
    case "CHANGE_DEPARTMENT":
      return { ...state, data: action.payload };
      break;
  }
  return state;
}

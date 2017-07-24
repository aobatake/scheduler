import React from 'react';
require('../../scss/class.scss');

class Class extends React.Component {

  constructor(props){
    super(props);
    this.state = {
      show: 'none',
      chevron: 'down'
    };
    this.changeDetails = this.changeDetails.bind(this);
  }

  changeDetails() {
    const {show} = this.state;
    if (show === 'none'){
      this.setState({
        show: 'block',
        chevron: 'up'
      });
    }
    else {
      this.setState({
        show: 'none',
        chevron: 'down'
      });
    }
  }

  render(){
    const {show, chevron} = this.state;
    const {department, class_data} = this.props;
    const display_style = { display: show };
    const chevron_class = 'glyphicon glyphicon-chevron-'+ chevron + ' pull-right'

    return (
      <button className='list-group-item' onClick={this.changeDetails}>
        <b>
          <span>{department}{class_data.Course_Number}</span>
          <span className={chevron_class}></span>
        </b>
        <div style={display_style} className="class-details">
          <div><b>Course:</b> {class_data.Course_Title}</div>
          <div><b>CRN:</b> {class_data.CRN}</div>
          <div><b>Section:</b> {class_data.Section}</div>
          <div><b>Credits:</b> {class_data.Credits}</div>
          <div><b>Instructor:</b> {class_data.Instructor}</div>
          <div><b>Subject:</b> {class_data.Subject}</div>
          <div><b>Class Info:</b>
          <ul className="class-info list-group">
            {class_data.info.map( (element, index) => {
              return (
                  <li className="list-group-item">
                    <b>Meeting Time:</b> {element.Days} {element.Time}<br/>
                    <b>Room:</b> {element.Room}
                  </li> 
              );
            })  }
          </ul>
          </div>
        </div>
      </button>
    );
  }

};

export default Class;

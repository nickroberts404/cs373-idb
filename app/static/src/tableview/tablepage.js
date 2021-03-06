// tablepage.js

var React = require('react');
var Table = require('./table.js');
var NavBar = require('../partials/navbar.js');
// var subjectHeaders = require('./headers.js');
var marvel = require('../marvel.js');
var data;

class TablePage extends React.Component {

	constructor() {
		super();
		this.navigateToDetail = this.navigateToDetail.bind(this);
		this.state = {data: []};
	}

	navigateToDetail(id) {
		console.log("Navigating to "+this.props.route.path+'/'+id);
		this.props.history.push(this.props.route.path+'/'+id);
	}

	componentWillReceiveProps() {
		console.log("component mounting");
		var populate;
		var subject = getSubject(this.props.route.path);
		if (subject === 'characters') populate = marvel.getCharacters
		else if (subject === 'comics') populate = marvel.getComics
		else populate = marvel.getCreators
		populate(20, 0, (err, data) => {
			if (err) console.err("[TablePage:componentDidMount] There's been an error retrieving data!");
			else this.setState({data: data[subject].slice(0, 20)});
		});
	}

	render() {
		var subject = getSubject(this.props.route.path);
		var headers = subjectHeaders[subject];
		return (
			<div className="table-page">
				<NavBar />
				<div className="container">
					<h1>{this.props.route.title}</h1>
					<Table 
						content={this.state.data} 
						headers={headers} 
						navigate={this.navigateToDetail}
						subject={subject}
					/>
				</div>
			</div>
		)
	}
}

function getSubject(path) {
	if (path === '/characters') return "characters";
	else if (path === '/comics') return "comics";
	else return "creators";
}

module.exports = TablePage;



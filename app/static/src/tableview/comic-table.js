
// comic-table.js

var React = require('react');
var Table = require('./table.js');
var NavBar = require('../partials/navbar.js');
var Loader = require('../partials/loader.js');
var Paginator = require('../partials/paginator.js');
var marvel = require('../marvel.js');
var LIMIT = 20;
var headers = [
	{key: "thumbnail", value: "Thumbnail"},
	{key: "title", value: "Title"},
	{key: "id", value: "ID"},
	{key: "issue_num", value: "Issue"},
	{key: "page_count", value: "Pages"},
	{key: "number_of_stories", value: "# of Stories"}
];

class ComicTable extends React.Component {

	constructor(props) {
		super(props);
		this.navigateToDetail = this.navigateToDetail.bind(this);
		var page = parseInt(props.location.query.page) || 1;
		this.state = {data: null, page: page, lastPage: null, loading: true};
	}

	navigateToDetail(id) {
		console.log("Navigating to "+this.props.route.path+'/'+id);
		this.props.history.push(this.props.route.path+'/'+id);
	}

	componentDidMount() {
		this.getData(this.state.page);
	}

	getData(page) {
		var offset = (page-1)*LIMIT;
		marvel.getComics(LIMIT, offset, (err, data) => {
			if (err) console.error("[TablePage:componentDidMount] There's been an error retrieving data!");
			else this.setState({data: data.comics, lastPage: Math.ceil(data.count/LIMIT)});
			this.setState({loading: false});
		});
	}

	render() {
		if(this.state.data){
			return (
				<div className="table-page">
					<NavBar />
					<Paginator 
						pagePath="/comics"
						currentPage={this.state.page}
						lastPage={this.state.lastPage}
						pageLimit={5}
						changePage={this.getData.bind(this)} 
					/>
					<div className="container">
						<h1>{this.props.route.title}</h1>
						<Table 
							content={this.state.data} 
							headers={headers} 
							navigate={this.navigateToDetail}
							subject="comics"
						/>
					</div>
				</div>
			)
		} else {
			return (
				<Loader loading={this.state.loading} />
			)
		}
	}
}

module.exports = ComicTable;



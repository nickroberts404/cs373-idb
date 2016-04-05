// creatorpage.js

var React = require('react');
var NavBar = require('../partials/navbar.js');
var data = require('../../mockdata.json');

class CreatorPage extends React.Component {
	render() {
		var creatorData = data.details[this.props.params.creatorId];
		if (creatorData) {
			return (
				<div className="character-page">
					<NavBar />
					<div className="container">
						<div className="row">
							<div className="col-sm-4 thumbnail-wrapper">
								<img src={creatorData.thumbnail} />
							</div>
							<div className="col-sm-6">
								<h2>{creatorData.firstName}{creatorData.lastName} <small>{creatorData.id}</small></h2>
								<p>This creator doesn't have a description, sorry!</p>
								<ul className="fact-list">
									<li>Comics: {creatorData.numberOfComics}</li>
									<li>Series: {creatorData.numberOfSeries}</li>
									<li>Stories: {creatorData.numberOfStories}</li>
								</ul>
							</div>
						</div>
						<div className="col-sm-8 col-sm-offset-2">
							<div className="panel panel-default">
								<div className="panel-heading">Creator for </div>
								<div className="panel-body list-group">
									{creatorData.comics.map( comic => {
										return <a onClick={()=>this.props.history.push('comics/'+comic.id)} className="list-group-item comic-link">{comic.name}</a>
									})}
								</div>
							</div>
						</div>
					</div>
				</div>
			)
		} else {
			return (
				<div className="comic-page">
					<NavBar />
					<div className="container">
						<h2>No data yet, try again later!</h2>
					</div>
				</div>
			)
		}
	}
}

module.exports = CreatorPage;


// legends.js

const request = require('request');
const API = 'http://dudecarry.me/api/';

//Retrieve champions
function getChampions(cb){
	request(`${API}champions`, (error, response, body) => {
		cb(error, JSON.parse(body));
	})
}

// Retrieve the champion with the given ID
function getChampion(id, cb){
	request(API+'champion/'+id, (error, response, body) => {
		cb(error, JSON.parse(body));
	})
}

//Retrieve players
function getSummoners(cb){
	request(`${API}summoners`, (error, response, body) => {
		cb(error, JSON.parse(body));
	})
}

// Retrieve the player with the given ID
function getSummoner(id, cb){
	request(API+'summoner/'+id, (error, response, body) => {
		cb(error, JSON.parse(body));
	})
}

//Retrieve teams
function getTeams(cb){
	request(`${API}teams`, (error, response, body) => {
		cb(error, JSON.parse(body));
	})
}

// Retrieve the team with the given ID
function getTeam(id, cb){
	request(API+'team/'+id, (error, response, body) => {
		cb(error, JSON.parse(body));
	})
}

module.exports = {
	getChampion: getChampion,
	getChampions: getChampions,
	getSummoner: getSummoner,
	getSummoners: getSummoners,
	getTeam: getTeam,
	getTeams: getTeams
}

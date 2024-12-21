# To run
1. start the express server with `node expressMiddleware/express.js`
2. cd into resVote2.0 (`cd resVote2.0`) and run `npm start`

* Note: Make sure you have resVault set up on chrome. Currently I have mongo synced to main-net for resDB so connect to it.

# DO NOT RUN sync.js
* I don't know whether or not this will cause duplicates in mongoDB

### Notes
* To sync your mongoDB, change the mongoURI in `expressMiddleware/express.js` and `resVote2.0/src/mongoDB/sync.js`
  - Run sync.js to populate the transactions into your DB
  - Then run express.js to field requests from `resVote2.0/src/mongoDB/mongoAPI.js`

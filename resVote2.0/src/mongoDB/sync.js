const { WebSocketMongoSync } = require('resilient-node-cache');

const uri = "mongodb+srv://taculp:SRAo8EG1Ub6YFP6C@cluster0.htruocb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";
const mongoConfig = {
    uri: uri,
    dbName: "resDB",
    collectionName: "the_cache"
}


const resilientDBConfig = {
    // baseUrl: 'resilientdb://crow.resilientdb.com',
    baseUrl: "resilientdb://localhost:18000",
    httpSecure: false,
    wsSecure: false,
  };
  
  const sync = new WebSocketMongoSync(mongoConfig, resilientDBConfig);
  
  sync.on('connected', () => {
    console.log('WebSocket connected.');
  });
  
  sync.on('data', (newBlocks) => {
    console.log('Received new blocks:', newBlocks);
  });
  
  sync.on('error', (error) => {
    console.error('Error:', error);
  });
  
  sync.on('closed', () => {
    console.log('Connection closed.');
  });
  
  (async () => {
    try {
      await sync.initialize();
      console.log('Synchronization initialized.');
    } catch (error) {
      console.error('Error during sync initialization:', error);
    }
  })();
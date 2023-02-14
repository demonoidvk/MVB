# MVB
Parts of the SRC file:
1. Ledgers: (under development)
      Block: to handle the blocks to be committed
      Blockchain: to handle committing a block to the blockchain
2. main: 
      InputAndWrite: to get the message input by the user, with which node to send that message to.
      sender.py: to send the message recieved in above py file, to different nodes as per information.
      shutdown.py: to shutdown all different running threads and nodes, in one go. (under development)
3. nodes:
      listener: to listen to the new transactions request sent by InputAndWrite class
      NodeMain: to handle all the new requests, process them and add to list of processed transactions, which after sometime will be sent to block class(ledgers),
                for validation and approval from other nodes
      transactions: basic structure class for a single transaction
      unCommittedtransaction:  basic structure class for a single unCommitted transaction
4. utility:
      constants: to handle the port numbers, needed for the sender and listener connections
      util: Single python file, with all different functions that are shared between multiple files, like read json file, generate signature for a node, encryption,
            if a new node is added, generating a node_id and writing blockchain data in a final ledger file.
            
How to run the code:
1. run as many instances of NodeMain(through different terminals), as it will start 3 different threads per instance(new txn listener, broadcaster, compute engine)
2. Once all nodes are running, start the InputAndWrite, with syntax: python InputAndWrite.py "{\"sender\": \"J.J.\", \"reciever\": \"A.J\", \"message\": \"a\"}" 2
       here: 1st command line argument will be the message
            2nd witll be the node to which to send the message to.
       
       
Parts left for develment:
1. Handling Forking
2. Building the blockchain
3. Block verification code
4. Handling invalid transactions

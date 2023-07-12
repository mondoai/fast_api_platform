var db = db.getSiblingDB("ds_db");

db.ds_account.dropIndexes();
db.ds_account.drop();


db.ds_account.createIndex({"account_hash_code": 1});
db.ds_account.createIndex({"username": 1}, {unique: true});

db.ds_account.createIndex({"agent_profile.shipping_address.postal_address.geo_point": "2dsphere"});




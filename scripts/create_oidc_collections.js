var db = db.getSiblingDB("nf_db");

db.authorization_request.dropIndexes();
db.authorization_request.drop();

db.oidc_token.dropIndexes();
db.oidc_token.drop();

db.oidc_client.dropIndexes();
db.oidc_client.drop();

/**********************************************************************
 *
 *
 */
var authorization_request = {
    date_last_updated: new Date()
};
db.authorization_request.insert(authorization_request);

/**
 * authorization_request expiration index:
 */
db.authorization_request.createIndex({
    "expire_on": 1
}, {expireAfterSeconds: 600});

db.authorization_request.remove({});

/**********************************************************************
*                    neurofit token collection
*
*/

/**
 * oidc_token expiration index:
 */
db.oidc_token.createIndex({
    "expire_on": 1
}, {expireAfterSeconds: 172800});

db.oidc_token.remove({});

/*********************************************************************
*
*
*/

db.oidc_client.createIndex({"client_id": 1});

/**
 * user account collection
 */
db.user_account.createIndex({
    "username": 1
}, {unique: true});

db.user_account.createIndex({"username": 1, "password": 1});



authorization_request
device_scan_authorization
oidc_token
scan_results
system.indexes
user_account


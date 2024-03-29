var db = db.getSiblingDB("nf_db");

db.runCommand({
    dropAllUsersFromDatabase: 1,
    writeConcern: {
        w: "majority"
    }
});

db.dropDatabase();

db.createUser({
    user: "nf_db_user",
    pwd: "nf_db_pwd",
    roles: [{
        role: "readWrite",
        db: "nf_db"
    }]
});

/**
 *
 * @type {Object}
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
}, {
    expireAfterSeconds: 600
});

db.authorization_request.remove({});

/**
 * oidc_token expiration index:
 */
db.oidc_token.createIndex({
    "expire_on": 1
}, {
    expireAfterSeconds: 172800
});

db.oidc_token.remove({});

/**
 * user account collection
 */
db.user_account.createIndex({
    "username": 1
}, {
    unique: true
});

db.user_account.createIndex({
    "username": 1,
    "password": 1
});

/*********************************************************************
*
* OIDC client index
*/
db.oidc_client.createIndex({ "client_id": 1 });


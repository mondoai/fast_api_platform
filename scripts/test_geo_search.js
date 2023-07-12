var db = db.getSiblingDB("ds_db");

var match_crit = {
    "agent_profile.shipping_address.postal_address.geo_point": {
        $near: {
            $geometry: {
                type: "Point",
                coordinates: [-122.09994219999999, 37.3926924]
            },
            $maxDistance: 100000,
            $minDistance: 0
        }
    }
};

var options = {
    "_id": 1,
    "agent_profile.shipping_address.postal_address": 1,
    "agent_profile.shipping_address.for_business_name": 1,
    "account_status": 1,
    "agent_profile.services": 1,
    "agent_profile.storage_limit": 1,
    "agent_profile.available_hours": 1,
    "agent_profile.storage_description": 1,
    "agent_profile.business_address": 1,
    "agent_profile.picture_url": 1
};

db.ds_account.find(match_crit, options);

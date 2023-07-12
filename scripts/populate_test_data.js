var db = db.getSiblingDB("ds_db");

db.ds_account.remove({});

var ds_customer_account = {
    first_name: "April",
    middle_name: "June",
    last_name: "Doe",
    phone_number: "650-555-1234",
    email_address: "april@neurofit.com",
    account_hash_code: "197210082540",
    username: "april@neurofit.com",
    password: "april1234",
    locale: "en_US",

    account_status: {
        status: "ACTIVE",
        accepted_tnc: true,
        tnc_acceptance_date: new Date()
    },

    customer_profile: {
        completeness: "100",
        picture_url: "https://s3-us-west-2.amazonaws.com/neurofit/img/ms-icon-310x310.png",
        addresses: [{
            address_1: "938 Clark Ave",
            address_2: "",
            address_3: "",
            city: "Mountain View",
            state: "CA",
            country: "US",
            postal_code: "94040",
            geo_point: {
                type: "Point",
                coordinates: [-122.09994219999999, 37.3926924]
            },
            default: true
        }],
        favorite_agents: []
    },
    agent_profile: null,

    date_created: new Date(),
    date_last_updated: new Date()
};
db.ds_account.insert(ds_customer_account);



var ds_agnet_account = {
    first_name: "Jo",
    middle_name: "Brown",
    last_name: "Doe",
    phone_number: "650-555-1234",
    email_address: "lipstick@neurofit.com",
    account_hash_code: "197210082540",
    username: "lipstick@neurofit.com",
    password: "april1234",
    locale: "en_US",

    account_status: {
        status: "ACTIVE",
        accepted_tnc: true,
        tnc_acceptance_date: new Date()
    },

    customer_profile: null,
    agent_profile: {
        completeness: "100",
        picture_url: "https://s3-us-west-2.amazonaws.com/neurofit/img/ms-icon-310x310.png",
        shipping_address: {
            postal_address: {
                address_1: "750 Castro St",
                address_2: "",
                address_3: "",
                city: "Mountain View",
                state: "CA",
                country: "US",
                postal_code: "94041",
                geo_point: {
                    type: "Point",
                    coordinates: [-122.0832054, 37.3876059]
                }
            },
            for_business_name: "Beauty Supplies, Inc."
        },
        date_of_birth: new Date("1982-7-13"),
        ssn: "123-45-6789",
        address: {
            address_1: "750 Castro St",
            address_2: "",
            address_3: "",
            city: "Mountain View",
            state: "CA",
            country: "US",
            postal_code: "94041"
        },
        storage_limit: "50 shipments",
        available_hours: [
            ["0700-1200", "1300-1700"],
            ["0700-1200", "1300-1700"],
            ["0700-1200", "1300-1700"],
            ["0700-1200", "1300-1700"],
            ["0700-1200", "1300-1700"],
            ["0700-1200", "1300-1700"],
            ["0700-1200", "1300-1700"]
        ],
        services: ["RECEIVE", "SEND"],
        storage_description: "Back store storage",
        business_address: true,
        background_check: [{
            background_check_provider: "Security International",
            passed: true,
            results: ["Passed check for business", "passed check for personnel"]
        }]
    },

    date_created: new Date(),
    date_last_updated: new Date()
};
db.ds_account.insert(ds_agnet_account);

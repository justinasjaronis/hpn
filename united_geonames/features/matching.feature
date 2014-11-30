Feature: Matching

    Scenario: Matching by Name
        Given we have a City object "Vilnius"
        When get United Geo object "Vilnius"
        Then we will run matching for name "Wilno"


    Scenario: two different variations of input
        # http://aruodai.lan:1441/admin/united_geonames/unitedgeoname/9274/
        Given by user country "France" and name "Paris"
        Given by user country "Lithuania" and coordinates x "25.2798000000000016" y "54.6891600000000011"
        Given by user country "France" and region "Ile-de-France"
        Given by user country "France" and subregion "Paris"

        Given by user name "Paris" and coordinates x "-17.4285211665224082 " y "49.5145963084038527"
        Given by user name "Paris" and subregion "Paris"
        Given by user name "Paris" and region "Ile-de-France"

        Given by user only region "Ile-de-France"
        Given by user only subregion "Paris"
        Given by user only coordinates x "-17.4285211665224082 " y "49.5145963084038527"
        Given by user only country "France"
        Given by user only name "Vilnius"

        Given by user coordinates x "-17.4285211665224082" y "49.5145963084038527" and region "Ile-de-France"
        Given by user coordinates x "-17.4285211665224082" y "49.5145963084038527" and city "Paris"
        Given by user coordinates x "-17.4285211665224082" y "49.5145963084038527" and country "France"


    Scenario: three different variations of input
        Given by three: user name "Paris" coordinates x "-17.4285211665224082" y "49.5145963084038527" and region "Ile-de-France"
        Given by three: user name "Paris" region "Ile-de-France" subregion "Paris"
        Given by three: user name "Paris" country "France" subregion "Paris"
        Given by three: user name "Paris" country "France" region "Ile-de-France"
        Given by three: user coord x "-17.4285211665224082" coord y "49.5145963084038527" and region "Ile-de-France" subregion "Paris"
        Given by three: user coord x "-17.4285211665224082" coord y "49.5145963084038527" and region "Ile-de-France" country "France"


    Scenario: four different variations of input
        Given by four: user name "Paris" coordinates x "-17.4285211665224082" y "49.5145963084038527" and region "Ile-de-France" subregion "Paris"
        Given by four: user name "Paris" coordinates x "-17.4285211665224082" y "49.5145963084038527" and region "Ile-de-France" country "France"
        Given by four: user name "Paris" and region "Ile-de-France" country "France" subregion "Paris"
        Given by four: user coordinates x "-17.4285211665224082" y "49.5145963084038527" and region "Ile-de-France" country "France" subregion "Paris"


    Scenario: five different variations of input
        Given by five: user name "Paris" coordinates x "-17.4285211665224082" y "49.5145963084038527" and region "Ile-de-France" subregion "Paris" country "France"


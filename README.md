# Data-science

This is the data science component of [the airprice app for optimizing AirBnB listings in Berlin](https://airprice.now.sh/protected).

### Endpoints

The api currently lives at [optimalprice.stromsy.com](optimalprice.stromsy.com).

GET https://optimalprice.stromsy.com/lookup-neighborhood
  * expects URL parameters:
      * longitude: number
      * latitude: number
  * returns JSON object:
  {"neighborhood": neighborhood}
  
POST https://optimalprice.stromsy.com/estimate-price
  * expects form parameters:
      * neighborhood: str, should be one of these values: ['Reinickendorf', 'Steglitz - Zehlendorf', 'Tempelhof - Schöneberg', 'Lichtenberg', 'Spandau', 'Charlottenburg-Wilm.', 'Friedrichshain-Kreuzberg', 'Pankow', 'Treptow - Köpenick', 'Mitte', 'Marzahn - Hellersdorf', 'Neukölln']
      * room_type: str, should be one of these values: ['Entire home/apt', 'Private room', 'Shared room', 'Hotel room']
      * listings_count: int, total number of listings by the host
      * num_reviews: int, number of reviews on the listing
      * min_nights: int, minimum number of nights on the listing
      * availability: int, number of nights per year the listing is available
      * last_review_time: int, the number of seconds ago that the last review was posted
  * returns JSON object:
  {"price": price}

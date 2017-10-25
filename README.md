# tap-reviewscouk

A singer.io tap for extracting data from reviews.co.uk API, written in python 3.

Author: Hugh Nimmo-Smith (hugh@onedox.com)

## Limitations

Current limitations include:

- Only supports merchant reviews (no product reviews)
- No error handling

## Configuration

A ```store```, ```apikey``` and ```start_date``` config keys are required:

```
{
  "store": "onedox",
  "apikey": "abcdefgh1234567890",
  "start_date": "2015-01-01"
}
```

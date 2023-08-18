# Receipt Processor

An implementation of the [receipt processor](https://github.com/fetch-rewards/receipt-processor-challenge) using python and flask.

## To run it

A Dockerfile is provided to create the image needed to test this. 

```bash
# build the image
docker build . -t receipt-processor

# run the image exposing the ports used by Flask
docker run -p 5555:5555 receipt-processor

# or run the image in background
docker run -d -p 5555:5555 receipt-processor
```

## Testing

### With unit tests

The project uses pytest to run all the different test in the `tests` directory.

To run the test run the `./run-image-tests.sh` script once you created the image or run:

```bash
docker run -it --entrypoint pytest receipt-processor
```
Current coverage: `100%`

### With the image

To test directly on the server you can use curl to post a json from the `fixtures` directory
```bash
$ curl -X POST -H "Content-Type: application/json"  -d @tests/fixtures/receipt-target.json localhost:5555/receipt/process
# the response
{"id":"f87b9dcf-07c0-4cdf-82cb-cdd2d60a9541"}

#then you can use that id to retrieve the info
$ curl -X GET localhost:5555/receipt/f87b9dcf-07c0-4cdf-82cb-cdd2d60a9541/points
{"points":28}
```

## future improvements

- Use redis or other similar tool to store receipts
- Use a queue or similar approach to calculate points
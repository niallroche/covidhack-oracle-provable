""":cvarassign a request id
fetch data
store underlying data
get etag and last modified or other data


extract data from underlying data source html/xml/json/rdf

do any NLP or regular expressions to extract target data

validate that data was found and the format and range is expected
is there a drift from the expected result or previous errors that may indicate an issue

if there is an underlying issue with the data then return an error according to the schema depending on the type of error
include a confidence level with the data if applicable/possible (dependant on extraction approach and model)

encode in schema hash and sign

compute a hash of the data and extracted values and meta data and sign and store in IPFS
for audit purposes with the request id

include data references in the output

return to sender using appropriate encodings and headers


fetch
"""
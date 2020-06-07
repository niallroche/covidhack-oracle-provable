/*
MIT License

Copyright (c) 2020 Niall Roche

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

"use strict";

const pinataSDK = require('@pinata/sdk');
const pinata_api_key = process.env.PINATA_API_KEY
const pinata_api_secret = process.env.PINATA_SECRET_API_KEY
const pinata = pinataSDK(pinata_api_key, pinata_api_secret);
const { Readable } = require("stream")
const fs = require("fs");

module.exports.saveToIPFS = function(event, context, callback) {
    console.info('in handler')
    console.info(event)
    // let requestBody = JSON.parse(event.body)
    console.info(event.body)

    let body = event
    // test if the function is being invoked directly or from another function as it determines how the input content is wrapped
    if (event.body === undefined) {
        console.info('using entire body')
    } else {
        body = JSON.parse(event.body)
        console.info('parsing using body')
    }

    // console.info(requestBody)
    // pinata.testAuthentication().then((result) => {
    //     //handle successful authentication here
    //     console.log(result);
    //     const response = {
    //         statusCode: 200,
    //         body: JSON.stringify(result),
    //     };
    //
    //     callback(null, response);
    // }).catch((err) => {
    //     //handle error here
    //     console.log(err);
    // });

    // const body = {
    //     message: 'Pinatas are awesome'
    // };
    // const body = JSON.parse(jsoncontent)
    const options = {
        pinataMetadata: {
            name: 'MyCustomName',
            keyvalues: {
                customKey: 'customValue',
                customKey2: 'customValue2'
            }
        },
        pinataOptions: {
            cidVersion: 0
        }
    };

    const input_string = JSON.stringify(body)
    // const stream = fs.createWriteStream("data.json")
    // stream.write(input_string)

    // var s3 = new AWS.S3({apiVersion: '2006-03-01'})
    // var params = {Bucket: 'myBucket', Key: 'data.json'}
    //
    // var file = require('fs').createWriteStream('/path/to/file.jpg')
    // s3.getObject(params).createReadStream().pipe(file)

    // module.exports.pinDataFileToIPFS()
    module.exports.pinDataFileToIPFS(input_string, '5f3110b4af0f23d9195f', '34bb31e5734de77b77be3c9bc6b6d443f5808f58e55a8afc7dc5887458c38525')

    // const readable = Readable.from([input_string])
    // const readable = ReadableString(input_string)
    // const readable = Readable.from(input_string, {encoding: 'utf8'})
    // const readable = fs.createReadStream("data.json")
    pinata.pinJSONToIPFS(body, options).then((result) => {

    // pinata.pinFileToIPFS(readable, options).then((result) => {
    // pinata.pinJSONToIPFS(body, options).then((result) => {
        //handle results here
        console.log(result);
        const response = {
            statusCode: 200,
            body: JSON.stringify(result),
        };

        callback(null, response);
    }).catch((err) => {
        //handle error here
        console.log(err);
    });
};

// save

//retrieve from IPFS
module.exports.load_from_ipfs = function(event, context, callback) {

    pinata.unpin("QmP9AdfUmscMFErpaViL2Xxcn4ziQTxoDDjQALUWQMoPWX").then((result) => {
        //handle results here
        console.log(result);
        const response = {
            statusCode: 200,
            body: JSON.stringify(result),
        };

        callback(null, response);
    }).catch((err) => {
        //handle error here
        console.log(err);
    });
};

// class ReadableString extends Readable {
//   private sent = false
//
//   constructor(private str: string) {
//     super();
//   }
//
//   _read() {
//     if (!this.sent) {
//       this.push(Buffer.from(this.str));
//       this.sent = true
//     }
//     else {
//       this.push(null)
//     }
//   }
// }

const axios = require('axios');
// const fs = require('fs');
const FormData = require('form-data');

// export const pinFileToIPFS = (input_string, pinataApiKey, pinataSecretApiKey) => {
module.exports.pinDataFileToIPFS = (input_string, pinataApiKey, pinataSecretApiKey) => {
    const url = `https://api.pinata.cloud/pinning/pinFileToIPFS`;

    //we gather a local file for this example, but any valid readStream source will work here.
    let data = new FormData();

    // async function * generate() {
    //   yield 'hello';
    //   yield 'streams';
    // }

    // const readable = Readable.from(generate());
    // const readable = Readable.from([input_string], {encoding: 'utf8'})
    // const readable = new Buffer(input_string);
    const readable = new Buffer("input_string");
    data.append('file', readable, {filename:'testfile.txt', contentType:'text/plain'})
    // data.append('file', fs.createReadStream('./yourfile.png'));

    //You'll need to make sure that the metadata is in the form of a JSON object that's been convered to a string
    //metadata is optional
    const metadata = JSON.stringify({
        name: 'testname',
        keyvalues: {
            exampleKey: 'exampleValue'
        }
    });
    data.append('pinataMetadata', metadata);

    //pinataOptions are optional
    const pinataOptions = JSON.stringify({
        cidVersion: 0,
        customPinPolicy: {
            regions: [
                {
                    id: 'FRA1',
                    desiredReplicationCount: 1
                },
                {
                    id: 'NYC1',
                    desiredReplicationCount: 2
                }
            ]
        }
    });
    data.append('pinataOptions', pinataOptions);

    return axios.post(url,
        data,
        {
            maxContentLength: 'Infinity', //this is needed to prevent axios from erroring out with large files
            headers: {
                'Content-Type': `multipart/form-data; boundary=${data._boundary}`,
                'pinata_api_key': pinataApiKey,
                'pinata_secret_api_key': pinataSecretApiKey
            }
        }
    ).then(function (response) {
        //handle response here
        console.log('pinFileToIPFS resp')
        console.log(response)
        console.log('pinFileToIPFS resp data')
        console.log(response.data)
    }).catch(function (error) {
        console.log('pinFileToIPFS error')
        //handle error here
         console.error(error)
    });
};
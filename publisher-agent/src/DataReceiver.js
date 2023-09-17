import dgram from "dgram";
import client from 'prom-client'
import DataGui from './models/DataGui.js';
import AlarmMsg from './models/AlarmMsg.js';
let importer
if (process.env.PROTOCOL==='AMQP') {importer=await import("./DataSenderAMQP.js");}
else if (process.env.PROTOCOL==='MQTT'){importer=await import("./DataSenderMQTT.js");}

let s_port = 8053;
const recieving_timeout = Number(process.env.SLEEP_TIME)
let channel = await importer.connect();
let server = dgram.createSocket("udp4");

let tags = []
let timeouts = []

const counter = new client.Counter({
  name: 'Tags_tracikng',
  help: 'The number of tags tracked',
});

server.on("listening", async function () {
  let address = server.address();
  console.log("server listening " + address.address + ":" + address.port);
});

server.on("message", async function (msg) {
  let data = getDataObject(msg.toString())
  console.log("First data" + data);
  let f;

  if (!tags.includes(data.tagID)) {
    counter.inc();
    tags.push(data.tagID)
    timeouts.push(true)
  }
  tags.some(function (item, index) { f = index; return item == data.tagID; })
  if (channel != null) {
    if (timeouts[f]) {
      await importer.sendMessage(channel, data.tagID, data)
      timeouts[f] = false
      timer(f)
    }
  }
  else {
    channel = await importer.connect();
    console.log("channel " + channel);
    if (channel != null) {
      await importer.sendMessage(channel, data.tagID, data)
    }
  }
});

async function timer(f) {
  setTimeout(() => {
    timeouts[f] = true
  }, recieving_timeout)
}

server.on("error", function (err) {
  console.log("server error: \n" + err.stack);
  server.close();
});

server.on("close", function () {
  console.log("closed.");
});

server.bind(s_port);

function getDataObject(rawData) {
  let aux = rawData.split(";");
  //return new DataGui(...aux)
  if (aux[0] == "107"){
    return new DataGui(...aux)
  } else if (aux[0] == "108"){
    return new AlarmMsg(...aux)
  }
}

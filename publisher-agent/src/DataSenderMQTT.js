import mqtt from 'mqtt';
const MQTT_TOPIC = process.env.TOPIC;
const MQTT_QUEUE_HOST = process.env.MQTT_QUEUE_HOST;
const MQTT_QUEUE_PORT = process.env.MQTT_QUEUE_PORT;

export async function connect() {
    try {
    const connectUrl = `mqtt://${MQTT_QUEUE_HOST}:${MQTT_QUEUE_PORT}`

    // MQTT options
    const options = {
        clientId: 'publisher-agent',
        keepalive: 0,
        clean: true,
        reconnectPeriod: 0
    };

    const client = mqtt.connect(connectUrl, options)
    return client
    } catch (error) {
        return null
    }
}

export function sendMessage(channel, topic, msg) {
    var key = MQTT_TOPIC    //var key = 'tracking.tags.'+topic;
      
  channel.publish(key, Buffer.from(JSON.stringify(msg)));
    console.log(" [x] Sent %s:'%s'", key, msg);
}
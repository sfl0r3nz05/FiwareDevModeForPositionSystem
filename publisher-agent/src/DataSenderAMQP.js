import amqp from 'amqplib';
const AMQP_QUEUE_HOST = process.env.AMQP_QUEUE_HOST;
const AMQP_QUEUE_PORT = process.env.AMQP_QUEUE_PORT;

export async function connect() {
  try {
  const connection = await amqp.connect(`amqp://${AMQP_QUEUE_HOST}:${AMQP_QUEUE_PORT}`, "heartbeat=60")
  const channel = await connection.createChannel()
  return channel
  } catch (error) {
      return null
  }
}

export async function sendMessage(channel, topic, msg) {
  // create the queues with different priorities
  await channel.assertQueue('high-priority', { arguments: { 'x-max-priority': 10 } });
  await channel.assertQueue('low-priority', { arguments: { 'x-max-priority': 1 } });

  // send messages to each queue with priority
  if (msg["ID_mensaje"] == "108") {
    await channel.sendToQueue('high-priority', Buffer.from(JSON.stringify(msg)), { priority: 10 });
  }
  else{
    await channel.sendToQueue('low-priority', Buffer.from(JSON.stringify(msg)), { priority: 1 });
  }
}
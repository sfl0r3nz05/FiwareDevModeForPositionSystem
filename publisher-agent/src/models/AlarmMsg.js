class AlarmMsg {
    constructor(ID_mensaje, timestamp, tagID, AlarmType) {
        this.ID_mensaje = Number(ID_mensaje)
        this.timestamp = timestamp
        this.tagID = tagID
        this.AlarmType = Number(AlarmType)
    }
    
}
export default AlarmMsg

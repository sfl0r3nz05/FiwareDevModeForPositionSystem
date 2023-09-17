class DataGui {
    constructor(ID_mensaje, timestamp, tagID, x, y, z, hpl_1, vpl, SingularMatrix) {
        this.ID_mensaje = Number(ID_mensaje)
        this.timestamp = timestamp
        this.tagID = tagID
        this.x = parseFloat(x)
        this.y = parseFloat(y)
        this.z = parseFloat(z)
        this.hpl_1 = parseFloat(hpl_1)
        this.vpl = parseFloat(vpl)
        this.SingularMatrix = Number(SingularMatrix)
    }
    
}
export default DataGui
